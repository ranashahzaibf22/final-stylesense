# StyleSense.AI - Deployment Guide

## Overview
This guide covers deployment of StyleSense.AI to production environments.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Backend Deployment (Railway)](#backend-deployment-railway)
- [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
- [Database Setup (MongoDB Atlas)](#database-setup-mongodb-atlas)
- [Environment Variables](#environment-variables)
- [Post-Deployment](#post-deployment)
- [Monitoring](#monitoring)

---

## Prerequisites

### Accounts Required
- [ ] GitHub account (with repository access)
- [ ] MongoDB Atlas account (free tier available)
- [ ] Railway account (for backend) OR Heroku
- [ ] Vercel account (for frontend) OR Netlify

### Pre-Deployment Checklist
- [ ] All tests passing locally
- [ ] Code committed to GitHub
- [ ] Environment variables documented
- [ ] Database backup created (if migrating)
- [ ] API endpoints tested

---

## Database Setup (MongoDB Atlas)

### 1. Create MongoDB Atlas Account
1. Visit [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up for free account
3. Verify email

### 2. Create Cluster
1. Click "Build a Cluster"
2. Select **FREE** tier (M0 Sandbox)
3. Choose cloud provider and region (closest to your backend)
4. Name your cluster (e.g., "stylesense-cluster")
5. Click "Create Cluster" (takes 3-5 minutes)

### 3. Configure Database Access
1. Go to "Database Access" in left sidebar
2. Click "Add New Database User"
3. Authentication Method: **Password**
4. Username: `stylesense_admin`
5. Password: Generate secure password (save this!)
6. Database User Privileges: **Read and write to any database**
7. Click "Add User"

### 4. Configure Network Access
1. Go to "Network Access" in left sidebar
2. Click "Add IP Address"
3. For development: Click "Allow Access from Anywhere" (0.0.0.0/0)
4. For production: Add specific IP addresses
5. Click "Confirm"

### 5. Get Connection String
1. Go to "Databases" (main page)
2. Click "Connect" on your cluster
3. Select "Connect your application"
4. Driver: **Python**, Version: **3.6 or later**
5. Copy connection string:
   ```
   mongodb+srv://stylesense_admin:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. Replace `<password>` with your actual password
7. Add database name: `/stylesense` before the `?`
   ```
   mongodb+srv://stylesense_admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/stylesense?retryWrites=true&w=majority
   ```

### 6. Create Database and Collections
Run in MongoDB Compass or Atlas UI:
```javascript
use stylesense

// Create collections
db.createCollection("wardrobe")
db.createCollection("recommendations")
db.createCollection("users")

// Create indexes
db.wardrobe.createIndex({ "user_id": 1 })
db.wardrobe.createIndex({ "category": 1 })
db.recommendations.createIndex({ "user_id": 1 })
db.recommendations.createIndex({ "created_at": -1 })
```

---

## Backend Deployment (Railway)

### Option 1: Railway (Recommended)

#### 1. Prepare Backend
1. Ensure `requirements.txt` is complete
2. Verify `railway.toml` exists at repository root with Docker configuration:
   ```toml
   [build]
   builder = "DOCKERFILE"
   dockerfilePath = "backend/Dockerfile"
   dockerContext = "backend"
   ```
3. Ensure `Dockerfile` exists in backend directory
4. Verify `start.sh` is executable and in backend directory
5. Ensure `PORT` environment variable is used in `app.py`

#### 2. Deploy to Railway
1. Visit [Railway.app](https://railway.app/)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Select your repository
6. Railway will automatically detect the Dockerfile and use the railway.toml configuration
7. No need to manually configure build commands - railway.toml handles this

#### 3. Set Environment Variables
In Railway project settings, add:
```env
MONGODB_URI=mongodb+srv://stylesense_admin:PASSWORD@cluster0.xxxxx.mongodb.net/stylesense
FLASK_SECRET_KEY=your-production-secret-key-here
FLASK_DEBUG=False
CORS_ORIGINS=https://your-frontend-domain.vercel.app
USE_GPU=False
PORT=5000
```

#### 4. Deploy
1. Click "Deploy"
2. Wait for build to complete
3. Get your Railway URL (e.g., `https://stylesense-backend.up.railway.app`)

### Option 2: Heroku

#### 1. Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Ubuntu
curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# Windows - download from heroku.com
```

#### 2. Login and Create App
```bash
heroku login
cd backend
heroku create stylesense-backend
```

#### 3. Set Environment Variables
```bash
heroku config:set MONGODB_URI="your-mongodb-uri"
heroku config:set FLASK_SECRET_KEY="your-secret-key"
heroku config:set FLASK_DEBUG=False
heroku config:set CORS_ORIGINS="https://your-frontend.vercel.app"
```

#### 4. Create Procfile
```
web: python app.py
```

#### 5. Deploy
```bash
git push heroku main
heroku logs --tail
```

---

## Frontend Deployment (Vercel)

### 1. Prepare Frontend
1. Create `vercel.json` in frontend directory:
   ```json
   {
     "buildCommand": "npm run build",
     "outputDirectory": "build",
     "devCommand": "npm start",
     "installCommand": "npm install"
   }
   ```

2. Update API URL for production
   Create `frontend/.env.production`:
   ```env
   REACT_APP_API_URL=https://your-backend-url.railway.app/api
   ```

### 2. Deploy to Vercel
1. Visit [Vercel.com](https://vercel.com)
2. Sign up/Login with GitHub
3. Click "Add New Project"
4. Import your GitHub repository
5. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### 3. Set Environment Variables
In Vercel project settings > Environment Variables:
```env
REACT_APP_API_URL=https://your-backend-url.railway.app/api
```

### 4. Deploy
1. Click "Deploy"
2. Wait for build to complete
3. Get your Vercel URL (e.g., `https://stylesense.vercel.app`)

### 5. Update Backend CORS
Go back to Railway/Heroku and update `CORS_ORIGINS`:
```env
CORS_ORIGINS=https://stylesense.vercel.app
```

---

## Environment Variables

### Production Environment Variables

#### Backend
```env
# Database
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/stylesense

# Security
FLASK_SECRET_KEY=generate-strong-random-key-here
FLASK_DEBUG=False

# CORS (comma-separated)
CORS_ORIGINS=https://your-frontend.vercel.app,https://www.yourdomain.com

# Optional APIs
HF_API_KEY=your_huggingface_key
WEATHER_API_KEY=your_weather_key

# Configuration
USE_GPU=False
PORT=5000
```

#### Frontend
```env
REACT_APP_API_URL=https://your-backend.railway.app/api
```

---

## Post-Deployment

### 1. Verify Deployment

#### Check Backend Health
```bash
curl https://your-backend-url.railway.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "ml_models": "fallback_mode",
  "timestamp": "2024-11-02T10:00:00.000Z"
}
```

#### Check Frontend
1. Visit `https://your-frontend.vercel.app`
2. Check Dashboard loads
3. Verify API connection in browser console
4. Test file upload
5. Test recommendations

### 2. Configure Custom Domain (Optional)

#### Vercel Custom Domain
1. Go to Project Settings > Domains
2. Add your domain
3. Update DNS records as instructed
4. Wait for SSL certificate

#### Railway Custom Domain
1. Go to Project Settings
2. Add custom domain
3. Update DNS records
4. Enable SSL

### 3. Enable HTTPS
Both Railway and Vercel provide automatic HTTPS. Verify:
```bash
curl -I https://your-domain.com
```

### 4. Test All Features
- [ ] User registration/login (if implemented)
- [ ] Image upload
- [ ] Wardrobe management
- [ ] Recommendations generation
- [ ] AR try-on
- [ ] Product catalogue
- [ ] Camera capture

---

## Monitoring

### Application Monitoring

#### Railway Monitoring
- View logs: Project > Deployments > Logs
- Metrics: Project > Metrics
- Set up alerts in Settings

#### Vercel Monitoring
- Analytics: Project > Analytics
- Logs: Project > Deployments > Logs
- Real-time metrics available

### Database Monitoring

#### MongoDB Atlas
- Metrics: Cluster > Metrics
- Real-time Performance: Available in dashboard
- Alerts: Set up email alerts

### Error Tracking (Optional)

#### Sentry Setup
1. Create Sentry account
2. Install SDK:
   ```bash
   pip install sentry-sdk[flask]
   npm install @sentry/react
   ```

3. Initialize in `app.py`:
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.flask import FlaskIntegration

   sentry_sdk.init(
       dsn="your-sentry-dsn",
       integrations=[FlaskIntegration()],
       traces_sample_rate=1.0
   )
   ```

---

## Troubleshooting

### Common Issues

#### 1. "Application Error" on Railway
- Check logs: `railway logs`
- Verify environment variables
- Check Python version compatibility

#### 2. Build Failed on Vercel
- Check build logs
- Verify package.json scripts
- Check Node version (use `.nvmrc` file)

#### 3. Database Connection Timeout
- Verify MongoDB Atlas IP whitelist
- Check connection string format
- Ensure network access configured

#### 4. CORS Errors
- Verify `CORS_ORIGINS` includes frontend URL
- Check protocol (http vs https)
- Ensure no trailing slashes

#### 5. 502 Bad Gateway
- Check backend is running
- Verify PORT environment variable
- Check backend logs for errors

---

## Maintenance

### Regular Tasks
- [ ] Monitor error rates
- [ ] Check database performance
- [ ] Review logs weekly
- [ ] Update dependencies monthly
- [ ] Backup database regularly
- [ ] Monitor API usage
- [ ] Check SSL certificate expiry

### Scaling Considerations

#### When to Scale Backend
- Response time > 2 seconds
- CPU usage > 70%
- Memory usage > 80%
- Error rate > 1%

#### Scaling Options
1. **Vertical Scaling**: Upgrade Railway/Heroku plan
2. **Horizontal Scaling**: Multiple instances with load balancer
3. **Database Scaling**: MongoDB Atlas cluster tier upgrade
4. **CDN**: Use Cloudflare or similar for static assets

---

## Rollback Plan

### If Deployment Fails

#### Railway
1. Go to Deployments
2. Click on previous working deployment
3. Click "Redeploy"

#### Vercel
1. Go to Deployments
2. Find previous working version
3. Click three dots > "Promote to Production"

### Database Rollback
1. Use MongoDB Atlas backup
2. Restore to previous snapshot
3. Update connection string if needed

---

## Security Checklist

- [ ] All environment variables in config (not in code)
- [ ] MongoDB network access restricted
- [ ] Strong database passwords
- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] File upload validation active
- [ ] Rate limiting implemented (future)
- [ ] Error messages don't expose sensitive info
- [ ] Dependencies updated regularly
- [ ] Security headers configured

---

## Support

For deployment issues:
- Check service status pages
- Review documentation
- Check GitHub issues
- Contact platform support

---

**Deployment Checklist Complete! 🚀**

Your StyleSense.AI application is now live and ready for users!
