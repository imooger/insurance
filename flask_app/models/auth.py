from werkzeug.security import generate_password_hash, check_password_hash
from flask import session, request
from . import get_db_connection


class User:
    @staticmethod
    def login(email, password):
        with get_db_connection() as conn:
            cursor = conn.execute(
                """
                SELECT users.id, users.email, users.role, clients.first_name, clients.last_name, clients.photo, users.password 
                FROM users 
                JOIN clients ON users.email = clients.email 
                WHERE users.email = ?
                """,
                (email,)
            )
            row = cursor.fetchone()

            if not row or not check_password_hash(row["password"], password):
                return None

            session.clear()
            session["user_id"] = row["id"]
            session["role"] = row["role"]
            session["email"] = row["email"]
            session["first_name"] = row["first_name"]
            session["last_name"] = row["last_name"]
            session["photo"] = row["photo"]
            return row

    @staticmethod
    def register(
        email,
        password,
        first_name=None,
        last_name=None,
        date_of_birth=None,
        phone=None,
        street=None,
        city=None,
        state=None,
        zip=None,
        photo=None,
        set_session=True,
    ):
        conn = get_db_connection()

        try:
            # Validate input
            if not email or not password:
                return "Email and password are required", None

            confirmation = request.form.get("confirmation")
            if password != confirmation:
                return "Passwords don't match", None

            cursor = conn.execute("SELECT * FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                return "Email already exists", None

            hashed_pass = generate_password_hash(password)
            conn.execute(
                "INSERT INTO users (email, password, role) VALUES (?, ?, ?)",
                (email, hashed_pass, "insured"),
            )
            # Loading into clients
            conn.execute(
                """
                INSERT INTO clients (first_name, last_name, date_of_birth, email, phone, street, city, state, zip, photo) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (first_name, last_name, date_of_birth, email, phone, street, city, state, zip, photo)
            )
            conn.commit()

            # Fetching (joining on email) user data after registration for session
            cursor = conn.execute(
                """
                SELECT users.id, users.email, users.role, clients.first_name, clients.last_name, clients.photo 
                FROM users 
                JOIN clients ON users.email = clients.email 
                WHERE users.email = ?
                """,
                (email,)
            )
            user_data = cursor.fetchone()

            if set_session:
                session.clear()
                session["user_id"] = user_data["id"]
                session["role"] = user_data["role"]
                session["email"] = user_data["email"]
                session["first_name"] = user_data["first_name"]
                session["last_name"] = user_data["last_name"]
                session["photo"] = user_data["photo"]

            return None, user_data["id"]
        finally:
            conn.close()

    

    @staticmethod
    def get_user_by_email(email):
        with get_db_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM Users WHERE email = ?", (email,)
            )
            user = cursor.fetchone()
        return user

    @staticmethod
    def update_email(user_id, new_email):
        conn = get_db_connection()
        conn.execute(
            "UPDATE Users SET email = ? WHERE id = ?",
            (new_email, user_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete_user_by_email(email):
        conn = get_db_connection()
        conn.execute(
            "DELETE FROM Users WHERE email = ?", (email,)
        )
        conn.commit()
        conn.close()


    @staticmethod
    def logout():
        # No need for database interaction in logout, just clear session
        session.clear()
