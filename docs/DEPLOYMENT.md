# Production Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying StyleSense.AI to production using Vercel (frontend) and Railway (backend).

## Prerequisites

- GitHub account with repository access
- Vercel account (free tier available)
- Railway account (free tier available)
- MongoDB Atlas account (free tier available)
- OpenWeatherMap API key (free)
- Domain name (optional)

## Part 1: Database Setup (MongoDB Atlas)

### Step 1: Create MongoDB Cluster

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up or log in
3. Create a new cluster:
   - Choose "Shared" (free tier)
   - Select region closest to your users
   - Cluster name: `stylesense-prod`
4. Create database user:
   - Username: `stylesense-admin`
   - Password: Generate secure password
   - Database User Privileges: "Read and write to any database"
5. Network Access:
   - Add IP Address: `0.0.0.0/0` (allow from anywhere)
   - **Note**: For production, restrict to specific IPs
6. Get connection string:
   - Click "Connect" → "Connect your application"
   - Copy connection string
   - Replace `<password>` with your password
   - Example: `mongodb+srv://stylesense-admin:PASSWORD@cluster0.xxxxx.mongodb.net/stylesense?retryWrites=true&w=majority`

### Step 2: Initialize Database

```bash
# Connect using MongoDB Compass or mongosh
mongosh "mongodb+srv://stylesense-admin:PASSWORD@cluster0.xxxxx.mongodb.net/"

# Create database and collections
use stylesense
db.createCollection("users")
db.createCollection("profiles")
db.createCollection("products")
db.createCollection("recommendations")

# Create indexes
db.profiles.createIndex({ "user_id": 1 }, { unique: true })
db.products.createIndex({ "category": 1 })
```

## Part 2: Backend Deployment (Railway)

### Step 1: Prepare Backend

1. Ensure `railway.toml` exists in `/backend` directory
2. Add `gunicorn` to `requirements.txt`:
   ```
   gunicorn==21.2.0
   ```
3. Create `Procfile` in `/backend`:
   ```
   web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app
   ```

### Step 2: Deploy to Railway

