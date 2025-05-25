# Stage 1: Frontend build
FROM python:3.9-slim AS frontend
WORKDIR /app/frontend
COPY frontend/templates /app/frontend/templates
COPY frontend/routes.py /app/frontend/

# Stage 2: Backend build
FROM python:3.9-slim AS backend
WORKDIR /app/backend
COPY backend/backend.py /app/backend/

# Stage 3: Build dependencies for runtime
FROM python:3.9-slim AS builder
WORKDIR /app
COPY requirements.txt /app/

# When you add --no-cache-dir, pip will not store any downloaded package files or metadata in the cache.
RUN pip install --user --no-cache-dir -r /app/requirements.txt
# --user (When you run pip install --user, Python installs packages into /root/.local 
# instead of the system-wide /usr/local/lib/...)
# So this line copies only the user-installed Python packages, -it
# not the whole Python environment 

# Final image
FROM python:3.9-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
# Add /root/.local/bin to the beginning of the PATH, so executables installed by pip can be run directly

COPY --from=frontend /app/frontend/ /app/frontend/
COPY --from=backend /app/backend/ /app/backend/
COPY run_app.py /app/

EXPOSE 5000
EXPOSE 8000

CMD ["python", "run_app.py"]
