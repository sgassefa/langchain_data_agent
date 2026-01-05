# SQLite University Database Setup for Local Development
# Creates and populates the University database from Database System Concepts (Silberschatz)
# Reference: https://www.db-book.com/university-lab-dir/sqljs.html

import os
import sqlite3

UNIVERSITY_DB_FILE = "data/university.db"

# University Database Schema DDL
SCHEMA_DDL = """
-- Department table
CREATE TABLE IF NOT EXISTS department (
    dept_name VARCHAR(20) PRIMARY KEY,
    building VARCHAR(15),
    budget NUMERIC(12,2) CHECK (budget > 0)
);

-- Classroom table
CREATE TABLE IF NOT EXISTS classroom (
    building VARCHAR(15),
    room_number VARCHAR(7),
    capacity NUMERIC(4,0),
    PRIMARY KEY (building, room_number)
);

-- Time slot table
CREATE TABLE IF NOT EXISTS time_slot (
    time_slot_id VARCHAR(4),
    day VARCHAR(1),
    start_time TIME,
    end_time TIME,
    PRIMARY KEY (time_slot_id, day, start_time)
);

-- Instructor table
CREATE TABLE IF NOT EXISTS instructor (
    ID VARCHAR(5) PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    dept_name VARCHAR(20),
    salary NUMERIC(8,2) CHECK (salary > 29000),
    FOREIGN KEY (dept_name) REFERENCES department(dept_name) ON DELETE SET NULL
);

-- Student table
CREATE TABLE IF NOT EXISTS student (
    ID VARCHAR(5) PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    dept_name VARCHAR(20),
    tot_cred NUMERIC(3,0) CHECK (tot_cred >= 0),
    FOREIGN KEY (dept_name) REFERENCES department(dept_name) ON DELETE SET NULL
);

-- Course table
CREATE TABLE IF NOT EXISTS course (
    course_id VARCHAR(8) PRIMARY KEY,
    title VARCHAR(50),
    dept_name VARCHAR(20),
    credits NUMERIC(2,0) CHECK (credits > 0),
    FOREIGN KEY (dept_name) REFERENCES department(dept_name) ON DELETE SET NULL
);

-- Section table
CREATE TABLE IF NOT EXISTS section (
    course_id VARCHAR(8),
    sec_id VARCHAR(8),
    semester VARCHAR(6) CHECK (semester IN ('Fall', 'Winter', 'Spring', 'Summer')),
    year NUMERIC(4,0) CHECK (year > 1701 AND year < 2100),
    building VARCHAR(15),
    room_number VARCHAR(7),
    time_slot_id VARCHAR(4),
    PRIMARY KEY (course_id, sec_id, semester, year),
    FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE,
    FOREIGN KEY (building, room_number) REFERENCES classroom(building, room_number) ON DELETE SET NULL
);

-- Teaches table (instructor teaches section)
CREATE TABLE IF NOT EXISTS teaches (
    ID VARCHAR(5),
    course_id VARCHAR(8),
    sec_id VARCHAR(8),
    semester VARCHAR(6),
    year NUMERIC(4,0),
    PRIMARY KEY (ID, course_id, sec_id, semester, year),
    FOREIGN KEY (course_id, sec_id, semester, year) REFERENCES section(course_id, sec_id, semester, year) ON DELETE CASCADE,
    FOREIGN KEY (ID) REFERENCES instructor(ID) ON DELETE CASCADE
);

-- Takes table (student takes section)
CREATE TABLE IF NOT EXISTS takes (
    ID VARCHAR(5),
    course_id VARCHAR(8),
    sec_id VARCHAR(8),
    semester VARCHAR(6),
    year NUMERIC(4,0),
    grade VARCHAR(2),
    PRIMARY KEY (ID, course_id, sec_id, semester, year),
    FOREIGN KEY (course_id, sec_id, semester, year) REFERENCES section(course_id, sec_id, semester, year) ON DELETE CASCADE,
    FOREIGN KEY (ID) REFERENCES student(ID) ON DELETE CASCADE
);

-- Advisor table
CREATE TABLE IF NOT EXISTS advisor (
    s_ID VARCHAR(5) PRIMARY KEY,
    i_ID VARCHAR(5),
    FOREIGN KEY (i_ID) REFERENCES instructor(ID) ON DELETE SET NULL,
    FOREIGN KEY (s_ID) REFERENCES student(ID) ON DELETE CASCADE
);

-- Prereq table
CREATE TABLE IF NOT EXISTS prereq (
    course_id VARCHAR(8),
    prereq_id VARCHAR(8),
    PRIMARY KEY (course_id, prereq_id),
    FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE,
    FOREIGN KEY (prereq_id) REFERENCES course(course_id)
);
"""

