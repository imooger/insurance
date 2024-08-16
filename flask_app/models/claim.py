from . import get_db_connection

class Claim:

    @staticmethod
    def get_all_claims_for_admin(order_by="claim_date", order_dir="asc"):
        with get_db_connection() as conn:
            # Update the query to handle integer sorting for policy_number
            if order_by == "policy_number":
                order_by_clause = f"CAST({order_by} AS INTEGER) {order_dir}"
            else:
                order_by_clause = f"{order_by} {order_dir}"
            claims = conn.execute(
                f"""
                SELECT claims.*, insurance_policies.client_id, clients.first_name, clients.last_name, insurance_policies.policy_number, insurance_policies.policy_type
                FROM claims
                JOIN insurance_policies ON claims.policy_id = insurance_policies.policy_id
                JOIN clients ON insurance_policies.client_id = clients.client_id
                ORDER BY {order_by_clause}
                """
            ).fetchall()
            #print(len(claims))  # the returned claims
        return claims

    @staticmethod
    def get_claims_for_insured(email, order_by="claim_date", order_dir="asc"):
        with get_db_connection() as conn:
            # Update the query to handle integer sorting for policy_number
            if order_by == "policy_number":
                order_by_clause = f"CAST({order_by} AS INTEGER) {order_dir}"
            else:
                order_by_clause = f"{order_by} {order_dir}"
            claims = conn.execute(
                f"""
                SELECT claims.*, insurance_policies.client_id, clients.first_name, clients.last_name, insurance_policies.policy_number, insurance_policies.policy_type
                FROM claims
                JOIN insurance_policies ON claims.policy_id = insurance_policies.policy_id
                JOIN clients ON insurance_policies.client_id = clients.client_id
                WHERE clients.email = ?
                ORDER BY {order_by_clause}
                """,
                (email,),
            ).fetchall()
            #print(claims)  # returned claims
        return claims


    @staticmethod
    def get_claim_by_id(claim_id):
        with get_db_connection() as conn:
            claim = conn.execute(
                "SELECT * FROM claims WHERE claim_id = ?", (claim_id,)
            ).fetchone()
        return claim

    @staticmethod
    def add_claim(policy_id, description, claim_amount, claim_date, status):
        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO claims (policy_id, description, claim_amount, claim_date, status) VALUES (?, ?, ?, ?, ?)",
                (policy_id, description, claim_amount, claim_date, status),
            )
            conn.commit()

    @staticmethod
    def update_claim(claim_id, description, claim_amount, claim_date, status):
        with get_db_connection() as conn:
            conn.execute(
                "UPDATE claims SET description = ?, claim_amount = ?, claim_date = ?, status = ? WHERE claim_id = ?",
                (description, claim_amount, claim_date, status, claim_id),
            )
            conn.commit()

    @staticmethod
    def delete_claim(claim_id):
        with get_db_connection() as conn:
            conn.execute("DELETE FROM claims WHERE claim_id = ?", (claim_id,))
            conn.commit()

    @staticmethod
    def get_claims_for_client(client_id):
        with get_db_connection() as conn:
            claims = conn.execute(
                "SELECT * FROM claims WHERE policy_id IN (SELECT policy_id FROM insurance_policies WHERE client_id = ?)",
                (client_id,)
            ).fetchall()
        return claims

    @staticmethod
    def get_claims_by_policy(policy_id):
        with get_db_connection() as conn:
            claims = conn.execute(
                "SELECT claim_id FROM claims WHERE policy_id = ?", (policy_id,)
            ).fetchall()
            return [claim[0] for claim in claims]

    
