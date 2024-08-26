from . import get_db_connection
from datetime import date, timedelta, datetime

# Handles retrieval and management of policies
class PolicyService:

    @staticmethod
    def get_policy_count():
        with get_db_connection() as conn:
            count = conn.execute(
                """
                SELECT COUNT(*) AS total_count
                FROM insurance_policies
                """
            ).fetchone()
        return count["total_count"]

    @staticmethod
    def get_policies_for_admin_paginated(page=1, per_page=10, order_by="end_date", order_dir="asc"):
        offset = (page - 1) * per_page
        with get_db_connection() as conn:
            if order_by == "policy_number":
                order_by_clause = f"CAST({order_by} AS INTEGER) {order_dir}"
            else:
                order_by_clause = f"{order_by} {order_dir}"

            rows = conn.execute(
                f"""
                SELECT insurance_policies.*, clients.first_name, clients.last_name, clients.date_of_birth,
                    CASE WHEN end_date >= date('now') THEN 'Active' ELSE 'Expired' END AS activity,
                    (SELECT COUNT(*) FROM claims WHERE claims.policy_id = insurance_policies.policy_id) AS claim_count,
                    SUM(CASE 
                        WHEN insurance_policies.status = 'Approved' 
                            AND insurance_policies.end_date > date('now')
                        THEN insurance_policies.premium_amount 
                        ELSE 0 
                    END) AS total_premium
                FROM insurance_policies
                JOIN clients ON insurance_policies.client_id = clients.client_id
                GROUP BY insurance_policies.policy_id, clients.client_id
                ORDER BY {order_by_clause}
                LIMIT ? OFFSET ?
                """,
                (per_page, offset)
            ).fetchall()

            policies = [dict(row) for row in rows]
        return policies

    @staticmethod
    def get_all_policies_for_admin(order_by="end_date", order_dir="asc", page=1):
        return PolicyService.get_policies_for_admin_paginated(page=page, order_by=order_by, order_dir=order_dir)


    @staticmethod
    def get_policies_for_insured(email, order_by="end_date", order_dir="asc"):
        today = date.today()
        with get_db_connection() as conn:
            if order_by == "policy_number":
                order_by_clause = f"CAST({order_by} AS INTEGER) {order_dir}"
            else:
                order_by_clause = f"{order_by} {order_dir}"
            policies = conn.execute(
                f"""
                SELECT insurance_policies.*, clients.first_name, clients.last_name,
                    CASE WHEN end_date >= ? THEN 'Active' ELSE 'Expired' END AS activity,
                    (SELECT COUNT(*) FROM claims WHERE claims.policy_id = insurance_policies.policy_id) AS claim_count
                FROM insurance_policies
                JOIN clients ON insurance_policies.client_id = clients.client_id
                WHERE clients.email = ?
                ORDER BY {order_by_clause}
                """,
                (today, email,)
            ).fetchall()
        return policies

    @staticmethod
    def get_policy_by_id(policy_id):
        with get_db_connection() as conn:
            policy = conn.execute(
                """
                SELECT insurance_policies.*, clients.first_name, clients.last_name,clients.date_of_birth,clients.phone,clients.email,
                    CASE WHEN end_date >= date('now') THEN 'Active' ELSE 'Expired' END AS activity
                FROM insurance_policies
                JOIN clients ON insurance_policies.client_id = clients.client_id
                WHERE policy_id = ?
                """,
                (policy_id,)
            ).fetchone()
        return policy

    @staticmethod
    def get_policies_by_client_id(client_id):
        with get_db_connection() as conn:
            policies = conn.execute(
                """
                SELECT *, CASE WHEN end_date >= ? THEN 'Active' ELSE 'Expired' END AS activity
                FROM insurance_policies
                WHERE client_id = ?
                """,
                (date.today(), client_id)
            ).fetchall()
        return policies


# Handles creation, updates, deletion, and renewal of policies
class PolicyManagementService:

    @staticmethod
    def add_policy(client_id, policy_number, policy_type, start_date, end_date, premium_amount, status):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''
            INSERT INTO insurance_policies (client_id, policy_number, policy_type, start_date, end_date, premium_amount, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (client_id, policy_number, policy_type, start_date, end_date, premium_amount, status)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def update_policy(policy_id, policy_number, policy_type, start_date, end_date, premium_amount, renewed, status):
        with get_db_connection() as conn:
            # Fetching the existing policy to preserve the renewed count
            existing_policy = conn.execute(
                "SELECT renewed FROM insurance_policies WHERE policy_id = ?", (policy_id,)
            ).fetchone()

            if not existing_policy:
                raise ValueError("Policy not found")

            # renewed = existing_policy["renewed"]

            conn.execute(
                """
                UPDATE insurance_policies 
                SET 
                    policy_number = ?, 
                    policy_type = ?, 
                    start_date = ?, 
                    end_date = ?, 
                    premium_amount = ?,
                    renewed = ?,
                    status = ?
                WHERE policy_id = ?
                """,
                (
                    policy_number,
                    policy_type,
                    start_date,
                    end_date,
                    premium_amount,
                    renewed,
                    status,
                    policy_id,
                )
            )
            conn.commit()

    @staticmethod
    def delete_policy(policy_id):
        with get_db_connection() as conn:
            conn.execute(
                "DELETE FROM insurance_policies WHERE policy_id = ?", (policy_id,)
            )
            conn.commit()

    @staticmethod
    def renew_policy(policy_id):
        with get_db_connection() as conn:
            today = datetime.today().date()
            next_year = today + timedelta(days=364)
            # Fetching the expired policy data
            expired_policy = conn.execute(
                "SELECT * FROM insurance_policies WHERE policy_id = ?", (policy_id,)
            ).fetchone()

            if not expired_policy:
                raise ValueError("Policy not found")

            # New policy with the same data
            client_id = expired_policy["client_id"]
            policy_number = expired_policy["policy_number"]
            policy_type = expired_policy["policy_type"]
            start_date = today
            end_date = next_year
            premium_amount = expired_policy["premium_amount"]
            status = "Approved" 

            # Inserting the new policy into the database
            PolicyManagementService.add_policy(
                client_id, policy_number, policy_type, start_date, end_date, premium_amount, status
            )

            renewed = expired_policy["renewed"] + 1 if expired_policy["renewed"] else 1
            conn.execute(
                """
                UPDATE insurance_policies 
                SET 
                    renewed = ?
                WHERE policy_id = ?
                """,
                (renewed, policy_id,)
            )
            conn.commit()


# Handles claims-related operations
class ClaimsService:

    @staticmethod
    def get_claims_by_policy_id(policy_id, order_by="claim_date", order_dir="asc"):
        with get_db_connection() as conn:
            if order_by == "claim_amount":
                order_by_clause = f"CAST({order_by} AS FLOAT) {order_dir}"
            else:
                order_by_clause = f"{order_by} {order_dir}"
            claims = conn.execute(
                f"""
                SELECT * FROM claims 
                WHERE policy_id = ?
                ORDER BY {order_by_clause}
                """,
                (policy_id,)
            ).fetchall()
        return claims

    @staticmethod
    def get_last_policy_id():
        with get_db_connection() as conn:
            last_policy = conn.execute(
                "SELECT policy_id FROM insurance_policies ORDER BY policy_id DESC LIMIT 1"
            ).fetchone()
            if last_policy:
                return last_policy["policy_id"]
            return None