# Sample Data - at least 10 records per table
SAMPLE_DATA = """
-- Department data (10 departments)
INSERT INTO department VALUES ('Biology', 'Watson', 90000.00);
INSERT INTO department VALUES ('Comp. Sci.', 'Taylor', 100000.00);
INSERT INTO department VALUES ('Elec. Eng.', 'Taylor', 85000.00);
INSERT INTO department VALUES ('Finance', 'Painter', 120000.00);
INSERT INTO department VALUES ('History', 'Painter', 50000.00);
INSERT INTO department VALUES ('Music', 'Packard', 80000.00);
INSERT INTO department VALUES ('Physics', 'Watson', 70000.00);
INSERT INTO department VALUES ('Psychology', 'Thompson', 65000.00);
INSERT INTO department VALUES ('Mathematics', 'Taylor', 95000.00);
INSERT INTO department VALUES ('Chemistry', 'Watson', 88000.00);

-- Classroom data (12 classrooms)
INSERT INTO classroom VALUES ('Packard', '101', 500);
INSERT INTO classroom VALUES ('Painter', '514', 10);
INSERT INTO classroom VALUES ('Taylor', '3128', 70);
INSERT INTO classroom VALUES ('Watson', '100', 30);
INSERT INTO classroom VALUES ('Watson', '120', 50);
INSERT INTO classroom VALUES ('Taylor', '112', 40);
INSERT INTO classroom VALUES ('Thompson', '201', 25);
INSERT INTO classroom VALUES ('Packard', '301', 100);
INSERT INTO classroom VALUES ('Watson', '200', 60);
INSERT INTO classroom VALUES ('Painter', '201', 35);
INSERT INTO classroom VALUES ('Taylor', '200', 80);
INSERT INTO classroom VALUES ('Thompson', '101', 45);

-- Time slot data (12 time slots)
INSERT INTO time_slot VALUES ('A', 'M', '08:00', '08:50');
INSERT INTO time_slot VALUES ('A', 'W', '08:00', '08:50');
INSERT INTO time_slot VALUES ('A', 'F', '08:00', '08:50');
INSERT INTO time_slot VALUES ('B', 'M', '09:00', '09:50');
INSERT INTO time_slot VALUES ('B', 'W', '09:00', '09:50');
INSERT INTO time_slot VALUES ('B', 'F', '09:00', '09:50');
INSERT INTO time_slot VALUES ('C', 'M', '11:00', '11:50');
INSERT INTO time_slot VALUES ('C', 'W', '11:00', '11:50');
INSERT INTO time_slot VALUES ('C', 'F', '11:00', '11:50');
INSERT INTO time_slot VALUES ('D', 'M', '13:00', '13:50');
INSERT INTO time_slot VALUES ('D', 'W', '13:00', '13:50');
INSERT INTO time_slot VALUES ('E', 'T', '10:30', '11:45');
INSERT INTO time_slot VALUES ('E', 'R', '10:30', '11:45');
INSERT INTO time_slot VALUES ('F', 'T', '14:30', '15:45');
INSERT INTO time_slot VALUES ('F', 'R', '14:30', '15:45');
INSERT INTO time_slot VALUES ('G', 'M', '16:00', '16:50');
INSERT INTO time_slot VALUES ('G', 'W', '16:00', '16:50');
INSERT INTO time_slot VALUES ('H', 'W', '10:00', '12:30');

-- Instructor data (15 instructors)
INSERT INTO instructor VALUES ('10101', 'Srinivasan', 'Comp. Sci.', 65000.00);
INSERT INTO instructor VALUES ('12121', 'Wu', 'Finance', 90000.00);
INSERT INTO instructor VALUES ('15151', 'Mozart', 'Music', 40000.00);
INSERT INTO instructor VALUES ('22222', 'Einstein', 'Physics', 95000.00);
INSERT INTO instructor VALUES ('32343', 'El Said', 'History', 60000.00);
INSERT INTO instructor VALUES ('33456', 'Gold', 'Physics', 87000.00);
INSERT INTO instructor VALUES ('45565', 'Katz', 'Comp. Sci.', 75000.00);
INSERT INTO instructor VALUES ('58583', 'Califieri', 'History', 62000.00);
INSERT INTO instructor VALUES ('76543', 'Singh', 'Finance', 80000.00);
INSERT INTO instructor VALUES ('76766', 'Crick', 'Biology', 72000.00);
INSERT INTO instructor VALUES ('83821', 'Brandt', 'Comp. Sci.', 92000.00);
INSERT INTO instructor VALUES ('98345', 'Kim', 'Elec. Eng.', 80000.00);
INSERT INTO instructor VALUES ('11111', 'Chen', 'Mathematics', 78000.00);
INSERT INTO instructor VALUES ('22233', 'Watson', 'Chemistry', 82000.00);
INSERT INTO instructor VALUES ('33344', 'Adams', 'Psychology', 68000.00);

-- Student data (15 students)
INSERT INTO student VALUES ('00128', 'Zhang', 'Comp. Sci.', 102);
INSERT INTO student VALUES ('12345', 'Shankar', 'Comp. Sci.', 32);
INSERT INTO student VALUES ('19991', 'Brandt', 'History', 80);
INSERT INTO student VALUES ('23121', 'Chavez', 'Finance', 110);
INSERT INTO student VALUES ('44553', 'Peltier', 'Physics', 56);
INSERT INTO student VALUES ('45678', 'Levy', 'Physics', 46);
INSERT INTO student VALUES ('54321', 'Williams', 'Comp. Sci.', 54);
INSERT INTO student VALUES ('55739', 'Sanchez', 'Music', 38);
INSERT INTO student VALUES ('70557', 'Snow', 'Physics', 0);
INSERT INTO student VALUES ('76543', 'Brown', 'Comp. Sci.', 58);
INSERT INTO student VALUES ('76653', 'Aoi', 'Elec. Eng.', 60);
INSERT INTO student VALUES ('98765', 'Bourikas', 'Elec. Eng.', 98);
INSERT INTO student VALUES ('98988', 'Tanaka', 'Biology', 120);
INSERT INTO student VALUES ('11223', 'Miller', 'Mathematics', 45);
INSERT INTO student VALUES ('33445', 'Davis', 'Chemistry', 72);

-- Course data (15 courses)
INSERT INTO course VALUES ('BIO-101', 'Intro. to Biology', 'Biology', 4);
INSERT INTO course VALUES ('BIO-301', 'Genetics', 'Biology', 4);
INSERT INTO course VALUES ('BIO-399', 'Computational Biology', 'Biology', 3);
INSERT INTO course VALUES ('CS-101', 'Intro. to Computer Science', 'Comp. Sci.', 4);
INSERT INTO course VALUES ('CS-190', 'Game Design', 'Comp. Sci.', 4);
INSERT INTO course VALUES ('CS-315', 'Robotics', 'Comp. Sci.', 3);
INSERT INTO course VALUES ('CS-319', 'Image Processing', 'Comp. Sci.', 3);
INSERT INTO course VALUES ('CS-347', 'Database System Concepts', 'Comp. Sci.', 3);
INSERT INTO course VALUES ('EE-181', 'Intro. to Digital Systems', 'Elec. Eng.', 3);
INSERT INTO course VALUES ('FIN-201', 'Investment Banking', 'Finance', 3);
INSERT INTO course VALUES ('HIS-351', 'World History', 'History', 3);
INSERT INTO course VALUES ('MU-199', 'Music Video Production', 'Music', 3);
INSERT INTO course VALUES ('PHY-101', 'Physical Principles', 'Physics', 4);
INSERT INTO course VALUES ('MATH-101', 'Calculus I', 'Mathematics', 4);
INSERT INTO course VALUES ('CHEM-101', 'General Chemistry', 'Chemistry', 4);

-- Section data (20 sections)
INSERT INTO section VALUES ('BIO-101', '1', 'Summer', 2024, 'Watson', '100', 'A');
INSERT INTO section VALUES ('BIO-301', '1', 'Summer', 2024, 'Watson', '120', 'B');
INSERT INTO section VALUES ('CS-101', '1', 'Fall', 2024, 'Taylor', '3128', 'C');
INSERT INTO section VALUES ('CS-101', '2', 'Fall', 2024, 'Taylor', '112', 'D');
INSERT INTO section VALUES ('CS-190', '1', 'Spring', 2024, 'Taylor', '3128', 'A');
INSERT INTO section VALUES ('CS-190', '2', 'Spring', 2024, 'Taylor', '112', 'B');
INSERT INTO section VALUES ('CS-315', '1', 'Spring', 2024, 'Packard', '101', 'C');
INSERT INTO section VALUES ('CS-319', '1', 'Spring', 2024, 'Watson', '100', 'D');
INSERT INTO section VALUES ('CS-319', '2', 'Spring', 2024, 'Taylor', '3128', 'E');
INSERT INTO section VALUES ('CS-347', '1', 'Fall', 2024, 'Taylor', '200', 'F');
INSERT INTO section VALUES ('EE-181', '1', 'Spring', 2024, 'Taylor', '3128', 'G');
INSERT INTO section VALUES ('FIN-201', '1', 'Spring', 2024, 'Painter', '514', 'H');
INSERT INTO section VALUES ('HIS-351', '1', 'Spring', 2024, 'Painter', '201', 'A');
INSERT INTO section VALUES ('MU-199', '1', 'Spring', 2024, 'Packard', '301', 'B');
INSERT INTO section VALUES ('PHY-101', '1', 'Fall', 2024, 'Watson', '200', 'C');
INSERT INTO section VALUES ('MATH-101', '1', 'Fall', 2024, 'Taylor', '112', 'D');
INSERT INTO section VALUES ('CHEM-101', '1', 'Fall', 2024, 'Watson', '100', 'E');
INSERT INTO section VALUES ('CS-101', '1', 'Spring', 2025, 'Taylor', '3128', 'A');
INSERT INTO section VALUES ('CS-347', '1', 'Spring', 2025, 'Taylor', '200', 'B');
INSERT INTO section VALUES ('BIO-101', '1', 'Fall', 2024, 'Watson', '120', 'C');

-- Teaches data (18 records)
INSERT INTO teaches VALUES ('10101', 'CS-101', '1', 'Fall', 2024);
INSERT INTO teaches VALUES ('10101', 'CS-315', '1', 'Spring', 2024);
INSERT INTO teaches VALUES ('10101', 'CS-347', '1', 'Fall', 2024);
INSERT INTO teaches VALUES ('12121', 'FIN-201', '1', 'Spring', 2024);
INSERT INTO teaches VALUES ('15151', 'MU-199', '1', 'Spring', 2024);
INSERT INTO teaches VALUES ('22222', 'PHY-101', '1', 'Fall', 2024);
INSERT INTO teaches VALUES ('32343', 'HIS-351', '1', 'Spring', 2024);
INSERT INTO teaches VALUES ('45565', 'CS-101', '2', 'Fall', 2024);
INSERT INTO teaches VALUES ('45565', 'CS-319', '1', 'Spring', 2024);
INSERT INTO teaches VALUES ('76766', 'BIO-101', '1', 'Summer', 2024);
INSERT INTO teaches VALUES ('76766', 'BIO-301', '1', 'Summer', 2024);
INSERT INTO teaches VALUES ('83821', 'CS-190', '1', 'Spring', 2024);
INSERT INTO teaches VALUES ('83821', 'CS-190', '2', 'Spring', 2024);
INSERT INTO teaches VALUES ('83821', 'CS-319', '2', 'Spring', 2024);
INSERT INTO teaches VALUES ('98345', 'EE-181', '1', 'Spring', 2024);
INSERT INTO teaches VALUES ('11111', 'MATH-101', '1', 'Fall', 2024);
INSERT INTO teaches VALUES ('22233', 'CHEM-101', '1', 'Fall', 2024);
INSERT INTO teaches VALUES ('10101', 'CS-101', '1', 'Spring', 2025);

-- Takes data (25 records)
INSERT INTO takes VALUES ('00128', 'CS-101', '1', 'Fall', 2024, 'A');
INSERT INTO takes VALUES ('00128', 'CS-347', '1', 'Fall', 2024, 'A-');
INSERT INTO takes VALUES ('12345', 'CS-101', '1', 'Fall', 2024, 'C');
INSERT INTO takes VALUES ('12345', 'CS-190', '2', 'Spring', 2024, 'A');
INSERT INTO takes VALUES ('12345', 'CS-315', '1', 'Spring', 2024, 'A');
INSERT INTO takes VALUES ('12345', 'CS-347', '1', 'Fall', 2024, 'A');
INSERT INTO takes VALUES ('19991', 'HIS-351', '1', 'Spring', 2024, 'B');
INSERT INTO takes VALUES ('23121', 'FIN-201', '1', 'Spring', 2024, 'C+');
INSERT INTO takes VALUES ('44553', 'PHY-101', '1', 'Fall', 2024, 'B-');
INSERT INTO takes VALUES ('45678', 'CS-101', '1', 'Fall', 2024, 'F');
INSERT INTO takes VALUES ('45678', 'CS-319', '2', 'Spring', 2024, 'B');
INSERT INTO takes VALUES ('54321', 'CS-101', '2', 'Fall', 2024, 'A-');
INSERT INTO takes VALUES ('54321', 'CS-190', '2', 'Spring', 2024, 'B+');
INSERT INTO takes VALUES ('55739', 'MU-199', '1', 'Spring', 2024, 'A');
INSERT INTO takes VALUES ('76543', 'CS-101', '1', 'Fall', 2024, 'A');
INSERT INTO takes VALUES ('76543', 'CS-319', '2', 'Spring', 2024, 'A');
INSERT INTO takes VALUES ('76653', 'EE-181', '1', 'Spring', 2024, 'C');
INSERT INTO takes VALUES ('98765', 'CS-101', '1', 'Fall', 2024, 'C-');
INSERT INTO takes VALUES ('98765', 'CS-315', '1', 'Spring', 2024, 'B');
INSERT INTO takes VALUES ('98988', 'BIO-101', '1', 'Summer', 2024, 'A');
INSERT INTO takes VALUES ('98988', 'BIO-301', '1', 'Summer', 2024, 'B+');
INSERT INTO takes VALUES ('11223', 'MATH-101', '1', 'Fall', 2024, 'A');
INSERT INTO takes VALUES ('33445', 'CHEM-101', '1', 'Fall', 2024, 'B');
INSERT INTO takes VALUES ('00128', 'CS-315', '1', 'Spring', 2024, 'A');
INSERT INTO takes VALUES ('76653', 'CS-101', '2', 'Fall', 2024, 'B+');

-- Advisor data (15 records)
INSERT INTO advisor VALUES ('00128', '10101');
INSERT INTO advisor VALUES ('12345', '10101');
INSERT INTO advisor VALUES ('23121', '76543');
INSERT INTO advisor VALUES ('44553', '22222');
INSERT INTO advisor VALUES ('45678', '22222');
INSERT INTO advisor VALUES ('54321', '45565');
INSERT INTO advisor VALUES ('55739', '15151');
INSERT INTO advisor VALUES ('70557', '33456');
INSERT INTO advisor VALUES ('76543', '83821');
INSERT INTO advisor VALUES ('76653', '98345');
INSERT INTO advisor VALUES ('98765', '98345');
INSERT INTO advisor VALUES ('98988', '76766');
INSERT INTO advisor VALUES ('19991', '32343');
INSERT INTO advisor VALUES ('11223', '11111');
INSERT INTO advisor VALUES ('33445', '22233');

-- Prereq data (10 prerequisites)
INSERT INTO prereq VALUES ('BIO-301', 'BIO-101');
INSERT INTO prereq VALUES ('BIO-399', 'BIO-101');
INSERT INTO prereq VALUES ('CS-190', 'CS-101');
INSERT INTO prereq VALUES ('CS-315', 'CS-101');
INSERT INTO prereq VALUES ('CS-319', 'CS-101');
INSERT INTO prereq VALUES ('CS-347', 'CS-101');
INSERT INTO prereq VALUES ('EE-181', 'PHY-101');
INSERT INTO prereq VALUES ('CS-315', 'MATH-101');
INSERT INTO prereq VALUES ('CHEM-101', 'MATH-101');
INSERT INTO prereq VALUES ('BIO-399', 'CS-101');
"""


