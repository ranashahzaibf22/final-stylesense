# Complete Deployment Guide - StyleSense.AI

This guide provides step-by-step instructions to deploy the StyleSense.AI application to production using Railway (backend) and Vercel (frontend).

## 🎯 Overview

- **Backend**: Flask API deployed on Railway using Docker
- **Frontend**: React app deployed on Vercel
- **Database**: MongoDB Atlas (free tier)

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ GitHub account with repository access
- ✅ Railway account (https://railway.app)
- ✅ Vercel account (https://vercel.com)
- ✅ MongoDB Atlas account (https://www.mongodb.com/cloud/atlas)

## 🚀 Quick Start Deployment

### Step 1: Set Up MongoDB Atlas

1. Create a free MongoDB Atlas account
2. Create a new cluster (M0 Free tier)
3. Set up database access:
   - Create a database user
   - Allow access from anywhere (0.0.0.0/0) for Railway
4. Get your connection string:
   ```
   mongodb+srv://<username>:<password>@cluster.mongodb.net/stylesense
   ```

### Step 2: Deploy Backend to Railway (Docker)

1. **Connect Repository**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `final-stylesense` repository
   - Railway will auto-detect the Dockerfile in `/backend`

2. **Configure Environment Variables**
   
   In Railway Dashboard → Variables, add:

   ```env
   # Required
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/stylesense
   FLASK_SECRET_KEY=your-strong-random-secret-key-here
   
   # Optional but recommended
   HF_API_KEY=your-huggingface-api-key
   OPENWEATHER_API_KEY=your-openweather-api-key
   CORS_ORIGINS=https://your-app.vercel.app
   FLASK_DEBUG=False
   USE_GPU=False
   WORKERS=4
   TIMEOUT=120
   ```

   **Important**: 
   - Do NOT set `PORT` - Railway sets this automatically
   - Generate a strong secret key: `python -c "import secrets; print(secrets.token_hex(32))"`

3. **Deploy**
   - Railway will automatically build using the Dockerfile
   - Wait 3-5 minutes for build completion
   - Get your Railway URL: `https://your-app.up.railway.app`

4. **Verify Backend**
   ```bash
   curl https://your-app.up.railway.app/api/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "database": "connected",
     "ml_models": "available",
     "version": "1.0.0"
   }
   ```

### Step 3: Deploy Frontend to Vercel

1. **Connect Repository**
   - Go to https://vercel.com
   - Click "Add New..." → "Project"
   - Import `final-stylesense` repository
   - Set **Root Directory** to `frontend`
   - Vercel auto-detects Create React App

2. **Configure Environment Variables**
   
   In Vercel Dashboard → Settings → Environment Variables, add:

   ```env
   # Required
   REACT_APP_API_URL=https://your-railway-app.up.railway.app/api
   CI=false
   
   # Optional
   REACT_APP_API_TIMEOUT=30000
   REACT_APP_ENABLE_CAMERA=true
   REACT_APP_ENABLE_AR_TRYON=true
   REACT_APP_ENABLE_RECOMMENDATIONS=true
   ```

   **Important**: 
   - Replace `your-railway-app.up.railway.app` with your actual Railway URL
   - Include `/api` suffix in REACT_APP_API_URL
   - Set variables for: Production, Preview, Development

3. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for build
   - Get your Vercel URL: `https://your-app.vercel.app`

4. **Update Backend CORS**
   - Go back to Railway → Variables
   - Update `CORS_ORIGINS` to include your Vercel URL:
     ```
     CORS_ORIGINS=https://your-app.vercel.app
     ```
   - Railway will auto-redeploy

### Step 4: Test Complete Setup

1. Visit your Vercel URL
2. Open browser DevTools → Console
3. Check for API connectivity:
   - No CORS errors
   - API requests succeed
   - Data loads properly

## 📁 Deployment Files

### Backend (Docker)
- `backend/Dockerfile` - Docker configuration for Railway
- `backend/.dockerignore` - Files excluded from Docker build
- `backend/start.sh` - Startup script
- `backend/Procfile` - Fallback if Docker fails
- `backend/railway.toml` - Railway configuration

### Frontend (Vercel)
- `frontend/vercel.json` - Vercel configuration
- `frontend/package.json` - Build settings
- `frontend/.env.example` - Environment variable template

## 🔧 Troubleshooting

### Backend Issues

**Problem**: Build fails on Railway
- **Solution**: Check Railway build logs, verify Dockerfile syntax, ensure requirements.txt is correct

**Problem**: App crashes on start
- **Solution**: Check Railway application logs, verify environment variables, test database connection

**Problem**: API returns 500 errors
- **Solution**: Check MongoDB connection, verify HF_API_KEY if using ML features, review error logs

### Frontend Issues

**Problem**: API requests fail
- **Solution**: Verify REACT_APP_API_URL is correct, check backend health endpoint, verify CORS settings

**Problem**: CORS errors
- **Solution**: Add Vercel URL to backend CORS_ORIGINS, redeploy backend

**Problem**: Blank page after deploy
- **Solution**: Check browser console for errors, verify build succeeded, check routing in vercel.json

### Database Issues

**Problem**: Database connection fails
- **Solution**: Verify MONGODB_URI format, check database user credentials, ensure network access allows Railway IPs

## 📊 Monitoring

### Railway
- View logs: Dashboard → Deployments → View Logs
- Monitor metrics: CPU, Memory, Network
- Health checks: Automatic via `/api/health`

### Vercel
- View logs: Dashboard → Deployments → Function Logs
- Analytics: Dashboard → Analytics
- Real-time metrics available in dashboard

## 🔐 Security Checklist

- [ ] Strong FLASK_SECRET_KEY generated
- [ ] CORS_ORIGINS restricted to frontend domains only
- [ ] No .env files committed to Git
- [ ] Database password is strong
- [ ] MongoDB network access configured properly
- [ ] API keys kept secure (backend only)
- [ ] HTTPS enabled (automatic on Railway/Vercel)

## 💰 Cost Estimate

- **Railway**: Free tier (500 hours/month, ~$5/month after)
- **Vercel**: Free tier (unlimited deployments)
- **MongoDB Atlas**: Free tier (M0 - 512MB storage)

**Total**: $0-5/month

## 🔄 Continuous Deployment

Both Railway and Vercel automatically deploy when you push to GitHub:

- **Main branch** → Production deployment
- **Pull requests** → Preview deployments
- **Other branches** → Preview deployments (Vercel)

## 📚 Additional Resources

- [Backend Docker Deployment Guide](backend/DOCKER_DEPLOY.md)
- [Frontend Vercel Deployment Guide](frontend/VERCEL_DEPLOY.md)
- [Full Deployment Documentation](DEPLOYMENT.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)

## 🆘 Getting Help

1. Check deployment guides in this repository
2. Review Railway/Vercel documentation
3. Check application logs for errors
4. Create an issue in the GitHub repository

## ✅ Deployment Checklist

Use this checklist to track your deployment progress:

### Database
- [ ] MongoDB Atlas account created
- [ ] Cluster created and configured
- [ ] Database user created
- [ ] Network access configured (0.0.0.0/0)
- [ ] Connection string obtained

### Backend
- [ ] Railway account created
- [ ] Repository connected to Railway
- [ ] Dockerfile detected by Railway
- [ ] Environment variables configured
- [ ] Build completed successfully
- [ ] Health endpoint responds correctly
- [ ] Railway URL obtained

### Frontend
- [ ] Vercel account created
- [ ] Repository connected to Vercel
- [ ] Root directory set to `frontend`
- [ ] Environment variables configured (REACT_APP_API_URL)
- [ ] Build completed successfully
- [ ] Vercel URL obtained

### Integration
- [ ] Backend CORS updated with Vercel URL
- [ ] Frontend API calls working
- [ ] No CORS errors
- [ ] All features tested
- [ ] Custom domain configured (optional)

---

**🎉 Congratulations!** Your StyleSense.AI application is now deployed to production!

For detailed guides, see:
- Backend: [DOCKER_DEPLOY.md](backend/DOCKER_DEPLOY.md)
- Frontend: [VERCEL_DEPLOY.md](frontend/VERCEL_DEPLOY.md)
