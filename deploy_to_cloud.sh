#!/bin/bash

# Config
PROJECT_ID="rhea-459720"
REGION="us-central1"
SERVICE_ACCOUNT="mailservice-sa@${PROJECT_ID}.iam.gserviceaccount.com"
REPO_NAME="mailservice-repo"
IMAGE_NAME="mailservice-job"
IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}"
SCHEDULER_JOB_NAME="mailservice-schedule-job"

# Check for required tools
for cmd in gcloud docker git; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ $cmd could not be found. Please install it."
        exit 1
    fi
done

echo "✅ Starting deployment of Cloud Run Job: $IMAGE_NAME"

# Set project
gcloud config set project $PROJECT_ID

# Authenticate Docker for Artifact Registry
echo "🔐 Configuring Docker authentication for Artifact Registry..."
gcloud auth configure-docker $REGION-docker.pkg.dev

# Build and push Docker image with amd64 compatibility
echo "🐳 Building and pushing Docker image for linux/amd64..."
docker buildx create --use --name builder > /dev/null 2>&1 || true
docker buildx build --platform linux/amd64 -t $IMAGE_URI --push .

# Deploy to Cloud Run as a job
echo "🚀 Deploying to Cloud Run Job..."
gcloud run jobs deploy $IMAGE_NAME \
  --image=$IMAGE_URI \
  --region=$REGION \
  --project=$PROJECT_ID \
  --service-account=$SERVICE_ACCOUNT \
  --max-retries=1 \
  --memory=512Mi \
  --command=python \
  --args=main.py

# Enable Cloud Scheduler API (safe to call repeatedly)
echo "📡 Ensuring Cloud Scheduler API is enabled..."
gcloud services enable cloudscheduler.googleapis.com

# Define job execution endpoint
EXECUTE_URI="https://${REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/${IMAGE_NAME}:run"

# Schedule job every 15 minutes
echo "📅 Scheduling job to run every 15 minutes via Cloud Scheduler..."
gcloud scheduler jobs delete $SCHEDULER_JOB_NAME --location=$REGION --quiet 2>/dev/null || true
gcloud scheduler jobs create http $SCHEDULER_JOB_NAME \
  --schedule="*/15 * * * *" \
  --uri="$EXECUTE_URI" \
  --http-method=POST \
  --oauth-service-account-email=$SERVICE_ACCOUNT \
  --location=$REGION

echo "✅ Deployment & Scheduling complete!"
echo "⏱️ Job will run every 15 minutes. View it at: https://console.cloud.google.com/run/jobs?project=$PROJECT_ID"
