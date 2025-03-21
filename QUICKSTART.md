# Quick Remote Deployment Guide

This guide provides the quickest way to deploy the Glucose API to a cloud service.

## Deploy to Railway

[Railway](https://railway.app/) is a platform that makes deploying applications extremely simple.

### Steps to deploy:

1. **Create a Railway account**
   - Go to [Railway](https://railway.app/) and sign up with GitHub

2. **Install the Railway CLI**
   ```bash
   npm i -g @railway/cli
   ```

3. **Login to Railway**
   ```bash
   railway login
   ```

4. **Initialize and deploy your project**
   ```bash
   # Inside your project directory
   railway init
   railway up
   ```

5. **Open your deployed application**
   ```bash
   railway open
   ```

6. **Load sample data (optional)**
   ```bash
   # Get the application URL from Railway dashboard
   railway run -s <your-service-name> -- python scripts/import_data.py
   ```

That's it! Your API is now available online with a public URL.

## Deploy to Render

[Render](https://render.com/) is another simple cloud provider with a generous free tier.

### Steps to deploy:

1. **Create a Render account**
   - Go to [Render](https://render.com/) and sign up with GitHub

2. **New Web Service**
   - Click "New +" and select "Web Service"
   - Connect your GitHub repository
   - Use the following settings:
     - **Name**: glucose-api
     - **Environment**: Python
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Create Web Service**
   - Click "Create Web Service"
   - Wait for the deployment to complete (5-10 minutes)

4. **Access your API**
   - Your API will be available at the URL provided by Render

## Accessing Your API

Once deployed, your API will be available at the URL provided by the service.

- **API Documentation**: `https://your-app-url/docs`
- **Health Check**: `https://your-app-url/health`
- **List Glucose Levels**: `https://your-app-url/api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc`