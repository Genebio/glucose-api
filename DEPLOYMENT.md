# Deployment Guide for Glucose Levels API

This document provides instructions for deploying the Glucose Levels API to Render.com, which offers a user-friendly and generous free tier for web applications.

## Deployed Demo

A live demo of this application is available at:
- API Documentation: https://glucose-api.onrender.com/docs
- Health Check: https://glucose-api.onrender.com/health

## Deploying to Render.com

### Method 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub**:
   - Create a new repository on GitHub
   - Initialize Git in your local project: `git init`
   - Add all files: `git add .`
   - Commit changes: `git commit -m "Initial commit"`
   - Add remote: `git remote add origin https://github.com/Genebio/glucose-api.git`
   - Push to GitHub: `git push -u origin main`

2. **Deploy on Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" and select "Blueprint"
   - Connect your GitHub repository
   - Render will detect the `render.yaml` configuration
   - Review settings and click "Apply"

3. **Import sample data**:
   - Once deployed, go to your service in Render dashboard
   - Click the "Shell" tab
   - Run: `cd /app && python scripts/import_data.py`
   - You should see confirmation of imported records

### Method 2: Manual Deployment

1. **Go to Render Dashboard**:
   - Visit [Render.com](https://render.com/) and sign up/login
   - Click "New" and select "Web Service"

2. **Configure Service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
   - **Plan**: Free
   - **Advanced settings**:
     - Add environment variable: `DATABASE_URL=sqlite:///glucose.db`
     - Add disk with mount path: `/app/data` (1GB size)

3. **Deploy and Import Data**:
   - Once deployed, use the Shell to import sample data
   - Run: `cd /app && python scripts/import_data.py`

## Verifying Deployment

After deployment, verify your API is working by:

1. **Check API documentation**: 
   - Visit https://your-app-name.onrender.com/docs
   - Explore available endpoints

2. **Test health endpoint**:
   - Visit https://your-app-name.onrender.com/health
   - Should return: `{"status":"healthy"}`

3. **Query glucose levels**:
   - Visit https://your-app-name.onrender.com/api/v1/levels/?user_id=cccccccc-cccc-cccc-cccc-cccccccccccc
   - Should return a paginated list of glucose readings

## Troubleshooting

If you encounter issues:

1. **Check Logs**: 
   - In the Render dashboard, go to the "Logs" tab
   - Look for any error messages

2. **Database Issues**:
   - Ensure the disk is properly mounted
   - Confirm data was imported: `sqlite3 glucose.db "SELECT COUNT(*) FROM glucose_levels;"`

3. **Resource Limits**:
   - The free tier has limits on usage and may sleep after periods of inactivity
   - First request after inactivity may take a few seconds