def create_database():
    """Create the University SQLite database"""
    print("🏫 Creating University SQLite database...")
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(UNIVERSITY_DB_FILE), exist_ok=True)
    
    # Remove existing database if present
    if os.path.exists(UNIVERSITY_DB_FILE):
        print(f"   Removing existing database: {UNIVERSITY_DB_FILE}")
        os.remove(UNIVERSITY_DB_FILE)
    
    # Create new database
    conn = sqlite3.connect(UNIVERSITY_DB_FILE)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Create schema
    print("   Creating tables...")
    cursor.executescript(SCHEMA_DDL)
    
    # Insert sample data
    print("   Inserting sample data...")
    cursor.executescript(SAMPLE_DATA)
    
    conn.commit()
    conn.close()
    
    print(f"   ✓ Created: {UNIVERSITY_DB_FILE}")
    return UNIVERSITY_DB_FILE


def verify_database(db_file):
    """Verify the database contents"""
    print("\n✅ Verifying database contents...")
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()
    
    print(f"\n   Found {len(tables)} tables:")
    
    expected_tables = [
        ("department", 10),
        ("classroom", 12),
        ("time_slot", 18),
        ("instructor", 15),
        ("student", 15),
        ("course", 15),
        ("section", 20),
        ("teaches", 18),
        ("takes", 25),
        ("advisor", 15),
        ("prereq", 10),
    ]
    
    for table, expected in expected_tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        status = "✓" if count >= expected else "⚠"
        print(f"   {status} {table}: {count} rows (expected {expected})")
    
    conn.close()
    return True


