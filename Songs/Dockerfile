# Base Image: Use Python Slim for a small, secure environment
FROM python:3.9.16-slim

# Set environment variables for non-buffered output for real-time logging
ENV PYTHONBUFFERED=1

# Install netcat, required for the entrypoint.sh wait-for-it loop ---
RUN apt-get update \
    && apt-get install -y netcat \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory for the application code
WORKDIR /app

# Copy requirements file first to utilize build caching
COPY requirements.txt .

# Install dependencies needed for the application.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root group and user (appuser, UID 1001)
RUN groupadd -r appuser -g 1001 \
    && useradd -r -u 1001 -g appuser appuser

# Copy the rest of the application source code into the working directory
COPY . /app

# Set execution permission for the entrypoint script as root (MUST succeed here)
RUN chmod +x /app/entrypoint.sh

# Change ownership of all application files to the non-root user (appuser)
RUN chown -R appuser:appuser /app 

# Documentation: Port the application listens on
EXPOSE 8000

# Security measure: Drop root privileges for the running application
USER appuser

# Set the entrypoint script to handle initial database setup (e.g., waiting for MongoDB)
ENTRYPOINT ["/app/entrypoint.sh"]

# Command to run the Flask application
CMD ["python", "app.py", "--host=0.0.0.0", "--port=8000"]
