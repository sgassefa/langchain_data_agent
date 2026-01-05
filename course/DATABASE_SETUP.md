# Database Setup Guide for LIS 4230
## Setting Up MySQL (Chinook) and PostgreSQL (Pagila)

This guide helps you set up the additional databases for the course.

---

## 🎵 Chinook Database (MySQL)

The Chinook database represents a digital media store, including tables for artists, albums, tracks, customers, and invoices.

### Option 1: Local MySQL Installation

1. **Install MySQL**
   ```powershell
   # Using winget
   winget install Oracle.MySQL
   
   # Or download from https://dev.mysql.com/downloads/installer/
   ```

2. **Download Chinook Database**
   ```powershell
   # Download from GitHub
   Invoke-WebRequest -Uri "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_MySql.sql" -OutFile "chinook_mysql.sql"
   ```

3. **Create Database and Import**
   ```bash
   mysql -u root -p
   ```
   ```sql
   CREATE DATABASE chinook;
   USE chinook;
   SOURCE chinook_mysql.sql;
   ```

4. **Create Course User**
   ```sql
   CREATE USER 'student'@'localhost' IDENTIFIED BY 'Go4RDBMS#Student!';
   GRANT SELECT ON chinook.* TO 'student'@'localhost';
   FLUSH PRIVILEGES;
   ```

### Option 2: Azure Database for MySQL

1. **Create Azure MySQL Flexible Server**
   ```powershell
   az mysql flexible-server create \
     --resource-group lis-4230-rg \
     --name lis-4230-mysql \
     --admin-user dbadmin \
     --admin-password 'goRDBMS4230' \
     --sku-name Standard_B1ms \
     --version 8.0
   ```

2. **Configure Firewall**
   ```powershell
   az mysql flexible-server firewall-rule create \
     --resource-group lis-4230-rg \
     --name lis-4230-mysql \
     --rule-name AllowMyIP \
     --start-ip-address <YOUR-IP> \
     --end-ip-address <YOUR-IP>
   ```

3. **Import Chinook Data**
   ```bash
   mysql -h lis-4230-mysql.mysql.database.azure.com -u dbadmin -p chinook < chinook_mysql.sql
   ```

### Environment Variables
```bash
# Add to .env file
MYSQL_HOST=localhost  # or lis-4230-mysql.mysql.database.azure.com
MYSQL_USER=student
MYSQL_PASSWORD=Go4RDBMS#Student!
```

---

## 🎬 Pagila Database (PostgreSQL)

Pagila is a port of the Sakila database (DVD rental) to PostgreSQL. It's the most popular PostgreSQL sample database.

### Option 1: Local PostgreSQL Installation

1. **Install PostgreSQL**
   ```powershell
   # Using winget
   winget install PostgreSQL.PostgreSQL
   
   # Or download from https://www.postgresql.org/download/
   ```

2. **Download Pagila Database**
   ```powershell
   # Clone the repository
   git clone https://github.com/devrimgunduz/pagila.git
   cd pagila
   ```

3. **Create Database and Import**
   ```bash
   # Connect to PostgreSQL
   psql -U postgres
   ```
   ```sql
   CREATE DATABASE pagila;
   \c pagila
   \i pagila-schema.sql
   \i pagila-data.sql
   ```

4. **Create Course User**
   ```sql
   CREATE USER student WITH PASSWORD 'Go4RDBMS#Student!';
   GRANT CONNECT ON DATABASE pagila TO student;
   GRANT USAGE ON SCHEMA public TO student;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO student;
   ```

### Option 2: Azure Database for PostgreSQL

1. **Create Azure PostgreSQL Flexible Server**
   ```powershell
   az postgres flexible-server create \
     --resource-group lis-4230-rg \
     --name lis-4230-postgres \
     --admin-user dbadmin \
     --admin-password 'goRDBMS4230' \
     --sku-name Standard_B1ms \
     --version 15
   ```

2. **Configure Firewall**
   ```powershell
   az postgres flexible-server firewall-rule create \
     --resource-group lis-4230-rg \
     --name lis-4230-postgres \
     --rule-name AllowMyIP \
     --start-ip-address <YOUR-IP> \
     --end-ip-address <YOUR-IP>
   ```

3. **Import Pagila Data**
   ```bash
   psql -h lis-4230-postgres.postgres.database.azure.com -U dbadmin -d pagila -f pagila-schema.sql
   psql -h lis-4230-postgres.postgres.database.azure.com -U dbadmin -d pagila -f pagila-data.sql
   ```

### Environment Variables
```bash
# Add to .env file
POSTGRES_HOST=localhost  # or lis-4230-postgres.postgres.database.azure.com
POSTGRES_USER=student
POSTGRES_PASSWORD=Go4RDBMS#Student!
```

---

## 🎓 University Database (SQLite)

The University database is based on the classic academic database from "Database System Concepts" by Silberschatz, Korth, and Sudarshan. It includes tables for departments, instructors, students, courses, sections, enrollments, and prerequisites.