def show_sample_queries():
    """Display sample queries for students"""
    print("\n" + "=" * 60)
    print("📝 Sample Queries for University Database")
    print("=" * 60)
    
    queries = [
        ("List all instructors and their departments", 
         "SELECT name, dept_name, salary FROM instructor ORDER BY salary DESC;"),
        
        ("Find all Computer Science courses",
         """SELECT course_id, title, credits
FROM course
WHERE dept_name = 'Comp. Sci.'
ORDER BY course_id;"""),
        
        ("Students and their total credits by department",
         """SELECT dept_name, COUNT(*) AS num_students, AVG(tot_cred) AS avg_credits
FROM student
GROUP BY dept_name
ORDER BY avg_credits DESC;"""),
        
        ("Find instructors earning above department average",
         """SELECT i.name, i.dept_name, i.salary
FROM instructor i
WHERE i.salary > (
    SELECT AVG(salary)
    FROM instructor
    WHERE dept_name = i.dept_name
)
ORDER BY i.salary DESC;"""),
        
        ("Course enrollment counts for Fall 2024",
         """SELECT c.course_id, c.title, COUNT(t.ID) AS enrollment
FROM course c
JOIN section s ON c.course_id = s.course_id
LEFT JOIN takes t ON s.course_id = t.course_id 
    AND s.sec_id = t.sec_id 
    AND s.semester = t.semester 
    AND s.year = t.year
WHERE s.semester = 'Fall' AND s.year = 2024
GROUP BY c.course_id, c.title
ORDER BY enrollment DESC;"""),

        ("Find students with their advisors",
         """SELECT s.name AS student, i.name AS advisor, s.dept_name
FROM student s
JOIN advisor a ON s.ID = a.s_ID
JOIN instructor i ON a.i_ID = i.ID
ORDER BY i.name, s.name;"""),

        ("List courses with prerequisites",
         """SELECT c.course_id, c.title, p.prereq_id AS prerequisite
FROM course c
JOIN prereq p ON c.course_id = p.course_id
ORDER BY c.course_id;"""),

        ("Department budget summary",
         """SELECT dept_name, building, budget,
       budget / (SELECT SUM(budget) FROM department) * 100 AS budget_pct
FROM department
ORDER BY budget DESC;"""),
    ]
    
    for title, query in queries:
        print(f"\n-- {title}")
        print(query)


