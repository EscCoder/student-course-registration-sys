# Student Course Registration System

This is a simple Python web application developed using **Flask** and deployed on **Google Cloud Platform (GCP)**. The application allows students to register for courses, view available courses, and manage their own registrations.

## 🛠️ Tech Stack

- **Backend**: Python (Flask)
- **Database**: MySQL (Cloud SQL on GCP)
- **Containerization**: Docker (Multi-stage build to reduce image size)

## 📁 Project Structure

- `flask_app/`: Main application directory
- `schema-creator/`: Contains SQL scripts to create the necessary schema in your Cloud SQL instance

> 🔐 The application uses **cookies** to manage user sessions securely.

> 📌 Currently, the database schema models a **one-to-one relationship** between students and courses.

## 🎯 Application Goals

### 1. User Requirements

- Students can view a list of available courses
- Students can register using basic details (name, email)
- Students can register for one or more courses
- Students can view the list of courses they are enrolled in

### 2. Course Management

- Store and manage course details like title and description
- (Optional) Admin functionality to add new courses
- Each course has a unique identifier

### 3. Registration Logic

- Prevent duplicate course registrations for the same student
- Ensure that both student and course exist before registration
- Each student is uniquely identified for course mapping

### 4. Data Handling

- Secure storage of student data
- Support for basic CRUD operations on course and registration data
- Ability to fetch a student's registered courses

### 5. Error Handling & Validation

- Validate inputs (e.g., email format, empty fields)
- Return meaningful success/error messages
- Gracefully reject invalid or duplicate registrations

### 6. Security & Access Control

- Students can only register and view their own courses
- Internal IDs and sensitive data are not exposed unnecessarily

### 7. Performance & Scalability

- Efficient handling of multiple concurrent course registration requests

## 🚀 Getting Started

1. Clone the repository
2. Use `schema-creator` to initialize your Cloud SQL database
3. Build and run the Docker container from the `flask_app` folder
4. Access the application via the browser

---

