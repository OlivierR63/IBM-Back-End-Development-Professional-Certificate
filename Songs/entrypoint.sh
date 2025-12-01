#!/bin/sh
# This script ensures MongoDB is available before starting the Flask service.

echo "Waiting for MongoDB service to start..."

# Assumes MongoDB is linked in docker-compose under the hostname 'mongodb' 
# and runs on the default port 27017.
# The MONGODB_SERVICE environment variable from README should point to this hostname.

# Loop until a connection is successful via netcat
# The MONGODB_SERVICE and MONGODB_PORT must be defined in docker-compose.yml
while ! nc -z $MONGODB_SERVICE 27017; do
  sleep 1
done

echo "MongoDB is up and running!"

# --- Optional: Data Initialization Step ---
# If your application needs the songs.json data loaded, 
# you would run a Python script here to insert the data.
# For example: python /app/load_initial_data.py

echo "Starting the Flask Songs API..."

# The 'exec "$@"' command replaces the shell process with the application 
# command (CMD), ensuring proper signal handling by Docker.
exec "$@"
