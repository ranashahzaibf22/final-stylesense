# Pre-Deployment Checklist

Use this checklist before deploying to Railway (backend) and Vercel (frontend) to ensure everything is configured correctly.

## 📋 General Prerequisites

- [ ] GitHub repository is up to date with latest code
- [ ] All changes are committed and pushed
- [ ] `.env` files are in `.gitignore` (never commit secrets!)
- [ ] Code has been tested locally
- [ ] Documentation is updated

---

## 🗄️ Database Setup (MongoDB Atlas)

### Account & Cluster
- [ ] MongoDB Atlas account created
- [ ] Free tier cluster created (M0 Sandbox)
- [ ] Cluster is running (not paused)
- [ ] Cluster region selected (close to backend location)

### Database Access
- [ ] Database user created
- [ ] Username is set (e.g., `stylesense_admin`)
- [ ] Strong password generated and saved securely
- [ ] User has "Read and write to any database" permissions

### Network Access
- [ ] IP whitelist configured
- [ ] 0.0.0.0/0 added (allow from anywhere) for Railway/Vercel
- [ ] Network access confirmed as active

### Connection String
- [ ] Connection string obtained from Atlas
- [ ] Format: `mongodb+srv://user:password@cluster.mongodb.net/stylesense`
- [ ] Password URL-encoded if contains special characters
- [ ] Database name included in connection string
- [ ] Connection string tested locally (if possible)

---

## 🚂 Backend Deployment (Railway)

