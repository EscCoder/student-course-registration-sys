import pymysql

# Database connection settings - update these for your environment
DB_CONFIG = {
    "host": "35.200.243.177",
    "user": "pallavi",
    "password": "password",
    "port": 3306,
    "database": "registration_system"
}

# Step 1: Create the database if it doesn't exist
with pymysql.connect(
    host=DB_CONFIG["host"],
    user=DB_CONFIG["user"],
    password=DB_CONFIG["password"],
    port=DB_CONFIG["port"]
) as conn:
    with conn.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        conn.commit()

# Step 2: Connect to the database and create tables
with pymysql.connect(**DB_CONFIG) as conn:
    with conn.cursor() as cursor:
        # Create `courses` table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description TEXT
        )
        """)

        # Create `users` table with foreign key to `courses`
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            course_id INT,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE SET NULL
        )
        """)

        conn.commit()
        print("Database and tables for 'registration_system' created successfully!")

# import pymysql

# # Database connection settings
# DB_CONFIG = {
#     "host": "35.200.243.177",
#     "user": "pallavi",
#     "password": "password",
#     "port": 3306,
#     "database": "registration_system"
# }

# # Courses to insert
# courses = [
#     ("OOPs", "Learn object-oriented programming basics"),
#     ("Networks", "Introduction to computer networking"),
#     ("Database System", "Core principles of database design"),
#     ("Comp Architecture", "Study of computer internal structure")
# ]

# # Connect and insert courses
# with pymysql.connect(**DB_CONFIG) as conn:
#     with conn.cursor() as cursor:
#         for title, desc in courses:
#             cursor.execute("INSERT INTO courses (title, description) VALUES (%s, %s)", (title, desc))
#         conn.commit()
#         print("Courses inserted successfully!")
