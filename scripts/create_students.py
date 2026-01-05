"""Create student accounts for RDBMS course."""
import pyodbc

SERVER = "lis-4230.database.windows.net"
DATABASE = "ContosoHR"
ADMIN_USER = "dbadmin"
ADMIN_PASS = "goRDBMS@4230"

# Connect to master database to create logins
master_conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE=master;"
    f"UID={ADMIN_USER};"
    f"PWD={ADMIN_PASS};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
)

print("Creating student logins on server...")
conn = pyodbc.connect(master_conn_str, autocommit=True)
cursor = conn.cursor()

students = []
for i in range(1, 11):
    username = f"student{i:02d}"
    # Azure requires: 8+ chars, uppercase, lowercase, number, special char
    password = f"Go4RDBMS#{i:02d}!"
    students.append((username, password))
    try:
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM sys.sql_logins WHERE name = '{username}')
            CREATE LOGIN [{username}] WITH PASSWORD = '{password}'
        """)
        print(f"  Created login: {username}")
    except Exception as e:
        print(f"  Login {username} error: {e}")

cursor.close()
conn.close()

# Connect to ContosoHR to create users and grant permissions
print("\nCreating users in ContosoHR database...")
db_conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={ADMIN_USER};"
    f"PWD={ADMIN_PASS};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
)

conn = pyodbc.connect(db_conn_str, autocommit=True)
cursor = conn.cursor()

for username, password in students:
    try:
        cursor.execute(f"""
            IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = '{username}')
            CREATE USER [{username}] FOR LOGIN [{username}]
        """)
        cursor.execute(f"ALTER ROLE db_datareader ADD MEMBER [{username}]")
        cursor.execute(f"ALTER ROLE db_datawriter ADD MEMBER [{username}]")
        print(f"  Created user: {username} with read/write access")
    except Exception as e:
        print(f"  User {username} error: {e}")

cursor.close()
conn.close()

print("\n" + "=" * 60)
print("STUDENT CREDENTIALS FOR RDBMS COURSE")
print("=" * 60)
print(f"Server:   {SERVER}")
print(f"Database: {DATABASE}")
print("-" * 60)
print(f"{'Username':<12} | {'Password':<20}")
print("-" * 60)
for username, password in students:
    print(f"{username:<12} | {password:<20}")
print("=" * 60)
