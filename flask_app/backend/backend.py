from fastapi import FastAPI, HTTPException, Depends, Request, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import pymysql
import logging
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

# --- Setup FastAPI app ---
app = FastAPI()

# --- Enable CORS ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  ##the url that is allowed to send request
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Logging setup ---
logging.basicConfig(filename='activity.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# --- Database config ---
DB_CONFIG = {
    "host": "157.32.210.222",
    "user": "root",
    "password": "secret",
    "database": "registration_system",
    "port": 3306,
    "cursorclass": pymysql.cursors.DictCursor
}

# --- Pydantic Models ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr

class CourseEnroll(BaseModel):
    course_id: int

class Course(BaseModel):
    id: int
    title: str
    description: str

class LoginRequest(BaseModel):
    name: str
    email: str

# --- Helpers ---
def get_db():
    conn = pymysql.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()

def get_user_id_from_cookie(request: Request) -> Optional[int]:
    user_id = request.cookies.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="User not logged in")
    return int(user_id)

# --- Routes ---
@app.post("/login")
def login_user(payload: LoginRequest, response: Response, db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute("SELECT id, name, email FROM users WHERE email = %s AND name = %s", (payload.email, payload.name))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        logging.info(f"User {user['email']} logged in.")
        response = RedirectResponse(url="/my-courses", status_code=HTTP_303_SEE_OTHER)
        response.set_cookie(key="user_id", value=str(user["id"]), httponly=True)
        return response

@app.post("/register")
def register_user(user: UserCreate, db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="User already exists")
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (user.name, user.email))
        db.commit()
        logging.info(f"User registered: {user.email}")
        return {"message": "Registration successful"}

@app.get("/my-courses", response_model=List[Course])
def my_courses(request: Request, db=Depends(get_db)):
    user_id = get_user_id_from_cookie(request)
    with db.cursor() as cursor:
        cursor.execute("""
            SELECT c.id, c.title, c.description
            FROM users u
            JOIN courses c ON u.course_id = c.id
            WHERE u.id = %s
        """, (user_id,))
        result = cursor.fetchall()

    return result

@app.get("/courses", response_model=List[Course])
def list_courses(db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM courses")
        return cursor.fetchall()

@app.post("/enroll")
def enroll_course(enroll: CourseEnroll, request: Request, db=Depends(get_db)):
    user_id = get_user_id_from_cookie(request)
    with db.cursor() as cursor:
        # Check if course exists
        cursor.execute("SELECT id FROM courses WHERE id = %s", (enroll.course_id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Course not found")

        # Check if user already enrolled in the same course
        cursor.execute("SELECT course_id FROM users WHERE id = %s", (user_id,))
        current = cursor.fetchone()
        if current and current["course_id"] == enroll.course_id:
            raise HTTPException(status_code=409, detail="Already enrolled in this course")

        # Update user's course_id
        cursor.execute("UPDATE users SET course_id = %s WHERE id = %s", (enroll.course_id, user_id))
        db.commit()
        return {"message": "Enrolled successfully"}

@app.delete("/unenroll")
def unenroll_course(enroll: CourseEnroll, request: Request, db=Depends(get_db)):
    user_id = get_user_id_from_cookie(request)
    with db.cursor() as cursor:
        # Check if user is enrolled in that course
        cursor.execute("SELECT course_id FROM users WHERE id = %s", (user_id,))
        current = cursor.fetchone()
        if not current or current["course_id"] != enroll.course_id:
            raise HTTPException(status_code=404, detail="You are not enrolled in this course")

        # Set course_id to NULL
        cursor.execute("UPDATE users SET course_id = NULL WHERE id = %s", (user_id,))
        db.commit()
        return {"message": "Unenrolled successfully"}


@app.get("/status")
def status_check(db=Depends(get_db)):
    with db.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as users FROM users")
        students = cursor.fetchone()["users"]
        cursor.execute("SELECT COUNT(*) as courses FROM courses")
        courses = cursor.fetchone()["courses"]
    return {
        "status": "OK",
        "students_registered": students,
        "courses_available": courses
    }

@app.get("/health")
def health_check(db=Depends(get_db)):
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT 1")
        return {"status": "ok"}
    except:
        raise HTTPException(status_code=500, detail="Database connection failed")

# --- Run ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:backend_app", port=5000, host="0.0.0.0", reload=True)
