# Deploy to Render

## Quick Deploy Steps

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service**
   - **Name**: `internal-linking-api`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command**: `uvicorn api_internal_linking:app --host 0.0.0.0 --port $PORT`

4. **Environment Variables**
   - `PORT`: `8000`

5. **Deploy**
   - Click "Create Web Service"
   - Render will build and deploy automatically
   - Your API will be available at: `https://your-app-name.onrender.com`

## Manual Configuration

If you prefer manual setup:

```yaml
# render.yaml
services:
  - type: web
    name: internal-linking-api
    env: python
    buildCommand: pip install -r requirements.txt && python -m spacy download en_core_web_sm
    startCommand: uvicorn api_internal_linking:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PORT
        value: 8000
```

## Features
- Automatic HTTPS
- Custom domains
- Auto-scaling
- Health checks 