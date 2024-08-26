from . import get_db_connection
from flask_app.models.statistics import Statistics
from datetime import datetime, date, timedelta


class ClientManager:
    """
    Class responsible for client-related operations.
    """
    
    @staticmethod
    def get_all_clients(page=1, per_page=10, order_by="active_policies_count", order_dir="asc"):
        with get_db_connection() as conn:
            offset = (page - 1) * per_page
            order_clause = f"{order_by} {order_dir}"

            clients = conn.execute(
                f"""
                WITH policy_summary AS (
                    SELECT clients.client_id,
                        COUNT(DISTINCT CASE 
                            WHEN insurance_policies.end_date > date('now') 
                            THEN insurance_policies.policy_id 
                            END) AS active_policies_count,
                        SUM(CASE 
                            WHEN insurance_policies.status = 'Approved' 
                                AND insurance_policies.end_date > date('now')
                            THEN insurance_policies.premium_amount 
                            ELSE 0 
                            END) AS monthly_premium,
                        SUM(CASE 
                            WHEN insurance_policies.status = 'Approved' 
                            THEN (julianday(MIN(insurance_policies.end_date, date('now'))) - julianday(insurance_policies.start_date)) / 30.0 * insurance_policies.premium_amount
                            ELSE 0 
                            END) AS indv_total_premium
                    FROM clients
                    LEFT JOIN insurance_policies ON clients.client_id = insurance_policies.client_id
                    WHERE clients.first_name != 'Admin'
                    GROUP BY clients.client_id
                ),
                claim_summary AS (
                    SELECT insurance_policies.client_id,
                        COUNT(DISTINCT claims.claim_id) AS claim_count,
                        SUM(CASE WHEN claims.status = 'Paid' THEN claims.claim_amount ELSE 0 END) AS paid_claim_sum
                    FROM insurance_policies
                    LEFT JOIN claims ON insurance_policies.policy_id = claims.policy_id
                    GROUP BY insurance_policies.client_id
                )
                SELECT clients.*,
                    COALESCE(claim_summary.claim_count, 0) AS claim_count,
                    COALESCE(policy_summary.active_policies_count, 0) AS active_policies_count,
                    COALESCE(policy_summary.monthly_premium, 0) AS monthly_premium,
                    COALESCE(policy_summary.indv_total_premium, 0) AS indv_total_premium,
                    COALESCE(claim_summary.paid_claim_sum, 0) AS paid_claim_sum
                FROM clients
                LEFT JOIN policy_summary ON clients.client_id = policy_summary.client_id
                LEFT JOIN claim_summary ON clients.client_id = claim_summary.client_id
                WHERE clients.first_name != 'Admin'
                ORDER BY {order_clause}
                LIMIT {per_page} OFFSET {offset}
                """
            ).fetchall()

            total_clients = conn.execute(
                "SELECT COUNT(*) FROM clients WHERE first_name != 'Admin'"
            ).fetchone()[0]

        return clients, total_clients

    @staticmethod
    def get_client_by_id(client_id):
        with get_db_connection() as conn:
            client = conn.execute(
                "SELECT * FROM clients WHERE client_id = ?", (client_id,)
            ).fetchone()
        return client

    @staticmethod
    def get_client_by_email(email):
        with get_db_connection() as conn:
            client = conn.execute(
                "SELECT * FROM clients WHERE email = ?", (email,)
            ).fetchone()
        return client

    @staticmethod
    def add_client(first_name, last_name, date_of_birth, email, phone, street, city, state, zip_, photo_link):
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO clients (first_name, last_name, date_of_birth, email, phone, street, city, state, zip, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (first_name, last_name, date_of_birth, email, phone, street, city, state, zip_, photo_link),
            )
            conn.commit()

    @staticmethod
    def update_client(client_id, first_name, last_name, date_of_birth, email, phone, street, city, state, zip_, photo):
        with get_db_connection() as conn:
            conn.execute(
                "UPDATE clients SET first_name = ?, last_name = ?, date_of_birth = ?, email = ?, phone = ?, street = ?, city = ?, state = ?, zip = ?, photo = ? WHERE client_id = ?",
                (first_name, last_name, date_of_birth, email, phone, street, city, state, zip_, photo, client_id),
            )
            conn.commit()

    @staticmethod
    def delete_client(client_id):
        PolicyManager.delete_policies_by_client(client_id)
        with get_db_connection() as conn:
            conn.execute("DELETE FROM clients WHERE client_id = ?", (client_id,))
            conn.commit()


