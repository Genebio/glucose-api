#!/bin/bash

# Start Minikube if not running
if ! minikube status | grep -q "Running"; then
  echo "Starting Minikube..."
  minikube start
else
  echo "Minikube is already running"
fi

# Set Docker to use Minikube's Docker daemon
eval $(minikube docker-env)

# Build the Docker image
echo "Building Docker image..."
docker build -t glucose-api:latest .

# Apply Kubernetes manifests
echo "Applying Kubernetes manifests..."
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Wait for deployment to be ready
echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/glucose-api

# Get the URL to access the service
echo "Getting service URL..."
minikube service glucose-api-service --url

echo "Deployment complete!"
echo "You can also access the service by running: minikube service glucose-api-service"