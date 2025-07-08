# Railway Deployment Guide

This guide will help you deploy the Enhanced Internal Linking API to Railway from scratch.

## Prerequisites

1. **GitHub Account**: You need a GitHub account to connect your repository
2. **Railway Account**: Sign up at [railway.app](https://railway.app) with your GitHub account
3. **Repository**: Your code should be in a GitHub repository

## Step 1: Prepare Your Repository

Your repository should contain these essential files:

- `api_internal_linking.py` - Main FastAPI application
- `enhanced_internal_linking.py` - Core linking logic
- `glossary_terms.json` - Glossary data
- `requirements.txt` - Python dependencies
- `railway_start.py` - Startup script
- `nixpacks.toml` - Railway build configuration
- `Procfile` - Alternative deployment configuration
- `railway.json` - Railway-specific configuration

## Step 2: Deploy to Railway

### Option A: Deploy via Railway Dashboard (Recommended)

1. **Go to Railway Dashboard**
   - Visit [railway.app](https://railway.app)
   - Sign in with your GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Deployment**
   - Railway will automatically detect Python
   - The build will use the `nixpacks.toml` configuration
   - No additional environment variables needed

4. **Deploy**
   - Railway will automatically build and deploy your application
   - The build process will:
     - Install Python dependencies from `requirements.txt`
     - Download spaCy model (`en_core_web_sm`)
     - Start the application using `railway_start.py`

### Option B: Deploy via Railway CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize Project**
   ```bash
   railway init
   ```

4. **Deploy**
   ```bash
   railway up
   ```

## Step 3: Verify Deployment

Once deployed, your API will be available at:
`https://your-app-name.railway.app`

### Test Endpoints

1. **Health Check**: `GET /health`
   ```bash
   curl https://your-app-name.railway.app/health
   ```

2. **API Documentation**: `GET /docs`
   - Visit `https://your-app-name.railway.app/docs` in your browser

3. **Root Endpoint**: `GET /`
   ```bash
   curl https://your-app-name.railway.app/
   ```

4. **Statistics**: `GET /stats`
   ```bash
   curl https://your-app-name.railway.app/stats
   ```

## Step 4: Test the API

### Process Article Content

```bash
curl -X POST "https://your-app-name.railway.app/process" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "<p>This is a test article about ETFs and mutual funds.</p>",
    "max_links": 5
  }'
```

### Upload and Process File

```bash
curl -X POST "https://your-app-name.railway.app/upload" \
  -F "file=@your-article.html" \
  -F "max_links=5"
```

## Configuration Files Explained

### `railway_start.py`
- Downloads spaCy model on startup
- Configures port from environment variable
- Starts uvicorn server

### `nixpacks.toml`
- Specifies Python 3.9
- Installs dependencies from `requirements.txt`
- Sets start command

### `railway.json`
- Configures health check endpoint
- Sets restart policy
- Specifies build method

### `Procfile`
- Alternative deployment configuration
- Specifies web process

## Environment Variables

Railway automatically sets:
- `PORT`: The port your application should listen on
- `RAILWAY_STATIC_URL`: Your application's public URL

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` for missing dependencies
   - Ensure all files are committed to GitHub

2. **Application Won't Start**
   - Check logs in Railway dashboard
   - Verify `railway_start.py` is executable

3. **spaCy Model Issues**
   - The startup script handles model downloading
   - Check logs for download errors

4. **Port Issues**
   - Railway automatically sets the PORT environment variable
   - The startup script uses this port

### Viewing Logs

1. Go to your Railway project dashboard
2. Click on your service
3. Go to the "Deployments" tab
4. Click on a deployment to view logs

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation
- `GET /stats` - Glossary statistics
- `GET /categories` - Available categories
- `GET /terms/{category}` - Terms by category
- `POST /process` - Process article content
- `POST /upload` - Upload and process file
- `POST /analyze` - Analyze article without linking

## Monitoring

Railway provides:
- Automatic health checks
- Deployment logs
- Performance metrics
- Automatic restarts on failure

## Scaling

Railway automatically scales based on traffic. You can also:
- Set custom scaling rules
- Configure resource limits
- Set up monitoring alerts

## Cost

Railway offers:
- Free tier for development
- Pay-as-you-go pricing for production
- Automatic scaling based on usage 