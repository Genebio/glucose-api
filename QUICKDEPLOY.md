# Quick Deploy Guide - Glucose API

This guide provides the simplest way to deploy the Glucose API to a cloud service with SQLite database.

## Option 1: Deploy to Render (Recommended)

[Render](https://render.com/) offers free web services with persistent disk storage, making it perfect for our SQLite-based API.

### Steps:

1. **Create a Render account** 
   - Go to [Render](https://render.com/) and sign up with GitHub

2. **Deploy your service**
   - From the dashboard, click "New +" and select "Web Service"
   - Connect to your GitHub repository
   - Use these settings:
     - **Name**: glucose-api
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - In Advanced settings:
     - Add environment variable: `DATABASE_URL=sqlite:///glucose.db`
     - Add a disk with mount path: `/app/data` (1GB is sufficient)
   - Click "Create Web Service"

3. **Import sample data (after deployment)**
   - Wait for the deployment to complete (5-10 minutes)
   - Go to your service's Shell tab in the Render dashboard
   - Run: `cd /app && python scripts/import_data.py`

Your API will be available at: `https://glucose-api-xxxx.onrender.com`


## Accessing Your API

Once deployed, your API will be available at the URL provided by the service:

- **API Documentation**: `https://your-app-url/docs`
- **Health Check**: `https://your-app-url/health`
- **List Glucose Levels**: `https://your-app-url/api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc`

## Note for Production Use

While SQLite is sufficient for demonstration purposes, consider using a more robust database like PostgreSQL for production workloads with higher concurrency requirements.