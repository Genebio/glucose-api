#!/bin/bash
set -e

# Configuration
IMAGE_NAME="glucose-api"
IMAGE_TAG="latest"
REGISTRY="${REGISTRY:-}"  # Set this environment variable before running to push to a registry

# Build the Docker image
echo "Building Docker image ${IMAGE_NAME}:${IMAGE_TAG}..."
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

# Push to registry if specified
if [ -n "$REGISTRY" ]; then
    FULL_IMAGE_NAME="${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
    echo "Tagging and pushing image to ${FULL_IMAGE_NAME}..."
    docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${FULL_IMAGE_NAME}
    docker push ${FULL_IMAGE_NAME}
    
    # Update deployment file to use registry image
    sed -i.bak "s|image: ${IMAGE_NAME}:${IMAGE_TAG}|image: ${FULL_IMAGE_NAME}|g" deployment.yaml
    sed -i.bak "s|imagePullPolicy: IfNotPresent|imagePullPolicy: Always|g" deployment.yaml
    rm -f deployment.yaml.bak
fi

# Check if Kubernetes is available
if ! command -v kubectl &> /dev/null; then
    echo "kubectl is not installed. Please install it to deploy to Kubernetes."
    exit 1
fi

# Apply Kubernetes manifests
echo "Deploying to Kubernetes..."
kubectl apply -f deployment.yaml

# Wait for deployment to be ready
echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/glucose-api

# Get service URL
if [ "$(kubectl get service glucose-api-service -o jsonpath='{.spec.type}')" == "LoadBalancer" ]; then
    echo "Waiting for LoadBalancer IP/hostname..."
    while [ -z "$(kubectl get service glucose-api-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}{.status.loadBalancer.ingress[0].hostname}')" ]; do
        sleep 5
    done
    
    # Get the external IP/hostname
    EXTERNAL_IP=$(kubectl get service glucose-api-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    EXTERNAL_HOSTNAME=$(kubectl get service glucose-api-service -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
    
    if [ -n "$EXTERNAL_IP" ]; then
        echo "Service available at: http://${EXTERNAL_IP}"
    elif [ -n "$EXTERNAL_HOSTNAME" ]; then
        echo "Service available at: http://${EXTERNAL_HOSTNAME}"
    fi
else
    echo "Service type is not LoadBalancer. Access may vary based on your Kubernetes setup."
fi

echo "Deployment complete!"

# Initialize data (optional)
read -p "Do you want to import sample data? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Importing sample data..."
    POD_NAME=$(kubectl get pods -l app=glucose-api -o jsonpath="{.items[0].metadata.name}")
    
    # Copy data files to the pod
    echo "Copying data files to the pod..."
    kubectl cp ./data $POD_NAME:/tmp/
    
    # Run the import script
    echo "Running import script..."
    kubectl exec $POD_NAME -- python scripts/import_data.py --data-dir /tmp/data
    
    echo "Data import complete!"
fi