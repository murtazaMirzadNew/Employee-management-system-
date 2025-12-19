CREATE USER c##khan1 IDENTIFIED BY 123;
GRANT CONNECT, RESOURCE, CREATE VIEW, CREATE SEQUENCE, CREATE PROCEDURE TO c##khan1;
ALTER USER c##khan1 QUOTA UNLIMITED ON USERS;# app/db.py
import oracledb

# Enable thin mode (no Oracle Client needed)
oracledb.init_oracle_client(lib_dir=None)  # Optional in thin mode; safe to omit
# But to be explicit and future-safe, we can just use thin mode directly:

def get_connection():
    try:
        # Thin mode connection (no tnsnames.ora or Oracle Client required)
        connection = oracledb.connect(
            user="c##khan1",
            password="123",
            dsn="localhost:1521/free"  # Adjust service name if using something other than XE
        )
        return connection
    except oracledb.Error as e:
        print(f"Database connection error: {e}")
        return None