1. Go to [Railway.app](https://railway.app/)
2. Sign up with GitHub
3. Create new project:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `final-stylesense` repository
   - Root directory: `/backend`
4. Configure environment variables:
   ```
   MONGODB_URI=mongodb+srv://...
   FLASK_ENV=production
   SECRET_KEY=[generate-strong-key]
   HF_API_KEY=[your-huggingface-key]
   OPENWEATHER_API_KEY=[your-openweather-key]
   CORS_ORIGINS=https://stylesense.vercel.app
   ```
5. Deploy:
   - Railway will automatically deploy
   - Wait for build to complete (~5-10 minutes)
   - Note the deployment URL: `https://stylesense-production.up.railway.app`

### Step 3: Configure Custom Domain (Optional)

1. In Railway dashboard, go to Settings
2. Click "Generate Domain" or add custom domain
3. For custom domain:
   - Add CNAME record in your DNS: `api.yourdomain.com` → Railway URL
   - Update in Railway settings

### Step 4: Test Backend

```bash
# Health check
curl https://your-backend-url.railway.app/api/health

# Test body detection endpoint
curl -X POST https://your-backend-url.railway.app/api/body-shape/analyze \
  -F "file=@test-image.jpg"
```

## Part 3: Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. Update `vercel.json` in `/frontend` directory (already created)
2. Create production build locally to test:
   ```bash
   cd frontend
   REACT_APP_API_URL=https://your-backend-url.railway.app npm run build
   ```

### Step 2: Deploy to Vercel

1. Go to [Vercel](https://vercel.com/)
2. Sign up with GitHub
3. Import project:
   - Click "Add New" → "Project"
   - Import `final-stylesense` repository
   - Framework Preset: "Create React App"
   - Root Directory: `frontend`
4. Configure:
   - Build Command: `npm run build`
   - Output Directory: `build`
   - Install Command: `npm install`
5. Environment Variables:
   ```
   REACT_APP_API_URL=https://your-backend-url.railway.app
   CI=false
   ```
6. Deploy:
   - Click "Deploy"
   - Wait for deployment (~3-5 minutes)
   - Vercel URL: `https://stylesense.vercel.app`

### Step 3: Configure Custom Domain (Optional)

1. In Vercel dashboard, go to Settings → Domains
2. Add custom domain: `www.yourdomain.com`
3. Update DNS records as instructed by Vercel
4. Enable HTTPS (automatic with Vercel)

### Step 4: Test Frontend

1. Visit https://stylesense.vercel.app
2. Test camera capture
3. Test AR try-on
4. Test recommendations
5. Check browser console for errors

## Part 4: CI/CD Configuration

### Step 1: Configure GitHub Secrets

1. Go to GitHub repository → Settings → Secrets and variables → Actions
2. Add secrets:
   ```
   VERCEL_TOKEN=[get-from-vercel-account-settings]
   VERCEL_ORG_ID=[from-vercel-team-settings]
   VERCEL_PROJECT_ID=[from-vercel-project-settings]
   RAILWAY_TOKEN=[from-railway-account-settings]
   REACT_APP_API_URL=https://your-backend-url.railway.app
   MONGODB_URI=[your-mongodb-connection-string]
   HF_API_KEY=[your-huggingface-key]
   OPENWEATHER_API_KEY=[your-openweather-key]
   ```

### Step 2: Enable GitHub Actions

1. The `.github/workflows/ci-cd.yml` file is already in the repository
2. Push to `main` branch to trigger production deployment
3. Push to `develop` branch to trigger staging deployment
4. Monitor workflow in GitHub Actions tab

### Step 3: Branch Protection

1. Go to Settings → Branches
2. Add branch protection rule for `main`:
   - Require pull request reviews
   - Require status checks to pass
   - Include administrators: No
3. Add branch protection rule for `develop`:
   - Require status checks to pass

## Part 5: Monitoring and Logging

### Step 1: Railway Logs

1. In Railway dashboard, click on your service
2. Go to "Observability" tab
3. View real-time logs
4. Set up log retention

### Step 2: Vercel Analytics

1. In Vercel dashboard, go to Analytics
2. Enable Web Analytics (free)
3. View performance metrics
4. Set up alerts

### Step 3: Error Tracking (Optional)

**Sentry Integration**:

1. Create Sentry account
2. Add to frontend:
   ```bash
   npm install @sentry/react
   ```
3. Initialize in `src/index.js`:
   ```javascript
   import * as Sentry from "@sentry/react";
   
   Sentry.init({
     dsn: process.env.REACT_APP_SENTRY_DSN,
     environment: process.env.NODE_ENV,
   });
   ```
4. Add to backend:
   ```bash
   pip install sentry-sdk[flask]
   ```

## Part 6: Security Hardening

### Step 1: Enable HTTPS

- Vercel: Automatic HTTPS
- Railway: Automatic HTTPS
- Verify SSL certificates are valid

### Step 2: Configure CORS

Backend `app.py`:
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://stylesense.vercel.app", "https://www.yourdomain.com"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### Step 3: Rate Limiting

Ensure rate limiting is enabled in production:
```python
limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://localhost:6379"  # Optional Redis
)
```

### Step 4: Security Headers

Add to backend:
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    return response
```

## Part 7: Performance Optimization

### Step 1: Enable Caching

**Vercel Cache Configuration**:
```json
{
  "headers": [
    {
      "source": "/static/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    }
  ]
}
```

### Step 2: Image Optimization

1. Use WebP format for images
2. Implement lazy loading
3. Add image CDN (Cloudinary/ImageKit)

### Step 3: API Response Caching

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300
})

@app.route('/api/product-catalogue')
@cache.cached(timeout=300)
def get_catalogue():
    # ... implementation
```

## Part 8: Backup and Recovery

### Step 1: Database Backups

1. MongoDB Atlas automatic backups (enabled by default)
2. Configure backup schedule:
   - Go to Cluster → Backup
   - Enable continuous backups
   - Set retention period (7 days free tier)

### Step 2: Code Backups

1. GitHub repository is the source of truth
2. Create release tags for versions:
   ```bash
   git tag -a v1.0.0 -m "Production release v1.0.0"
   git push origin v1.0.0
   ```

### Step 3: Disaster Recovery Plan

1. Document recovery procedures
2. Test restoration process
3. Keep encrypted backup of environment variables
4. Maintain list of critical dependencies

## Part 9: Post-Deployment Checklist

- [ ] Frontend accessible at production URL
- [ ] Backend API responding at production URL
- [ ] MongoDB connection working
- [ ] All API endpoints tested
- [ ] HTTPS enabled and working
- [ ] CORS configured correctly
- [ ] Environment variables set
- [ ] CI/CD pipeline working
- [ ] Monitoring and logging enabled
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Error tracking configured
- [ ] Database backups enabled
- [ ] Documentation updated with URLs
- [ ] Team notified of deployment

## Part 10: Rollback Procedure

### If Deployment Fails:

**Frontend (Vercel)**:
1. Go to Deployments tab
2. Find last working deployment
3. Click "..." → "Promote to Production"

**Backend (Railway)**:
1. Go to Deployments tab
2. Click on last working deployment
3. Click "Redeploy"

**Database**:
1. Go to MongoDB Atlas → Backup
2. Restore from snapshot
3. Select timestamp before issue

## Troubleshooting

### Common Issues

**Issue**: Frontend can't connect to backend
- **Solution**: Check CORS settings, verify API URL in environment variables

**Issue**: 500 errors from backend
- **Solution**: Check Railway logs, verify MongoDB connection string

**Issue**: Slow API responses
- **Solution**: Check Railway metrics, consider upgrading plan or optimizing code

**Issue**: Build failures
- **Solution**: Check GitHub Actions logs, verify dependencies in requirements.txt/package.json

**Issue**: Database connection timeout
- **Solution**: Verify MongoDB Atlas network access settings, check connection string

## Support

For deployment issues:
- Railway Support: https://help.railway.app/
- Vercel Support: https://vercel.com/support
- MongoDB Atlas Support: https://www.mongodb.com/support

## Summary

Production deployment involves:
1. ✅ MongoDB Atlas for database
2. ✅ Railway for backend API
3. ✅ Vercel for frontend
4. ✅ GitHub Actions for CI/CD
5. ✅ Security hardening
6. ✅ Monitoring and logging
7. ✅ Backup and recovery

**Estimated Setup Time**: 2-3 hours

**Monthly Cost**: ~$42 (Free tiers + domain)

**Scalability**: Supports up to 100 concurrent users on free tiers

---

**Next Steps**: See `NEXT_STEPS.md` for future enhancements and roadmap.
