import subprocess
import os

if __name__ == "__main__":
    # Run FastAPI backend (accessible from other IPs)
    backend = subprocess.Popen([
        "uvicorn", "backend.backend:app", "--host", "0.0.0.0", "--port", "5000", "--reload"
    ])

    # Run Flask frontend (accessible from other IPs)
    os.environ["FLASK_APP"] = "frontend.routes"
    frontend = subprocess.Popen([
        "flask", "run", "--host=0.0.0.0", "--port=8000"
    ])

    backend.wait()
    frontend.wait()