### Railway Account
- [ ] Railway account created at [railway.app](https://railway.app)
- [ ] Signed in with GitHub account
- [ ] GitHub repository access granted

### Project Setup
- [ ] New project created in Railway
- [ ] Repository connected: ranashahzaibf22/final-stylesense
- [ ] Root directory configured (leave empty or set to `backend`)
- [ ] Service deployed and running

### Files Verification
- [ ] `backend/start.sh` exists and is executable
- [ ] `backend/Procfile` exists as fallback
- [ ] `backend/requirements.txt` is complete
- [ ] `backend/railway.toml` is configured
- [ ] `backend/app.py` uses `PORT` environment variable

### Environment Variables (Railway Dashboard)
- [ ] `MONGODB_URI` - MongoDB connection string
- [ ] `FLASK_SECRET_KEY` - Strong random secret key (32+ chars)
- [ ] `CORS_ORIGINS` - Frontend URL (will be set after Vercel deployment)
- [ ] `FLASK_DEBUG` - Set to `False`
- [ ] `HF_API_KEY` - Hugging Face API key (optional but recommended)
- [ ] `OPENWEATHER_API_KEY` - OpenWeather API key (optional)
- [ ] `USE_GPU` - Set to `False` (unless GPU available)

### Deployment Verification
- [ ] Build completed successfully
- [ ] Service is running
- [ ] Railway URL obtained (e.g., `https://xxx.up.railway.app`)
- [ ] Health endpoint accessible: `/api/health` returns 200
- [ ] Response shows: `"status": "healthy"`, `"database": "connected"`

### Post-Deployment
- [ ] Logs checked for errors
- [ ] Test API endpoints with curl/Postman
- [ ] Response times acceptable (<2 seconds)
- [ ] No crash loops or restarts

---

## 🚀 Frontend Deployment (Vercel)

### Vercel Account
- [ ] Vercel account created at [vercel.com](https://vercel.com)
- [ ] Signed in with GitHub account
- [ ] GitHub repository access granted

### Project Setup
- [ ] New project created in Vercel
- [ ] Repository imported: ranashahzaibf22/final-stylesense
- [ ] Framework detected as "Create React App"
- [ ] Root directory set to: `frontend`

### Build Configuration
- [ ] Build Command: `npm install && npm run build`
- [ ] Output Directory: `build`
- [ ] Install Command: `npm install`
- [ ] Node.js Version: 18.x or 20.x

### Files Verification
- [ ] `frontend/package.json` has `build` script
- [ ] `frontend/vercel.json` exists and configured
- [ ] `frontend/.vercel/project.json` exists
- [ ] `frontend/src/utils/api.js` has default export

### Environment Variables (Vercel Dashboard)
- [ ] `REACT_APP_API_URL` - Backend Railway URL (e.g., `https://xxx.railway.app`)
- [ ] `REACT_APP_HF_KEY` - Hugging Face key (optional, if used in frontend)
- [ ] `CI` - Set to `false` (to allow build warnings)
- [ ] Variables set for "Production" environment
- [ ] Variables set for "Preview" environment (optional)

### Deployment Verification
- [ ] Build completed successfully
- [ ] No build errors in logs
- [ ] Vercel URL obtained (e.g., `https://xxx.vercel.app`)
- [ ] Site loads without blank page
- [ ] No JavaScript errors in console (F12)
- [ ] API calls work (check Network tab)

### Post-Deployment
- [ ] Homepage loads correctly
- [ ] All pages/routes accessible
- [ ] Images and assets load
- [ ] API connectivity verified
- [ ] Mobile responsiveness checked

---

## 🔄 Final Configuration

### Update Backend CORS
- [ ] Go to Railway dashboard
- [ ] Update `CORS_ORIGINS` environment variable
- [ ] Set to Vercel URL: `https://your-app.vercel.app`
- [ ] Railway auto-redeploys with new configuration
- [ ] Verify CORS works (no console errors in frontend)

### Custom Domains (Optional)
- [ ] Custom domain purchased (if desired)
- [ ] Domain added in Vercel settings
- [ ] DNS records configured
- [ ] SSL certificate issued automatically
- [ ] Backend domain added in Railway (if desired)
- [ ] Update CORS_ORIGINS with custom domain

### SSL/HTTPS
- [ ] Backend uses HTTPS (Railway provides automatically)
- [ ] Frontend uses HTTPS (Vercel provides automatically)
- [ ] API URLs use https:// protocol
- [ ] No mixed content warnings

---

## 🧪 Testing

### Backend Testing
- [ ] Health endpoint: `GET /api/health` → 200 OK
- [ ] Upload endpoint: `POST /api/wardrobe/upload` with test image
- [ ] Recommendations: `GET /api/recommendations?user_id=test`
- [ ] Product catalogue: `GET /api/product-catalogue`
- [ ] All endpoints return expected responses
- [ ] Error handling works (test with invalid inputs)

### Frontend Testing
- [ ] Homepage loads
- [ ] Navigation works
- [ ] Dashboard shows data
- [ ] Wardrobe upload works
- [ ] Recommendations load
- [ ] AR try-on functions
- [ ] Camera capture works (if supported)
- [ ] No console errors

### Integration Testing
- [ ] Frontend → Backend API calls work
- [ ] File uploads succeed
- [ ] Data displays correctly
- [ ] Error messages show appropriately
- [ ] Loading states work
- [ ] CORS no longer blocks requests

### Cross-Browser Testing
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari (if possible)
- [ ] Mobile browsers

---

## 📊 Monitoring Setup

### Railway Monitoring
- [ ] Log into Railway dashboard regularly
- [ ] Check metrics: CPU, Memory, Network
- [ ] Set up alerts (if available)
- [ ] Monitor error rates

### Vercel Monitoring
- [ ] Check Analytics dashboard
- [ ] Monitor page views
- [ ] Check Core Web Vitals
- [ ] Review build history

### Database Monitoring
- [ ] MongoDB Atlas metrics enabled
- [ ] Check connection count
- [ ] Monitor storage usage
- [ ] Set up alerts for quota limits

---

## 📚 Documentation

### Code Documentation
- [ ] README.md updated with deployment info
- [ ] DEPLOYMENT.md comprehensive
- [ ] QUICK_DEPLOY.md available
- [ ] TROUBLESHOOTING.md created
- [ ] API endpoints documented

### Environment Variables Documentation
- [ ] Backend `.env.example` complete
- [ ] Frontend `.env.example` complete
- [ ] All required variables documented
- [ ] Default values specified

### Deployment Guides
- [ ] backend/DEPLOY_README.md created
- [ ] frontend/DEPLOY_README.md created
- [ ] Step-by-step instructions clear
- [ ] Troubleshooting sections included

---

## 🔐 Security Checklist

### Secrets Management
- [ ] No secrets in Git history
- [ ] `.env` files in `.gitignore`
- [ ] Environment variables use platform secrets
- [ ] API keys rotated if exposed
- [ ] Strong random secret keys used

### Access Control
- [ ] MongoDB users have least privilege
- [ ] Database access restricted (IP whitelist if possible)
- [ ] Railway project access controlled
- [ ] Vercel project access controlled

### HTTPS & CORS
- [ ] All URLs use HTTPS
- [ ] CORS properly configured (not `*`)
- [ ] Security headers configured
- [ ] File upload validation active

---

## 📱 Performance Optimization

### Backend
- [ ] Gunicorn workers configured (4 default)
- [ ] Timeout set appropriately (120s default)
- [ ] ML models load efficiently
- [ ] Database queries optimized
- [ ] Caching implemented where appropriate

### Frontend
- [ ] Production build minified
- [ ] Static assets cached (1 year)
- [ ] Images optimized
- [ ] Code splitting used
- [ ] Lazy loading implemented

---

## 🎯 Go-Live Checklist

### Final Verification
- [ ] All previous checklist items completed
- [ ] Testing phase passed
- [ ] No critical bugs
- [ ] Performance acceptable
- [ ] Security reviewed

### Communication
- [ ] Team notified of deployment
- [ ] Users informed (if applicable)
- [ ] Support channels ready
- [ ] Rollback plan documented

### Monitoring
- [ ] Error tracking active
- [ ] Logs being collected
- [ ] Metrics dashboard ready
- [ ] Alert systems configured

---

## 🚨 Rollback Plan

### If Deployment Fails

**Railway**:
1. Go to Dashboard → Deployments
2. Find previous working deployment
3. Click "Redeploy"
4. Verify service recovers

**Vercel**:
1. Go to Dashboard → Deployments
2. Find previous working deployment
3. Click "..." → "Promote to Production"
4. Verify site recovers

**Database**:
1. Use MongoDB Atlas backup
2. Restore to previous snapshot (if needed)
3. Update connection strings if changed

---

## ✅ Completion

Once all items are checked:

1. Document deployment date and time
2. Note deployed versions (Git commit SHA)
3. Save deployment URLs
4. Update team documentation
5. Monitor for 24-48 hours
6. Celebrate successful deployment! 🎉

---

## 📝 Deployment Log Template

```
Deployment Date: ________________
Deployed By: ____________________

Backend:
- Railway URL: ___________________________________
- Git Commit: ____________________________________
- Status: ________________________________________

Frontend:
- Vercel URL: ____________________________________
- Git Commit: ____________________________________
- Status: ________________________________________

Database:
- MongoDB Cluster: ______________________________
- Status: ________________________________________

Issues Encountered:
_________________________________________________
_________________________________________________

Resolution:
_________________________________________________
_________________________________________________

Notes:
_________________________________________________
_________________________________________________
```

---

**Keep this checklist handy for future deployments and updates!**
