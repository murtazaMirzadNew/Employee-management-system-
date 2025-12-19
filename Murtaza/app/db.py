# app/db.py
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
            dsn="localhost:1521/orcldb"  # Adjust service name if using something other than XE
        )
        print("done")
        return connection
    except oracledb.Error as e:
        print(f"Database connection error: {e}")
        return None
    