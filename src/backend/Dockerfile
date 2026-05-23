# src/backend/Dockerfile

# 1. Use the official lightweight Python image
FROM python:3.11-slim

# 2. Set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory in the container
WORKDIR /app

# 4. Install system dependencies required for building certain Python packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# 6. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy the rest of the backend application code into the container
COPY . .

# 8. Expose the port the app runs on
EXPOSE 8000

# 9. Command to run the application (bind to 0.0.0.0 to be accessible from outside the container)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]