# Quick Deployment Guide - Railway & Vercel

This guide provides step-by-step instructions to deploy StyleSense.AI backend on Railway and frontend on Vercel.

## 🚀 Quick Start Deployment

### Prerequisites
- GitHub account with repository access
- Railway account ([railway.app](https://railway.app))
- Vercel account ([vercel.com](https://vercel.com))
- MongoDB Atlas account (free tier available)

---

## 📦 Part 1: Backend Deployment (Railway)

### Step 1: Set Up MongoDB Atlas

1. Create a free MongoDB Atlas cluster at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Configure network access: Allow access from anywhere (0.0.0.0/0) for Railway
3. Create database user with read/write permissions
4. Get connection string:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/stylesense?retryWrites=true&w=majority
   ```

### Step 2: Deploy to Railway

1. **Sign up/Login** to [Railway](https://railway.app) using GitHub
2. **Create New Project** → "Deploy from GitHub repo"
3. **Select Repository**: ranashahzaibf22/final-stylesense
4. **Configure Root Directory**: 
   - Set root directory to: `backend`
   - Or leave empty if Railway detects it automatically

5. **Set Environment Variables** in Railway dashboard:
   
   Click on your service → Variables tab → Add these variables:

   ```bash
   # Required
   MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/stylesense
   FLASK_SECRET_KEY=your-super-secret-key-change-this-in-production
   
   # Optional but recommended
   HF_API_KEY=your_huggingface_api_key
   OPENWEATHER_API_KEY=your_openweather_api_key
   CORS_ORIGINS=https://your-frontend.vercel.app
   
   # Configuration (defaults are fine)
   FLASK_DEBUG=False
   USE_GPU=False
   ```

6. **Deploy**: Railway will automatically:
   - Detect Python project
   - Install dependencies from `requirements.txt`
   - Use `start.sh` or `Procfile` to start the application
   - Assign a public URL (e.g., `https://stylesense-backend-production.up.railway.app`)

7. **Verify Deployment**:
   - Once deployed, visit: `https://your-backend-url.railway.app/api/health`
   - You should see: `{"status": "healthy", "database": "connected", ...}`

### Troubleshooting Railway Deployment

**Issue: Build fails with "start.sh not found"**
- Solution: Ensure `start.sh` is in the backend directory and executable
- Alternative: Railway will use `Procfile` if start.sh fails

**Issue: "Application error" on startup**
- Check Railway logs: Click service → Deployments → View logs
- Verify all required environment variables are set
- Ensure MONGODB_URI is correctly formatted

**Issue: Database connection timeout**
- Verify MongoDB Atlas network access allows 0.0.0.0/0
- Check connection string format and credentials

---

## 🎨 Part 2: Frontend Deployment (Vercel)

### Step 1: Deploy to Vercel

1. **Sign up/Login** to [Vercel](https://vercel.com) using GitHub
2. **Import Project** → Select your GitHub repository
3. **Configure Project**:
   
   ```
   Framework Preset: Create React App
   Root Directory: frontend
   Build Command: npm install && npm run build
   Output Directory: build
   Install Command: npm install
   ```

4. **Set Environment Variables** in Vercel dashboard:
   
   Project Settings → Environment Variables:

   ```bash
   # Required
   REACT_APP_API_URL=https://your-backend-url.railway.app
   
   # Optional
   REACT_APP_HF_KEY=your_huggingface_key
   REACT_APP_ENABLE_CAMERA=true
   REACT_APP_ENABLE_AR_TRYON=true
   ```

5. **Deploy**: Click "Deploy"
   - Vercel will build and deploy automatically
   - You'll get a URL like: `https://stylesense-frontend.vercel.app`

6. **Update Backend CORS**:
   - Go back to Railway dashboard
   - Update `CORS_ORIGINS` to include your Vercel URL:
     ```
     CORS_ORIGINS=https://stylesense-frontend.vercel.app
     ```
   - Railway will automatically redeploy

### Troubleshooting Vercel Deployment

**Issue: Build fails - "Cannot find build output"**
- Solution: Ensure `vercel.json` specifies `outputDirectory: "build"`
- Verify `package.json` has `"build": "react-scripts build"`

**Issue: API calls fail with CORS error**
- Ensure backend CORS_ORIGINS includes your Vercel domain
- Check REACT_APP_API_URL is set correctly (no trailing slash)

**Issue: Environment variables not working**
- Ensure variables start with `REACT_APP_`
- Redeploy after adding/changing environment variables
- Check variables are set for "Production" environment

**Issue: Blank page after deployment**
- Check browser console for errors
- Verify all static assets are loading
- Ensure `public/index.html` exists

---

## ✅ Verification Checklist

After deployment, verify these endpoints:

### Backend Health Check
```bash
curl https://your-backend-url.railway.app/api/health
```
Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-11-02T...",
  "database": "connected",
  "ml_models": "available|fallback_mode",
  "version": "1.0.0"
}
```

### Frontend Access
1. Visit: `https://your-frontend-url.vercel.app`
2. Check that homepage loads
3. Open browser DevTools → Console → Check for errors
4. Verify API connection in Network tab

---

## 🔄 Continuous Deployment

Both Railway and Vercel support automatic deployments:

- **Railway**: Automatically redeploys on push to `main` branch
- **Vercel**: Automatically redeploys on push to `main` branch

To trigger manual deployment:
- Railway: Dashboard → Redeploy
- Vercel: Dashboard → Deployments → Redeploy

---

## 📊 Monitoring & Logs

### Railway Logs
- Go to: Service → Deployments → View Logs
- Real-time logs show application output
- Filter by log level: Info, Warning, Error

### Vercel Logs
- Go to: Project → Deployments → Function Logs
- View build logs and runtime logs
- Check for errors during deployment

### MongoDB Monitoring
- MongoDB Atlas → Cluster → Metrics
- Monitor connections, operations, storage

---

## 🔒 Security Best Practices

1. **Never commit sensitive data** to Git:
   - Keep `.env` files in `.gitignore`
   - Use platform environment variables

2. **Use strong secrets**:
   - Generate random FLASK_SECRET_KEY: `python -c "import secrets; print(secrets.token_hex(32))"`
   - Rotate API keys periodically

3. **Restrict CORS**:
   - Only allow your frontend domains
   - Don't use `*` in production

4. **MongoDB Security**:
   - Use strong database passwords
   - Enable IP whitelisting when possible
   - Enable MongoDB Atlas backups

---

## 🆘 Common Issues & Solutions

### Issue: Port Already in Use (Railway)
- Solution: Railway automatically assigns PORT, don't hardcode it
- Ensure code uses: `port = int(os.getenv('PORT', 5000))`

### Issue: Worker Timeout (Railway)
- Solution: Increase timeout in `start.sh` or `Procfile`
- Current setting: `--timeout 120` (120 seconds)
- For ML operations, may need higher timeout

### Issue: Out of Memory (Railway)
- Solution: Reduce number of workers
- Optimize ML model loading
- Consider upgrading Railway plan

### Issue: Build Timeout (Vercel)
- Solution: Build typically completes in 2-5 minutes
- Check for large dependencies
- Consider using `npm ci` instead of `npm install`

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Vercel Documentation](https://vercel.com/docs)
- [MongoDB Atlas Docs](https://docs.atlas.mongodb.com/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)
- [Create React App Deployment](https://create-react-app.dev/docs/deployment/)

---

## 🎉 Success!

If you've completed all steps:
- ✅ Backend is running on Railway
- ✅ Frontend is deployed on Vercel
- ✅ Database is connected
- ✅ CORS is configured
- ✅ Environment variables are set

Your StyleSense.AI application is now live! 🚀

---

**Need Help?**
- Check Railway/Vercel logs for detailed error messages
- Review environment variables configuration
- Consult the full DEPLOYMENT.md for advanced topics
