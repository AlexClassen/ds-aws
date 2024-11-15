#!/bin/bash

# Configuration
REGION="us-east-1"
ECR_REPO_NAME_GAME="connect-four-game"
ECR_REPO_NAME_MANAGER="connect-four-manager"
ECR_ACCOUNT_ID="381561213897"
ECR_REPO_URI_GAME="${ECR_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ECR_REPO_NAME_GAME}"
ECR_REPO_URI_MANAGER="${ECR_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${ECR_REPO_NAME_MANAGER}"
PLATFORM="linux/amd64"

# Player settings (configurable)
PLAYER1="AI_1"
PLAYER2="AI_2"
PLAYER1_DEPTH=${1:-4}  # Default depth if not provided
PLAYER2_DEPTH=${2:-4}  # Default depth if not provided

# Function to check for errors
check_error() {
    if [ $? -ne 0 ]; then
        echo "Error occurred during the last operation. Exiting."
        exit 1
    fi
}

# Step 1: Log in to AWS ECR
echo "Logging in to AWS ECR..."
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 381561213897.dkr.ecr.us-east-1.amazonaws.com
check_error

# Step 2: Build and push the game image
echo "Building Docker image for game..."
docker build --platform "$PLATFORM" -t "$ECR_REPO_NAME_GAME:latest" -f Dockerfile.game .
check_error
docker tag "$ECR_REPO_NAME_GAME:latest" "$ECR_REPO_URI_GAME:latest"
docker push "$ECR_REPO_URI_GAME:latest"
check_error

# Step 3: Build and push the manager image
echo "Building Docker image for manager..."
docker build --platform "$PLATFORM" -t "$ECR_REPO_NAME_MANAGER:latest" -f Dockerfile.manager .
check_error
docker tag "$ECR_REPO_NAME_MANAGER:latest" "$ECR_REPO_URI_MANAGER:latest"
docker push "$ECR_REPO_URI_MANAGER:latest"
check_error