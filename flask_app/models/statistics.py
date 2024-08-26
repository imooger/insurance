from . import get_db_connection
from datetime import datetime, timedelta


class Statistics:

    @staticmethod
    def get_client_count():
        with get_db_connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
        return count



    @staticmethod
    def get_policy_count():
        with get_db_connection() as conn:
            current_date = datetime.now().strftime("%Y-%m-%d")
            count = conn.execute(
                """
                SELECT COUNT(*)
                FROM insurance_policies
                WHERE status = 'Approved'
                AND start_date <= ? 
                AND end_date >= ?
                """,
                (current_date, current_date)
            ).fetchone()[0]
        return count

    @staticmethod
    def get_claim_count():
        with get_db_connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM claims").fetchone()[0]
        return count

    @staticmethod
    def get_new_claim_count():
        with get_db_connection() as conn:
            count = conn.execute("SELECT COUNT(*) FROM claims WHERE status == 'New'").fetchone()[0]
        return count

    @staticmethod
    def get_total_claim_amount():
        with get_db_connection() as conn:
            total = conn.execute(
                """
                SELECT SUM(claim_amount) 
                FROM claims 
                WHERE status = 'Paid'
                """
            ).fetchone()[0]
        return total if total is not None else 0


    @staticmethod
    def get_average_policies_per_client():
        with get_db_connection() as conn:
            avg = conn.execute(
                "SELECT AVG(policy_count) FROM (SELECT COUNT(*) as policy_count FROM insurance_policies GROUP BY client_id)"
            ).fetchone()[0]
        return round(avg, 2) if avg is not None else None

    @staticmethod
    def get_average_premium_per_client():
        with get_db_connection() as conn:
            avg = conn.execute(
                "SELECT AVG(total_premium) FROM (SELECT SUM(premium_amount) as total_premium FROM insurance_policies GROUP BY client_id)"
            ).fetchone()[0]
        return round(avg, 2) if avg is not None else None

    @staticmethod
    def get_average_claims_per_client():
        with get_db_connection() as conn:
            avg = conn.execute(
                "SELECT AVG(claim_count) FROM (SELECT COUNT(*) as claim_count FROM claims JOIN insurance_policies ON claims.policy_id = insurance_policies.policy_id GROUP BY insurance_policies.client_id)"
            ).fetchone()[0]
        return round(avg, 2) if avg is not None else None

    @staticmethod
    def get_average_claim_amount_per_client():
        with get_db_connection() as conn:
            avg = conn.execute(
                "SELECT AVG(total_claim) FROM (SELECT SUM(claim_amount) as total_claim FROM claims GROUP BY policy_id)"
            ).fetchone()[0]
        return round(avg, 2) if avg is not None else None

    @staticmethod
    def get_client_with_highest_claim():
        with get_db_connection() as conn:
            client = conn.execute(
                "SELECT clients.client_id, MAX(claims.claim_amount) FROM claims INNER JOIN insurance_policies ON claims.policy_id = insurance_policies.policy_id INNER JOIN clients ON insurance_policies.client_id = clients.client_id GROUP BY clients.client_id ORDER BY MAX(claims.claim_amount) DESC LIMIT 1"
            ).fetchone()
        return client

    @staticmethod
    def get_client_with_highest_premium():
        with get_db_connection() as conn:
            client = conn.execute("""
                SELECT clients.client_id, SUM(insurance_policies.premium_amount) as total_premiums 
                FROM insurance_policies 
                INNER JOIN clients ON insurance_policies.client_id = clients.client_id 
                GROUP BY clients.client_id 
                ORDER BY total_premiums DESC 
                LIMIT 1
            """).fetchone()
            if client:
                client_id = client['client_id']
                total_premiums = round(client['total_premiums'], 2) if client['total_premiums'] is not None else None
                return client_id, total_premiums
        return None

    @staticmethod
    def get_client_with_most_claims():
        with get_db_connection() as conn:
            client = conn.execute(
                "SELECT clients.client_id, COUNT(*) as claim_count FROM claims INNER JOIN insurance_policies ON claims.policy_id = insurance_policies.policy_id INNER JOIN clients ON insurance_policies.client_id = clients.client_id GROUP BY clients.client_id ORDER BY claim_count DESC LIMIT 1").fetchone()
        return client

    @staticmethod
    def get_claim_count_by_status(claim_status):
        with get_db_connection() as conn:
            query = "SELECT COUNT(*) FROM claims WHERE status = ?"
            print(f"SQL Query: {query}, Parameters: ({claim_status},)")
            count = conn.execute(query, (claim_status,)).fetchone()[0]
        return count

    @staticmethod
    def get_claim_count_by_policy_type(policy_type):
        with get_db_connection() as conn:
            claim_count = conn.execute(
                "SELECT COUNT(*) FROM claims INNER JOIN insurance_policies ON claims.policy_id = insurance_policies.policy_id WHERE insurance_policies.policy_type = ?",
                (policy_type,)
            ).fetchone()[0]
        return claim_count

    @staticmethod
    def get_loss_ratio_by_policy_type(policy_type):
        with get_db_connection() as conn:
            # Calculating total claims for the given policy type with 'Paid' status
            total_claims = conn.execute(
                "SELECT SUM(claims.claim_amount) FROM claims INNER JOIN insurance_policies ON claims.policy_id = insurance_policies.policy_id WHERE insurance_policies.policy_type = ? AND claims.status = 'Paid'",
                (policy_type,)
            ).fetchone()[0]

            # Calculating total premiums for the given policy type
            total_premiums = conn.execute(
                "SELECT SUM(insurance_policies.premium_amount) FROM insurance_policies WHERE insurance_policies.policy_type = ?",
                (policy_type,)
            ).fetchone()[0]

            # Checking if total_premiums is not zero to avoid division by zero
            if total_claims is not None and total_premiums is not None and total_premiums > 0:
                loss_ratio = total_claims / total_premiums
            else:
                loss_ratio = 0 
        return loss_ratio

    @staticmethod
    def get_claim_count_by_month():
        with get_db_connection() as conn:
            results = conn.execute("""               
                SELECT strftime('%m', claim_date) AS month, COUNT(*) AS claim_count 
                FROM claims
                WHERE strftime('%Y', claim_date) = strftime('%Y', 'now')
                GROUP BY month
                ORDER BY month
            """).fetchall()
        
        new_claim_count_by_month = [(int(row['month']), row['claim_count']) for row in results]
        return new_claim_count_by_month

    @staticmethod
    def get_all_claims_count_by_month():
        with get_db_connection() as conn:
            results = conn.execute("""               
                SELECT strftime('%m', claim_date) as month, COUNT(*) as claim_count 
                FROM claims
                GROUP BY month"""
            ).fetchall()
        
        new_claim_count_by_month = [(int(row['month']), row['claim_count']) for row in results]
        return new_claim_count_by_month

    @staticmethod
    def get_new_policies_count_by_month():
        with get_db_connection() as conn:
            # Query to get the count of new policies per month for the current year
            results = conn.execute("""
                SELECT strftime('%m', start_date) AS month, COUNT(*) AS policy_count 
                FROM insurance_policies 
                WHERE strftime('%Y', start_date) = strftime('%Y', 'now')
                GROUP BY month
                ORDER BY month
            """).fetchall()

        new_policies_count_by_month = [(int(row['month']), row['policy_count']) for row in results]
        return new_policies_count_by_month

    def get_all_policies_count_by_month():
        with get_db_connection() as conn:
            # Query to get the count of new policies per month from the past to the present
            results = conn.execute("""
                SELECT strftime('%m', start_date) AS month, COUNT(*) AS policy_count 
                FROM insurance_policies 
                GROUP BY month
                ORDER BY month
            """).fetchall()
        # Converting results to a list of tuples
        all_policies_count_by_month = [(int(row['month']), row['policy_count']) for row in results]
        return all_policies_count_by_month

    @staticmethod
    def get_sum_of_claims_for_policy(policy_id):
        with get_db_connection() as conn:
            total_claims = conn.execute(
                "SELECT SUM(claim_amount) FROM claims WHERE policy_id = ? AND status == 'Paid'",
                (policy_id,)
            ).fetchone()[0]
        return total_claims if total_claims is not None else 0


    @staticmethod
    def get_premium_for_policy(policy_id):
        with get_db_connection() as conn:
            result = conn.execute(
                "SELECT premium_amount, start_date, end_date FROM insurance_policies WHERE policy_id = ? AND status == 'Approved'",
                (policy_id,)
            ).fetchone()

        if result is not None:
            return Statistics._calculate_total_premium_for_policy(result)
        return 0

    @staticmethod
    def get_total_premiums():
        with get_db_connection() as conn:
            results = conn.execute(
                "SELECT premium_amount, start_date, end_date FROM insurance_policies WHERE status == 'Approved'"
            ).fetchall()

        total_premium = 0

        for result in results:
            total_premium += Statistics._calculate_total_premium_for_policy(result)

        return round(total_premium, 2)

    @staticmethod
    def _calculate_total_premium_for_policy(result):
        premium = result['premium_amount']
        start_date = datetime.strptime(result['start_date'], "%Y-%m-%d")
        end_date = datetime.strptime(result['end_date'], "%Y-%m-%d")

        # Using the current date to calculate the total active period
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


    @staticmethod
    def get_paid_claim_amount_by_type(policy_type):
        with get_db_connection() as conn:
            total_paid_claims = conn.execute(
                """
                SELECT SUM(claims.claim_amount) 
                FROM claims 
                INNER JOIN insurance_policies 
                ON claims.policy_id = insurance_policies.policy_id 
                WHERE insurance_policies.policy_type = ? AND claims.status = 'Paid'
                """,
                (policy_type,)
            ).fetchone()[0]
        return total_paid_claims if total_paid_claims is not None else 0

    @staticmethod
    def get_sum_of_earned_premiums_by_policy_type(policy_type):
        with get_db_connection() as conn:
            policies = conn.execute(
                "SELECT policy_id FROM insurance_policies WHERE policy_type = ?",
                (policy_type,)
            ).fetchall()

        total_earned_premiums = 0
        # Calculating the earned premium for each policy and sum them up
        for policy in policies:
            policy_id = policy['policy_id']
            total_earned_premiums += Statistics.get_premium_for_policy(policy_id)

        return total_earned_premiums

    @staticmethod
    def get_claims_to_premiums_ratio(policy_type):
        total_paid_claims = Statistics.get_paid_claim_amount_by_type(policy_type)
        total_earned_premiums = Statistics.get_sum_of_earned_premiums_by_policy_type(policy_type)
        print(total_paid_claims)

        if total_earned_premiums == 0:
            return 0
        
        return (total_paid_claims / total_earned_premiums) * 100


    @staticmethod
    def get_active_policy_count_by_type(policy_type):
        with get_db_connection() as conn:
            # Retrieve all policies of the given type
            policies = conn.execute(
                "SELECT start_date, end_date FROM insurance_policies WHERE policy_type = ? AND status == 'Approved'",
                (policy_type,)
            ).fetchall()

        active_policy_count = 0
        current_date = datetime.now()

        for policy in policies:
            start_date = datetime.strptime(policy['start_date'], "%Y-%m-%d")
            end_date = datetime.strptime(policy['end_date'], "%Y-%m-%d")

            # Checking if the policy is currently active
            if start_date < current_date < end_date:
                active_policy_count += 1

        return active_policy_count


    @staticmethod
    def get_expired_policy_count_by_type(policy_type):
        with get_db_connection() as conn:
            # Retrieving all policies of the given type
            policies = conn.execute(
                "SELECT end_date FROM insurance_policies WHERE policy_type = ? AND status == 'Approved'",
                (policy_type,)
            ).fetchall()

        expired_policy_count = 0
        current_date = datetime.now()

        for policy in policies:
            end_date = datetime.strptime(policy['end_date'], "%Y-%m-%d")

            # Checking if the policy is expired
            if current_date > end_date:
                expired_policy_count += 1

        return expired_policy_count

    @staticmethod
    def get_active_policies_count():
        with get_db_connection() as conn:
            current_date = datetime.now().strftime("%Y-%m-%d")
            count = conn.execute(
                """
                SELECT COUNT(*)
                FROM insurance_policies
                WHERE status = 'Approved'
                AND start_date <= ?
                AND end_date >= ?
                """,
                (current_date, current_date)
            ).fetchone()[0]
        return count

    @staticmethod
    def get_expired_policies_count():
        with get_db_connection() as conn:
            current_date = datetime.now().strftime("%Y-%m-%d")
            count = conn.execute(
                """
                SELECT COUNT(*)
                FROM insurance_policies
                WHERE status = 'Approved'
                AND end_date < ?
                """,
                (current_date,)
            ).fetchone()[0]
        return count





        