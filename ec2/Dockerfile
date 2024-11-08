# Base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy local files to container
COPY game.py common.py /app/

# Install necessary Python packages
RUN pip install numpy boto3

# Command to run game.py with argument placeholders for players and depths
ENTRYPOINT ["python", "game.py"]
