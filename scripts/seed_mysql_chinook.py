# Chinook Database Setup Script for Azure MySQL
# Downloads Chinook data and seeds Azure MySQL Flexible Server

import os
import urllib.request
import pymysql
from dotenv import load_dotenv

load_dotenv()

# Azure MySQL connection settings
MYSQL_HOST = os.getenv("MYSQL_HOST", "lis-4230-mysql.mysql.database.azure.com")
MYSQL_USER = os.getenv("MYSQL_USER", "dbadmin")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", os.getenv("AZURE_SQL_PASSWORD"))
MYSQL_DATABASE = "chinook"

# Chinook SQL file URL (MySQL version)
CHINOOK_URL = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_MySql.sql"

def download_chinook_sql():
    """Download the Chinook MySQL script"""
    print("📥 Downloading Chinook database script...")
    sql_file = "chinook_mysql.sql"
    
    if os.path.exists(sql_file):
        print(f"   Using cached {sql_file}")
        with open(sql_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    urllib.request.urlretrieve(CHINOOK_URL, sql_file)
    print(f"   Downloaded {sql_file}")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        return f.read()

def create_database(cursor):
    """Create the Chinook database if it doesn't exist"""
    print("\n🗄️  Creating Chinook database...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
    cursor.execute(f"USE {MYSQL_DATABASE}")
    print(f"   Database '{MYSQL_DATABASE}' ready")

def execute_chinook_script(cursor, sql_content):
    """Execute the Chinook SQL script"""
    print("\n📊 Creating tables and loading data...")
    
    # Split by semicolons and execute each statement
    # Filter out empty statements and comments
    statements = sql_content.split(';')
    
    executed = 0
    errors = 0
    
    for stmt in statements:
        stmt = stmt.strip()
        if not stmt or stmt.startswith('--') or stmt.startswith('/*'):
            continue
        
        try:
            cursor.execute(stmt)
            executed += 1
            if executed % 100 == 0:
                print(f"   Executed {executed} statements...")
        except pymysql.Error as e:
            # Ignore "table already exists" errors
            if e.args[0] != 1050:  # Table already exists
                errors += 1
                if errors <= 5:
                    print(f"   Warning: {e}")
    
    print(f"   Completed: {executed} statements executed, {errors} warnings")

def create_student_users(cursor):
    """Create read-only student accounts"""
    print("\n👥 Creating student accounts...")
    
    for i in range(1, 11):
        username = f"student{i:02d}"
        password = f"Go4RDBMS#{i:02d}!"
        
        try:
            # Drop user if exists (MySQL 5.7+ syntax)
            cursor.execute(f"DROP USER IF EXISTS '{username}'@'%'")
            
            # Create user
            cursor.execute(f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}'")
            
            # Grant SELECT only on Chinook
            cursor.execute(f"GRANT SELECT ON {MYSQL_DATABASE}.* TO '{username}'@'%'")
            
            print(f"   ✓ Created {username}")
        except pymysql.Error as e:
            print(f"   ✗ Error creating {username}: {e}")
    
    cursor.execute("FLUSH PRIVILEGES")
    print("   Privileges flushed")

def verify_data(cursor):
    """Verify the data was loaded correctly"""
    print("\n✅ Verifying data...")
    
    tables = [
        ("Artist", 275),
        ("Album", 347),
        ("Track", 3503),
        ("Genre", 25),
        ("MediaType", 5),
        ("Playlist", 18),
        ("Customer", 59),
        ("Employee", 8),
        ("Invoice", 412),
        ("InvoiceLine", 2240),
    ]
    
    cursor.execute(f"USE {MYSQL_DATABASE}")
    
    all_good = True
    for table, expected_min in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            status = "✓" if count >= expected_min else "⚠"
            if count < expected_min:
                all_good = False
            print(f"   {status} {table}: {count} rows")
        except pymysql.Error as e:
            print(f"   ✗ {table}: Error - {e}")
            all_good = False
    
    return all_good

def main():
    print("=" * 60)
    print("🎵 Chinook Database Setup for Azure MySQL")
    print("=" * 60)
    
    # Connection string info
    print(f"\n📡 Connecting to: {MYSQL_HOST}")
    print(f"   User: {MYSQL_USER}")
    
    try:
        # Connect to MySQL server
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            charset='utf8mb4',
            autocommit=True,
            ssl={'ssl': {'ca': None}}  # Azure requires SSL
        )
        
        cursor = connection.cursor()
        print("   ✓ Connected successfully")
        
        # Download and execute Chinook script
        sql_content = download_chinook_sql()
        create_database(cursor)
        execute_chinook_script(cursor, sql_content)
        
        # Create student accounts
        create_student_users(cursor)
        
        # Verify data
        success = verify_data(cursor)
        
        cursor.close()
        connection.close()
        
        print("\n" + "=" * 60)
        if success:
            print("🎉 Chinook database setup complete!")
            print("\n📋 Connection Details:")
            print(f"   Host: {MYSQL_HOST}")
            print(f"   Database: {MYSQL_DATABASE}")
            print(f"   Admin: {MYSQL_USER}")
            print(f"   Students: student01-student10")
            print("\n🔧 Test connection:")
            print(f"   mysql -h {MYSQL_HOST} -u student01 -p chinook")
        else:
            print("⚠️  Setup completed with warnings. Check the output above.")
        print("=" * 60)
        
    except pymysql.Error as e:
        print(f"\n❌ MySQL Error: {e}")
        print("\nTroubleshooting:")
        print("1. Verify Azure MySQL server is running")
        print("2. Check firewall rules allow your IP")
        print("3. Verify credentials in .env file")
        raise

if __name__ == "__main__":
    main()
