from flask import Flask, render_template, request, redirect, url_for, session
import requests
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
CORS(app)
app.secret_key = "your_secret_key"
app.permanent_session_lifetime = timedelta(minutes=5)

API_BASE_URL = "http://localhost:5000"
client = requests.Session()  # to persist cookies

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        payload = {
            "name": request.form["name"],
            "email": request.form["email"]
        }
        res = client.post(f"{API_BASE_URL}/register", json=payload)
        if res.status_code == 200:
            return redirect(url_for("login"))
        return f"Error: {res.json().get('detail', 'Registration failed')}"
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        payload = {
            "name": request.form["name"],
            "email": request.form["email"]
        }
        res = client.post(f"{API_BASE_URL}/login", json=payload, allow_redirects=False)
        if res.status_code in [200, 303]:
            return redirect(url_for("dashboard"))
        return redirect(url_for("login", error="Invalid credentials"))
    return render_template("login.html", error=request.args.get("error"))

@app.route("/dashboard")
def dashboard():
    res = client.get(f"{API_BASE_URL}/my-courses")
    if res.status_code == 401:
        return redirect(url_for("login"))
    courses = res.json()
    return render_template("dashboard.html", courses=courses)

@app.route("/courses")
def courses():
    res = client.get(f"{API_BASE_URL}/courses")
    if res.status_code == 401:
        return redirect(url_for("login"))
    return render_template("courses.html", courses=res.json())

@app.route("/logout")
def logout():
    session.clear()
    client.cookies.clear()  # Clear session cookies too
    return redirect(url_for("login"))

@app.route("/enroll", methods=["POST"])
def enroll():
    course_id = request.form.get("course_id")
    res = client.post(f"{API_BASE_URL}/enroll", json={"course_id": course_id})
    if res.status_code == 200:
        return redirect(url_for("dashboard"))
    return f"Enrollment failed: {res.json().get('detail')}"

@app.route("/unenroll", methods=["POST"])
def unenroll():
    course_id = request.form.get("course_id")
    res = client.delete(f"{API_BASE_URL}/unenroll", json={"course_id": course_id})
    if res.status_code == 200:
        return redirect(url_for("dashboard"))
    return f"Unenrollment failed: {res.json().get('detail', 'Unknown error')}"

if __name__ == "__main__":
    app.run(debug=True, port=8000)