**Reference:** [https://www.db-book.com/university-lab-dir/sqljs.html](https://www.db-book.com/university-lab-dir/sqljs.html)

### Setup (Local SQLite)

1. **Run the setup script**
   ```powershell
   cd C:\Users\Shimelis.Assefa\langchain_data_agent
   python scripts/setup_sqlite_university.py
   ```

2. **Verify the database**
   ```powershell
   # The database is created at: data/university.db
   # Open with DB Browser for SQLite to explore
   ```

### Database Schema

| Table | Description | Records |
|-------|-------------|---------|
| `department` | Academic departments with budgets | 10 |
| `instructor` | Faculty members | 15 |
| `student` | Enrolled students | 15 |
| `course` | Course catalog | 15 |
| `section` | Course sections by semester | 20 |
| `teaches` | Instructor-section assignments | 18 |
| `takes` | Student enrollments with grades | 25 |
| `advisor` | Student-advisor relationships | 15 |
| `prereq` | Course prerequisites | 10 |
| `classroom` | Room locations and capacities | 12 |
| `time_slot` | Class meeting times | 18 |

### Sample Queries

```sql
-- Find all Computer Science courses
SELECT course_id, title, credits
FROM course
WHERE dept_name = 'Comp. Sci.';

-- Students with their advisors
SELECT s.name AS student, i.name AS advisor
FROM student s
JOIN advisor a ON s.ID = a.s_ID
JOIN instructor i ON a.i_ID = i.ID;

-- Course enrollment counts for Fall 2024
SELECT c.title, COUNT(t.ID) AS enrollment
FROM course c
JOIN section s ON c.course_id = s.course_id
LEFT JOIN takes t ON s.course_id = t.course_id 
  AND s.sec_id = t.sec_id 
  AND s.semester = t.semester 
  AND s.year = t.year
WHERE s.semester = 'Fall' AND s.year = 2024
GROUP BY c.title
ORDER BY enrollment DESC;
```

### Running with Data Agent

```powershell
# Run the agent with University database config
uv run data-agent query "What courses does Srinivasan teach?" -c university
uv run data-agent query "List students with A grades in Computer Science" -c university
uv run data-agent query "What are the prerequisites for CS-315?" -c university
```

---

## 🔧 Python Dependencies

Install MySQL and PostgreSQL drivers:

```powershell
cd C:\Users\Shimelis.Assefa\langchain_data_agent
uv add pymysql psycopg2-binary
```

---

## 📊 Database Schema Comparisons

### Entity Comparison Across Databases

| Concept | ContosoHR (Azure SQL) | Chinook (MySQL) | Pagila (PostgreSQL) | University (SQLite) |
|---------|----------------------|-----------------|---------------------|---------------------|
| **Primary Entity** | Employee | Track | Film | Student |
| **Categories** | Department | Genre | Category | Department |
| **Transactions** | TimeOffRequest | Invoice | Rental | Takes (enrollment) |
| **Customers** | (internal employees) | Customer | Customer | Student |
| **Hierarchy** | Employee→Manager | Artist→Album→Track | Actor→Film | Instructor→Teaches→Course |
| **Payments** | Salary | InvoiceLine | Payment | Salary |
| **Relationships** | Employee→Department | Track→Album→Artist | Film→Category | Student→Advisor→Instructor |

### SQL Dialect Comparison

| Feature | T-SQL (Azure SQL) | MySQL | PostgreSQL | SQLite |
|---------|-------------------|-------|------------|--------|
| **Row Limit** | `TOP 10` | `LIMIT 10` | `LIMIT 10` | `LIMIT 10` |
| **String Concat** | `+` or `CONCAT()` | `CONCAT()` | `\|\|` | `\|\|` |
| **Current Date** | `GETDATE()` | `NOW()` | `NOW()` or `CURRENT_DATE` | `date('now')` |
| **Date Add** | `DATEADD(day, 7, date)` | `DATE_ADD(date, INTERVAL 7 DAY)` | `date + INTERVAL '7 days'` | `date(date, '+7 days')` |
| **Identity** | `IDENTITY(1,1)` | `AUTO_INCREMENT` | `SERIAL` or `GENERATED` | `INTEGER PRIMARY KEY` |
| **Boolean** | `BIT` | `BOOLEAN` or `TINYINT(1)` | `BOOLEAN` | `INTEGER (0/1)` |
| **Case Sensitive** | No (by default) | No (by default) | Yes (for identifiers) | No (by default) |

---

## ✅ Verification Queries

### Test ContosoHR (Azure SQL)
```sql
SELECT COUNT(*) AS EmployeeCount FROM dbo.Employees;
-- Expected: 40
```

### Test Chinook (MySQL)
```sql
SELECT COUNT(*) AS TrackCount FROM Track;
-- Expected: 3503
```

### Test Pagila (PostgreSQL)
```sql
SELECT COUNT(*) AS FilmCount FROM public.film;
-- Expected: 1000
```

### Test University (SQLite)
```sql
SELECT COUNT(*) AS StudentCount FROM student;
-- Expected: 15

SELECT COUNT(*) AS CourseCount FROM course;
-- Expected: 15

SELECT COUNT(*) AS InstructorCount FROM instructor;
-- Expected: 15
```

---

## 🚀 Running the Multi-Database Agent

Once all databases are set up:

```powershell
# Set environment variables
$env:OPENAI_API_KEY = "your-key"
$env:MYSQL_HOST = "localhost"
$env:MYSQL_USER = "student"
$env:POSTGRES_HOST = "localhost"
$env:POSTGRES_USER = "student"

# Run with multi-database config
uv run data-agent query "Who are the top selling artists?" -c multi_database
uv run data-agent query "What is the average salary by department?" -c multi_database
uv run data-agent query "What are the most rented films?" -c multi_database

# Run with University database (SQLite - no additional setup needed)
uv run data-agent query "List all Computer Science courses" -c university
uv run data-agent query "Who teaches Database System Concepts?" -c university
uv run data-agent query "What students got an A in Fall 2024?" -c university
```

The agent will automatically route questions to the appropriate database!
