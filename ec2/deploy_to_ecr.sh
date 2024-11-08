#!/bin/bash

# Variables
ECR_REPO_URI="381561213897.dkr.ecr.us-east-1.amazonaws.com/connect-four-game"
IMAGE_NAME="connect-four-game:latest"
PLAYER1="AI_1"
PLAYER2="AI_2"
PLAYER1_DEPTH=3
PLAYER2_DEPTH=4

# Function to check for errors
check_error() {
    if [ $? -ne 0 ]; then
        echo "Error occurred during the last operation. Exiting."
        exit 1
    fi
}

# Step 1: Build the Docker image for linux/amd64
echo "Building Docker image for linux/amd64..."
docker build --platform linux/amd64 -t $IMAGE_NAME .
check_error

# Step 2: Tag the image
echo "Tagging Docker image..."
docker tag $IMAGE_NAME $ECR_REPO_URI
check_error

# Step 3: Push the image to ECR
echo "Logging into Amazon ECR..."
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 381561213897.dkr.ecr.us-east-1.amazonaws.com
check_error

echo "Pushing Docker image to ECR..."
docker push $ECR_REPO_URI
check_error

echo "Deployed to ECR!"
