# Alternative Chinook MySQL Setup - Direct SQL execution
# Uses subprocess to run mysql command directly

import os
import urllib.request
import subprocess
import tempfile
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST", "lis4230mysql.mysql.database.azure.com")
MYSQL_USER = os.getenv("MYSQL_USER", "dbadmin")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", os.getenv("AZURE_SQL_PASSWORD"))

def download_chinook():
    """Download Chinook SQL script"""
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_MySql.sql"
    local_file = "chinook_mysql.sql"
    
    if not os.path.exists(local_file):
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, local_file)
    
    return local_file

def fix_sql_for_mysql8(sql_content):
    """Fix compatibility issues with MySQL 8.4"""
    # Remove the N prefix from strings (MySQL Unicode prefix not needed in 8.x)
    # Replace N'string' with 'string'
    import re
    
    # Fix N'...' patterns
    fixed = re.sub(r"N'([^']*)'", r"'\1'", sql_content)
    
    # Fix any encoding issues
    fixed = fixed.replace("''", "'")  # Unescape quotes properly
    
    return fixed

def create_chinook_manually():
    """Create Chinook database with manual SQL"""
    import pymysql
    
    print("Connecting to MySQL...")
    conn = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        charset='utf8mb4',
        autocommit=True,
        ssl={'ssl': {}}
    )
    cursor = conn.cursor()
    
    # Create database
    cursor.execute("DROP DATABASE IF EXISTS chinook")
    cursor.execute("CREATE DATABASE chinook CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    cursor.execute("USE chinook")
    print("Created database 'chinook'")
    
    # Create tables
    tables = """
    -- Artists
    CREATE TABLE Artist (
        ArtistId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(120)
    );
    
    -- Albums  
    CREATE TABLE Album (
        AlbumId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Title VARCHAR(160) NOT NULL,
        ArtistId INT NOT NULL,
        FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId)
    );
    
    -- MediaType
    CREATE TABLE MediaType (
        MediaTypeId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(120)
    );
    
    -- Genre
    CREATE TABLE Genre (
        GenreId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(120)
    );
    
    -- Track
    CREATE TABLE Track (
        TrackId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(200) NOT NULL,
        AlbumId INT,
        MediaTypeId INT NOT NULL,
        GenreId INT,
        Composer VARCHAR(220),
        Milliseconds INT NOT NULL,
        Bytes INT,
        UnitPrice DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (AlbumId) REFERENCES Album(AlbumId),
        FOREIGN KEY (MediaTypeId) REFERENCES MediaType(MediaTypeId),
        FOREIGN KEY (GenreId) REFERENCES Genre(GenreId)
    );
    
    -- Playlist
    CREATE TABLE Playlist (
        PlaylistId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Name VARCHAR(120)
    );
    
    -- PlaylistTrack
    CREATE TABLE PlaylistTrack (
        PlaylistId INT NOT NULL,
        TrackId INT NOT NULL,
        PRIMARY KEY (PlaylistId, TrackId),
        FOREIGN KEY (PlaylistId) REFERENCES Playlist(PlaylistId),
        FOREIGN KEY (TrackId) REFERENCES Track(TrackId)
    );
    
    -- Employee
    CREATE TABLE Employee (
        EmployeeId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        LastName VARCHAR(20) NOT NULL,
        FirstName VARCHAR(20) NOT NULL,
        Title VARCHAR(30),
        ReportsTo INT,
        BirthDate DATETIME,
        HireDate DATETIME,
        Address VARCHAR(70),
        City VARCHAR(40),
        State VARCHAR(40),
        Country VARCHAR(40),
        PostalCode VARCHAR(10),
        Phone VARCHAR(24),
        Fax VARCHAR(24),
        Email VARCHAR(60),
        FOREIGN KEY (ReportsTo) REFERENCES Employee(EmployeeId)
    );
    
    -- Customer
    CREATE TABLE Customer (
        CustomerId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        FirstName VARCHAR(40) NOT NULL,
        LastName VARCHAR(20) NOT NULL,
        Company VARCHAR(80),
        Address VARCHAR(70),
        City VARCHAR(40),
        State VARCHAR(40),
        Country VARCHAR(40),
        PostalCode VARCHAR(10),
        Phone VARCHAR(24),
        Fax VARCHAR(24),
        Email VARCHAR(60) NOT NULL,
        SupportRepId INT,
        FOREIGN KEY (SupportRepId) REFERENCES Employee(EmployeeId)
    );
    
    -- Invoice
    CREATE TABLE Invoice (
        InvoiceId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        CustomerId INT NOT NULL,
        InvoiceDate DATETIME NOT NULL,
        BillingAddress VARCHAR(70),
        BillingCity VARCHAR(40),
        BillingState VARCHAR(40),
        BillingCountry VARCHAR(40),
        BillingPostalCode VARCHAR(10),
        Total DECIMAL(10,2) NOT NULL,
        FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId)
    );
    
    -- InvoiceLine
    CREATE TABLE InvoiceLine (
        InvoiceLineId INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        InvoiceId INT NOT NULL,
        TrackId INT NOT NULL,
        UnitPrice DECIMAL(10,2) NOT NULL,
        Quantity INT NOT NULL,
        FOREIGN KEY (InvoiceId) REFERENCES Invoice(InvoiceId),
        FOREIGN KEY (TrackId) REFERENCES Track(TrackId)
    );
    """
    
    for stmt in tables.split(';'):
        stmt = stmt.strip()
        if stmt and not stmt.startswith('--'):
            cursor.execute(stmt)
    print("Created tables")
    
    # Load data from SQLite
    import sqlite3
    sqlite_db = os.path.join(os.path.dirname(__file__), "..", "data", "chinook.db")
    
    if not os.path.exists(sqlite_db):
        print(f"SQLite database not found at {sqlite_db}")
        print("Please run setup_sqlite_chinook.py first")
        return
    
    print(f"Loading data from SQLite: {sqlite_db}")
    sqlite_conn = sqlite3.connect(sqlite_db)
    sqlite_cursor = sqlite_conn.cursor()
    
    # Tables to migrate (in order due to foreign keys)
    table_order = [
        'Artist', 'Album', 'MediaType', 'Genre', 'Track', 
        'Playlist', 'PlaylistTrack', 'Employee', 'Customer', 
        'Invoice', 'InvoiceLine'
    ]
    
    for table in table_order:
        print(f"  Loading {table}...", end=" ")
        
        # Get data from SQLite
        sqlite_cursor.execute(f"SELECT * FROM {table}")
        rows = sqlite_cursor.fetchall()
        
        if not rows:
            print("0 rows")
            continue
        
        # Get column count
        sqlite_cursor.execute(f"PRAGMA table_info({table})")
        columns = len(sqlite_cursor.fetchall())
        
        # Insert into MySQL
        placeholders = ", ".join(["%s"] * columns)
        insert_sql = f"INSERT INTO {table} VALUES ({placeholders})"
        
        try:
            cursor.executemany(insert_sql, rows)
            print(f"{len(rows)} rows")
        except Exception as e:
            print(f"Error: {e}")
    
    sqlite_conn.close()
    
    # Create student users
    print("\nCreating student accounts...")
    for i in range(1, 11):
        username = f"student{i:02d}"
        password = f"Go4RDBMS#{i:02d}!"
        try:
            cursor.execute(f"DROP USER IF EXISTS '{username}'@'%'")
            cursor.execute(f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}'")
            cursor.execute(f"GRANT SELECT ON chinook.* TO '{username}'@'%'")
            print(f"  ✓ {username}")
        except Exception as e:
            print(f"  ✗ {username}: {e}")
    cursor.execute("FLUSH PRIVILEGES")
    
    # Verify
    print("\nVerification:")
    for table in table_order:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count} rows")
    
    cursor.close()
    conn.close()
    
    print("\n✅ Chinook database setup complete!")
    print(f"   Host: {MYSQL_HOST}")
    print(f"   Database: chinook")

if __name__ == "__main__":
    create_chinook_manually()
