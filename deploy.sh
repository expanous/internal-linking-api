#!/bin/bash

echo "🚀 Enhanced Internal Linking API Deployment"
echo "=========================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No remote repository found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/yourusername/your-repo.git"
    exit 1
fi

echo "✅ Git repository ready"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git add .
git commit -m "Deploy API to production" || echo "No changes to commit"
git push origin main

echo ""
echo "🎉 Code pushed to GitHub!"
echo ""
echo "📋 Next steps:"
echo "1. Go to Railway: https://railway.app"
echo "   OR"
echo "2. Go to Render: https://render.com"
echo ""
echo "3. Connect your GitHub repository"
echo "4. Deploy automatically!"
echo ""
echo "🔗 Your API will be available at:"
echo "   Railway: https://your-app-name.railway.app"
echo "   Render: https://your-app-name.onrender.com"
echo ""
echo "📖 API Documentation will be at:"
echo "   /docs" 