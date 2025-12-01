@echo off
echo Starting the multi-service application stack...
docker compose up --build -d
echo All services launched in detached mode. Check logs with 'docker compose logs -f'
pause