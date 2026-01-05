# SQLite Chinook Setup for Local Development
# Downloads and sets up Chinook database for DB Browser for SQLite

import os
import urllib.request
import sqlite3

# Download URL for Chinook SQLite database
CHINOOK_SQLITE_URL = "https://github.com/lerocha/chinook-database/raw/master/ChinookDatabase/DataSources/Chinook_Sqlite.sqlite"
CHINOOK_DB_FILE = "chinook.db"

def download_chinook_sqlite():
    """Download the Chinook SQLite database file"""
    print("📥 Downloading Chinook SQLite database...")
    
    if os.path.exists(CHINOOK_DB_FILE):
        print(f"   Database already exists: {CHINOOK_DB_FILE}")
        response = input("   Overwrite? (y/n): ").strip().lower()
        if response != 'y':
            print("   Using existing database")
            return CHINOOK_DB_FILE
    
    urllib.request.urlretrieve(CHINOOK_SQLITE_URL, CHINOOK_DB_FILE)
    print(f"   ✓ Downloaded: {CHINOOK_DB_FILE}")
    return CHINOOK_DB_FILE

def verify_database(db_file):
    """Verify the database contents"""
    print("\n✅ Verifying database contents...")
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print(f"\n   Found {len(tables)} tables:")
    
    table_counts = [
        ("Album", 347),
        ("Artist", 275),
        ("Customer", 59),
        ("Employee", 8),
        ("Genre", 25),
        ("Invoice", 412),
        ("InvoiceLine", 2240),
        ("MediaType", 5),
        ("Playlist", 18),
        ("PlaylistTrack", 8715),
        ("Track", 3503),
    ]
    
    for table, expected in table_counts:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        status = "✓" if count >= expected else "⚠"
        print(f"   {status} {table}: {count} rows")
    
    conn.close()
    return True

def show_sample_queries():
    """Display sample queries for students"""
    print("\n" + "=" * 60)
    print("📝 Sample Queries for DB Browser for SQLite")
    print("=" * 60)
    
    queries = [
        ("List all artists", 
         "SELECT * FROM Artist LIMIT 10;"),
        
        ("Count tracks by genre",
         """SELECT g.Name AS Genre, COUNT(*) AS TrackCount
FROM Track t
JOIN Genre g ON t.GenreId = g.GenreId
GROUP BY g.GenreId
ORDER BY TrackCount DESC;"""),
        
        ("Top 10 customers by purchases",
         """SELECT c.FirstName || ' ' || c.LastName AS Customer,
       c.Country,
       SUM(i.Total) AS TotalPurchases
FROM Customer c
JOIN Invoice i ON c.CustomerId = i.CustomerId
GROUP BY c.CustomerId
ORDER BY TotalPurchases DESC
LIMIT 10;"""),
        
        ("Albums by artist with track count",
         """SELECT ar.Name AS Artist,
       al.Title AS Album,
       COUNT(t.TrackId) AS Tracks
FROM Artist ar
JOIN Album al ON ar.ArtistId = al.ArtistId
JOIN Track t ON al.AlbumId = t.AlbumId
GROUP BY al.AlbumId
ORDER BY Tracks DESC
LIMIT 10;"""),
        
        ("Revenue by genre",
         """SELECT g.Name AS Genre,
       ROUND(SUM(il.UnitPrice * il.Quantity), 2) AS Revenue
FROM Genre g
JOIN Track t ON g.GenreId = t.GenreId
JOIN InvoiceLine il ON t.TrackId = il.TrackId
GROUP BY g.GenreId
ORDER BY Revenue DESC;"""),
    ]
    
    for title, query in queries:
        print(f"\n-- {title}")
        print(query)

def main():
    print("=" * 60)
    print("🎵 Chinook SQLite Database Setup")
    print("   For use with DB Browser for SQLite")
    print("=" * 60)
    
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    
    # Create data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    
    # Change to data directory
    os.chdir(data_dir)
    print(f"\n📁 Working directory: {os.getcwd()}")
    
    # Download database
    db_file = download_chinook_sqlite()
    
    # Verify contents
    verify_database(db_file)
    
    # Show sample queries
    show_sample_queries()
    
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60)
    print(f"\n📂 Database location:")
    print(f"   {os.path.abspath(db_file)}")
    print("\n🔧 To open in DB Browser for SQLite:")
    print("   1. Open DB Browser for SQLite")
    print("   2. File → Open Database")
    print(f"   3. Navigate to: {os.path.abspath(db_file)}")
    print("\n💡 SQLite vs MySQL Syntax Differences:")
    print("   • Both use LIMIT (not TOP like T-SQL)")
    print("   • String concatenation: || in SQLite, CONCAT() in MySQL")
    print("   • SQLite is more flexible with types")
    print("   • SQLite uses TEXT, MySQL uses VARCHAR(n)")

if __name__ == "__main__":
    main()
