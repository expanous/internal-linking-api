# Railway Deployment Checklist

## Pre-Deployment Checklist

### ✅ Repository Setup
- [ ] All code is committed to GitHub repository
- [ ] Repository is public or Railway has access
- [ ] No sensitive data in repository (API keys, passwords, etc.)

### ✅ Required Files
- [ ] `api_internal_linking.py` - Main FastAPI application
- [ ] `enhanced_internal_linking.py` - Core linking logic
- [ ] `glossary_terms.json` - Glossary data (114KB file)
- [ ] `requirements.txt` - Python dependencies (includes spacy)
- [ ] `railway_start.py` - Startup script
- [ ] `nixpacks.toml` - Railway build configuration
- [ ] `Procfile` - Alternative deployment configuration
- [ ] `railway.json` - Railway-specific configuration

### ✅ Dependencies
- [ ] `fastapi==0.104.1`
- [ ] `uvicorn[standard]==0.24.0`
- [ ] `pydantic==2.5.0`
- [ ] `python-multipart==0.0.6`
- [ ] `beautifulsoup4==4.12.2`
- [ ] `lxml==4.9.3`
- [ ] `python-dotenv==1.0.0`
- [ ] `spacy==3.7.2`

### ✅ Configuration
- [ ] `nixpacks.toml` uses `python railway_start.py` as start command
- [ ] `railway_start.py` handles spaCy model downloading
- [ ] Port configuration uses environment variable
- [ ] Health check endpoint at `/health`

## Deployment Steps

### 1. Railway Account Setup
- [ ] Create Railway account at [railway.app](https://railway.app)
- [ ] Connect GitHub account
- [ ] Verify repository access

### 2. Deploy Application
- [ ] Create new Railway project
- [ ] Select "Deploy from GitHub repo"
- [ ] Choose your repository
- [ ] Wait for build to complete
- [ ] Note the generated URL

### 3. Verify Deployment
- [ ] Test health check: `GET /health`
- [ ] Test root endpoint: `GET /`
- [ ] Test statistics: `GET /stats`
- [ ] Test article processing: `POST /process`
- [ ] Check API documentation: `GET /docs`

### 4. Test with Sample Data
- [ ] Run `test_railway_deployment.py` with your Railway URL
- [ ] Verify all endpoints work correctly
- [ ] Check that spaCy model loaded successfully
- [ ] Confirm glossary terms are accessible

## Post-Deployment

### ✅ Monitoring
- [ ] Set up Railway monitoring
- [ ] Configure health check alerts
- [ ] Monitor resource usage

### ✅ Documentation
- [ ] Update API documentation if needed
- [ ] Share Railway URL with team
- [ ] Document any environment-specific configurations

### ✅ Testing
- [ ] Test with real article content
- [ ] Verify link generation works correctly
- [ ] Check performance under load

## Troubleshooting

### Common Issues
- [ ] Build fails: Check `requirements.txt` and dependencies
- [ ] spaCy model issues: Check startup logs
- [ ] Port issues: Verify environment variable usage
- [ ] Memory issues: Check resource limits

### Logs to Check
- [ ] Build logs in Railway dashboard
- [ ] Application startup logs
- [ ] spaCy model download logs
- [ ] Health check responses

## Success Criteria

Your deployment is successful when:
- [ ] Health check returns `{"status": "healthy"}`
- [ ] API documentation is accessible at `/docs`
- [ ] Article processing works with sample content
- [ ] All endpoints respond within reasonable time
- [ ] No critical errors in logs

## Next Steps

After successful deployment:
1. Set up custom domain (optional)
2. Configure monitoring and alerts
3. Set up CI/CD for automatic deployments
4. Document API usage for your team
5. Plan for scaling and optimization 