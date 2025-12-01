# Base Image: Python Slim is a good choice for size and security
FROM python:3.9.16-slim

# Set up environment variables for non-buffered output, which is good for logging
ENV PYTHONBUFFERED=1

# Set the working directory for the application code inside the container
WORKDIR /opt/app-root/src

# Copy requirements and install dependencies
# We copy this file first to leverage Docker's build cache
COPY requirements.txt .

# Upgrade pip (optional, but recommended to use a recent version)
RUN pip install --no-cache-dir --upgrade pip

# Install dependencies needed for the application
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root group and user with the standard UID 1001.
# -r creates a system account; -u specifies the UID; -g specifies the primary group.
# Install 'shadow' package if needed for useradd/groupadd on some distros, 
# but generally available on Debian-based slim images.
RUN groupadd -r appuser -g 1001 \
    && useradd -r -u 1001 -g appuser appuser

# Ensure the working directory is owned by the new non-root user
WORKDIR /opt/app-root/src
RUN chown -R appuser:appuser /opt/app-root/src

# Copy the rest of the application source code into the working directory
COPY . .

# Security measure: Drop root privileges for the running application
# Switch to the named user instead of the raw UID for better readability
USER appuser

# Documentation only: Indicates that the container listens on this port
EXPOSE 3000

# Application configuration (Flask specific environment variables)
ENV FLASK_APP=app

# Default command to run the Flask application
# This is usually overridden by the 'command:' instruction in docker-compose.yml
CMD ["flask", "run", "--host=0.0.0.0", "--port=3000"]