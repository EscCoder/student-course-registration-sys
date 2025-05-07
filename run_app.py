import subprocess
import os

if __name__ == "__main__":
    # Run FastAPI backend
    backend = subprocess.Popen(["uvicorn", "backend.backend:app", "--port", "5000", "--reload"])

    # Run Flask frontend
    os.environ["FLASK_APP"] = "frontend.routes"
    frontend = subprocess.Popen(["flask", "run", "--port", "8000"])

    # Wait for both
    backend.wait()
    frontend.wait()
