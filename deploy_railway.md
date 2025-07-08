# Deploy to Railway

## Quick Deploy Steps

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Connect Repository**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Environment**
   - Railway will auto-detect Python
   - Add environment variable: `PORT=8000`

4. **Deploy**
   - Railway will automatically build and deploy
   - Your API will be available at: `https://your-app-name.railway.app`

## Manual Deploy with Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

## Environment Variables
- `PORT`: 8000 (auto-set by Railway)
- No other variables needed for basic deployment 