def run_test_query(db_file):
    """Run a test query to demonstrate the database works"""
    print("\n" + "=" * 60)
    print("🔍 Running Test Query")
    print("=" * 60)
    
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    query = """
    SELECT s.name AS Student, c.title AS Course, t.grade
    FROM student s
    JOIN takes t ON s.ID = t.ID
    JOIN course c ON t.course_id = c.course_id
    WHERE t.grade IN ('A', 'A-')
    ORDER BY s.name, c.title
    LIMIT 10;
    """
    
    print("\nQuery: Find students with A grades")
    print("-" * 40)
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(f"{'Student':<15} {'Course':<30} {'Grade':<5}")
    print("-" * 50)
    for row in results:
        print(f"{row[0]:<15} {row[1]:<30} {row[2]:<5}")
    
    conn.close()


def main():
    """Main setup function"""
    print("=" * 60)
    print("🎓 University Database Setup")
    print("   Based on Database System Concepts (Silberschatz)")
    print("=" * 60)
    
    # Create database
    db_file = create_database()
    
    # Verify contents
    verify_database(db_file)
    
    # Run test query
    run_test_query(db_file)
    
    # Show sample queries
    show_sample_queries()
    
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print(f"\n📁 Database file: {db_file}")
    print("\n💡 To use with the data agent, run:")
    print("   data-agent --config src/data_agent/config/university.yaml")
    print("\n📖 Open with DB Browser for SQLite to explore the data")


if __name__ == "__main__":
    main()