class PolicyManager:
    """
    Class responsible for policy-related operations.
    """
    
    @staticmethod
    def renew_policy(policy_id):
        with get_db_connection() as conn:
            conn.execute(
                "UPDATE insurance_policies SET Renewed = Renewed + 1 WHERE policy_id = ?",
                (policy_id,),
            )
            conn.commit()

    @staticmethod
    def get_sum_of_earned_premiums_by_client_id(client_id):
        with get_db_connection() as conn:
            policies = conn.execute(
                "SELECT policy_id FROM insurance_policies WHERE client_id = ? AND status == 'Approved'",
                (client_id,)
            ).fetchall()

        total_earned_premiums = sum(
            Statistics.get_premium_for_policy(policy['policy_id']) for policy in policies
        )

        return total_earned_premiums

    @staticmethod
    def get_number_of_active_policies(client_id):
        with get_db_connection() as conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM insurance_policies WHERE client_id = ? AND end_date > ? AND status == 'Approved'",
                (client_id, datetime.now().date())
            ).fetchone()[0]
        return count or 0

    @staticmethod
    def get_number_of_expired_policies(client_id):
        with get_db_connection() as conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM insurance_policies WHERE client_id = ? AND end_date <= ? And status = 'Approved'",
                (client_id, datetime.now().date())
            ).fetchone()[0]
        return count or 0

    @staticmethod
    def get_premium_per_month_on_active_policies(client_id):
        with get_db_connection() as conn:
            premium_per_month = conn.execute(
                "SELECT SUM(premium_amount) FROM insurance_policies WHERE client_id = ? AND end_date > ? AND status == 'Approved'",
                (client_id, datetime.now().date())
            ).fetchone()[0]
        return premium_per_month or 0

    # sum of earned premiums for each policy in client details
    @staticmethod
    def get_premium_for_policy(policy_id):
        with get_db_connection() as conn:
            result = conn.execute(
                "SELECT premium_amount, start_date, end_date FROM insurance_policies WHERE policy_id = ? AND status == 'Approved'",
                (policy_id,)
            ).fetchone()

        if result is not None:
            premium = result['premium_amount']
            start_date = datetime.strptime(result['start_date'], "%Y-%m-%d")
            end_date = datetime.strptime(result['end_date'], "%Y-%m-%d")

            # Useing the current date to calculate the total active period
            current_date = datetime.now()

            # Calculating the number of full months the policy is active until now
            if current_date < end_date:
                active_end_date = current_date
            else:
                active_end_date = end_date

            total_premium = 0
            current_premium_date = start_date

            while current_premium_date <= active_end_date:
                total_premium += premium
                # Incrementing the date by one month, ensuring the day of the month remains consistent
                next_month = current_premium_date.month % 12 + 1
                next_year = current_premium_date.year + (current_premium_date.month // 12)
                days_in_next_month = (datetime(next_year, next_month % 12 + 1, 1) - timedelta(days=1)).day
                next_day = min(current_premium_date.day, days_in_next_month)
                current_premium_date = datetime(next_year, next_month, next_day)

            return total_premium

        return 0

    @staticmethod    
    def get_policies_with_claim_counts(client_id):
        with get_db_connection() as conn:
            policies = conn.execute("""
                SELECT 
                    p.*,
                    (SELECT COUNT(*) FROM claims c WHERE c.policy_id = p.policy_id) AS claim_count,
                    CASE WHEN p.end_date >= ? THEN 'Active' ELSE 'Expired' END AS activity
                FROM insurance_policies p
                WHERE p.client_id = ?
            """, (date.today(), client_id)).fetchall()
        return policies

    @staticmethod
    def delete_policies_by_client(client_id):
        with get_db_connection() as conn:
            policies = conn.execute(
                "SELECT policy_id FROM insurance_policies WHERE client_id = ?", (client_id,)
            ).fetchall()

            for policy in policies:
                ClaimsManager.delete_claims_by_policy(policy["policy_id"])
            
            conn.execute("DELETE FROM insurance_policies WHERE client_id = ?", (client_id,))
            conn.commit()

    @staticmethod
    def is_policy_ending_within_a_week(end_date):
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d").date()
        today = datetime.today().date()
        return today <= end_date_obj <= (today + timedelta(days=7))


class ClaimsManager:
    """
    Class responsible for claim-related operations.
    """
    
    @staticmethod
    def delete_claims_by_policy(policy_id):
        with get_db_connection() as conn:
            conn.execute("DELETE FROM claims WHERE policy_id = ?", (policy_id,))
            conn.commit()

    @staticmethod
    def get_total_claims_by_client_id(client_id):
        with get_db_connection() as conn:
            total_claims = conn.execute(
                "SELECT SUM(claim_amount) FROM claims WHERE policy_id IN (SELECT policy_id FROM insurance_policies WHERE client_id = ?) AND status == 'Paid'", 
                (client_id,)
            ).fetchone()[0]
        return total_claims or 0
