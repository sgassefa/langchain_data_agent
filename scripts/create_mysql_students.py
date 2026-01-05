#!/usr/bin/env python
"""Create student accounts for MySQL Chinook database"""
import pymysql

conn = pymysql.connect(
    host='lis4230mysql.mysql.database.azure.com',
    user='dbadmin',
    password='goRDBMS4230',
    database='chinook',
    charset='utf8mb4',
    autocommit=True,
    ssl={'ssl': {}}
)
cursor = conn.cursor()

print('Creating student accounts...')
for i in range(1, 11):
    username = f'student{i:02d}'
    password = f'Go4RDBMS#{i:02d}!'
    
    # Drop if exists
    try:
        cursor.execute(f"DROP USER IF EXISTS '{username}'@'%%'")
    except:
        pass
    
    # Create user and grant permissions
    try:
        cursor.execute(f"CREATE USER '{username}'@'%%' IDENTIFIED BY '{password}'")
        cursor.execute(f"GRANT SELECT ON chinook.* TO '{username}'@'%%'")
        print(f'  ✓ {username}')
    except Exception as e:
        print(f'  x {username}: {e}')

cursor.execute('FLUSH PRIVILEGES')
conn.close()
print('\n✓ Student accounts created!')
