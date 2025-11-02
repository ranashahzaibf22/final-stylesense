# Common Deployment Errors & Solutions

This document provides solutions to common errors encountered during Railway (backend) and Vercel (frontend) deployment.

## 📋 Table of Contents
- [Railway Backend Errors](#railway-backend-errors)
- [Vercel Frontend Errors](#vercel-frontend-errors)
- [Database Connection Errors](#database-connection-errors)
- [CORS Errors](#cors-errors)
- [Build Errors](#build-errors)
- [Runtime Errors](#runtime-errors)

---

## 🚂 Railway Backend Errors

### Error: "Script start.sh not found"
**Symptom**: Deployment fails with "bash: start.sh: No such file or directory"

**Causes**:
1. start.sh not in backend directory
2. start.sh not executable
3. Wrong working directory

**Solutions**:
```bash
# 1. Verify file exists
ls -la backend/start.sh

# 2. Make executable (should already be done)
chmod +x backend/start.sh

# 3. Check Railway configuration
# Railway should use: bash start.sh
# Or it will automatically fall back to Procfile
```

**Alternative**: Railway will use `Procfile` if `start.sh` fails. Ensure `backend/Procfile` exists.

---

### Error: "Application Error" or 500 Internal Server Error
**Symptom**: Backend returns 500 error or "Application Error" message

**Causes**:
1. Missing environment variables
2. Database connection failure
3. Python dependency issues
4. Port binding issues

**Solutions**:

1. **Check Railway Logs**:
   - Dashboard → Your Service → Deployments → View Logs
   - Look for specific error messages

2. **Verify Environment Variables**:
   ```bash
   # Required variables in Railway:
   MONGODB_URI=mongodb+srv://...
   FLASK_SECRET_KEY=...
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

3. **Check Health Endpoint**:
   ```bash
   curl https://your-backend.railway.app/api/health
   ```

4. **Verify Database Connection**:
   - Check MongoDB Atlas network access (allow 0.0.0.0/0)
   - Test connection string locally
   - Ensure database user has read/write permissions

---

### Error: "Worker timeout" or "H12 Request timeout"
**Symptom**: Requests timeout after 30-120 seconds

**Causes**:
1. ML model loading taking too long
2. Worker timeout too short
3. Heavy computation

**Solutions**:

1. **Increase timeout in start.sh**:
   ```bash
   # Change from:
   TIMEOUT=${TIMEOUT:-120}
   
   # To:
   TIMEOUT=${TIMEOUT:-180}  # 3 minutes
   ```

2. **Optimize ML model loading**:
   - Load models lazily (on first request)
   - Use smaller models
   - Cache model instances

3. **Set WORKERS environment variable**:
   ```bash
   # In Railway dashboard
   WORKERS=2  # Reduce workers if memory limited
   ```

---

### Error: "Out of Memory"
**Symptom**: Backend crashes with OOM error

**Causes**:
1. Too many workers
2. ML models too large
3. Memory leaks

**Solutions**:

1. **Reduce workers**:
   ```bash
   # In Railway dashboard
   WORKERS=2  # Default is 4
   ```

2. **Optimize memory usage**:
   - Use `USE_GPU=False` (CPU models use less memory)
   - Lazy-load ML models
   - Clear unused model cache

3. **Upgrade Railway plan**:
   - Free tier: 512MB RAM
   - Consider paid plan for more memory

---

## 🚀 Vercel Frontend Errors

### Error: "Cannot find build output"
**Symptom**: Vercel build succeeds but deployment fails

**Causes**:
1. Wrong output directory configured
2. Build command doesn't create build/ folder
3. vercel.json misconfigured

**Solutions**:

1. **Verify Vercel Project Settings**:
   ```
   Framework Preset: Create React App
   Root Directory: frontend
   Output Directory: build
   Build Command: npm install && npm run build
   ```

2. **Check vercel.json**:
   ```json
   {
     "outputDirectory": "build",
     "buildCommand": "npm install && npm run build"
   }
   ```

3. **Test build locally**:
   ```bash
   cd frontend
   npm run build
   ls -la build/  # Should show index.html, static/, etc.
   ```

---

### Error: "Build Failed" - Module not found
**Symptom**: Build fails with "Cannot resolve module" error

**Causes**:
1. Missing dependency in package.json
2. Import path error
3. Case-sensitive file names

**Solutions**:

1. **Install missing dependencies**:
   ```bash
   cd frontend
   npm install <missing-package>
   ```

2. **Check import paths**:
   - Ensure correct relative paths
   - Check file name casing (Linux is case-sensitive)

3. **Clear cache and reinstall**:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   npm run build
   ```

---

### Error: Blank Page After Deployment
**Symptom**: Deployment succeeds but shows white/blank page

**Causes**:
1. JavaScript errors
2. API connection failure
3. Environment variables not set
4. Incorrect asset paths

**Solutions**:

1. **Check Browser Console**:
   - Open DevTools (F12)
   - Look for JavaScript errors
   - Check Network tab for failed requests

2. **Verify Environment Variables**:
   ```bash
   # Must be set in Vercel dashboard:
   REACT_APP_API_URL=https://your-backend.railway.app
   ```

3. **Check API Connection**:
   ```bash
   # Test from browser console:
   fetch('https://your-backend.railway.app/api/health')
     .then(r => r.json())
     .then(console.log)
   ```

4. **Verify homepage in package.json**:
   ```json
   {
     "homepage": "/"
   }
   ```

---

### Error: Environment Variables Not Working
**Symptom**: `process.env.REACT_APP_API_URL` is undefined

**Causes**:
1. Variables not prefixed with `REACT_APP_`
2. Not set for correct environment
3. Not redeployed after setting

**Solutions**:

1. **Check variable names**:
   ```bash
   # CORRECT:
   REACT_APP_API_URL=...
   
   # WRONG (won't work):
   API_URL=...
   ```

2. **Set for all environments**:
   - Vercel Dashboard → Settings → Environment Variables
   - Add for: Production, Preview, Development

3. **Redeploy**:
   - Vercel Dashboard → Deployments → Redeploy
   - Environment changes require redeployment

---

## 🗄️ Database Connection Errors

### Error: "MongoServerError: Authentication failed"
**Symptom**: Cannot connect to MongoDB Atlas

**Causes**:
1. Wrong username/password
2. Special characters not encoded
3. User not created/configured

**Solutions**:

1. **Check credentials**:
   - MongoDB Atlas → Database Access
   - Verify username and password

2. **URL-encode password**:
   ```python
   # If password contains special chars: @, :, /, ?, #, [, ], @
   from urllib.parse import quote_plus
   password = "p@ssw0rd!"
   encoded = quote_plus(password)  # p%40ssw0rd%21
   
   # Use in connection string:
   # mongodb+srv://user:p%40ssw0rd%21@cluster...
   ```

3. **Create database user**:
   - MongoDB Atlas → Database Access
   - Add New Database User
   - Grant "Read and write to any database"

---

### Error: "Connection timeout"
**Symptom**: Cannot connect to database, timeout after 30s

**Causes**:
1. IP not whitelisted
2. Wrong connection string
3. Network issues

**Solutions**:

1. **Check Network Access**:
   - MongoDB Atlas → Network Access
   - Ensure 0.0.0.0/0 is allowed (for Railway/Vercel)

2. **Test connection string**:
   ```bash
   # Format:
   mongodb+srv://<user>:<password>@<cluster>.mongodb.net/<database>
   
   # Must include:
   # - Username
   # - Encoded password
   # - Cluster hostname
   # - Database name
   ```

3. **Verify cluster status**:
   - MongoDB Atlas → Clusters
   - Ensure cluster is running (not paused)

---

## 🔒 CORS Errors

### Error: "No 'Access-Control-Allow-Origin' header"
**Symptom**: Frontend API calls fail with CORS error

**Causes**:
1. Backend CORS_ORIGINS not set
2. Wrong frontend URL
3. HTTP vs HTTPS mismatch
4. Trailing slashes

**Solutions**:

1. **Set CORS_ORIGINS in Railway**:
   ```bash
   # Railway Dashboard → Variables
   CORS_ORIGINS=https://your-frontend.vercel.app
   
   # Multiple origins:
   CORS_ORIGINS=https://domain1.vercel.app,https://domain2.vercel.app
   ```

2. **Verify URL format**:
   ```bash
   # CORRECT:
   https://myapp.vercel.app
   
   # WRONG:
   https://myapp.vercel.app/  # No trailing slash
   http://myapp.vercel.app    # Use https
   ```

3. **Check in browser DevTools**:
   - Network tab
   - Click failed request
   - Check Response Headers

4. **Restart backend**:
   - Railway auto-restarts when env vars change
   - Or manually redeploy

---

## 🔨 Build Errors

### Error: "npm install failed"
**Symptom**: Build fails during dependency installation

**Causes**:
1. Network issues
2. Incompatible dependencies
3. Missing package-lock.json

**Solutions**:

1. **Use npm ci instead of npm install**:
   ```json
   // vercel.json
   {
     "installCommand": "npm ci"
   }
   ```

2. **Check Node version**:
   ```bash
   # Add to package.json:
   "engines": {
     "node": "18.x",
     "npm": "9.x"
   }
   ```

3. **Clear Vercel cache**:
   - Vercel Dashboard → Settings → Clear Cache
   - Redeploy

---

### Error: "Build exceeded time limit"
**Symptom**: Build times out (10 min on Vercel free tier)

**Causes**:
1. Too many/large dependencies
2. Slow build scripts
3. Network issues

**Solutions**:

1. **Optimize dependencies**:
   ```bash
   # Remove unused dependencies
   npm uninstall <unused-package>
   
   # Use production dependencies only
   npm install --production
   ```

2. **Use caching**:
   - Vercel automatically caches node_modules
   - Ensure package-lock.json is committed

3. **Split builds**:
   - Build locally for large projects
   - Upload pre-built files

---

## 🏃 Runtime Errors

### Error: "502 Bad Gateway"
**Symptom**: Backend returns 502 error

**Causes**:
1. Backend not running
2. Wrong PORT configuration
3. Backend crashed

**Solutions**:

1. **Check Railway logs**:
   - Look for crash messages
   - Verify app is listening on PORT

2. **Verify PORT usage**:
   ```python
   # In app.py, must use:
   port = int(os.getenv('PORT', 5000))
   app.run(host='0.0.0.0', port=port)
   
   # NOT hardcoded:
   # app.run(port=5000)  # WRONG
   ```

3. **Check health endpoint**:
   ```bash
   curl https://your-backend.railway.app/api/health
   ```

---

### Error: "413 Payload Too Large"
**Symptom**: File upload fails with 413 error

**Causes**:
1. File size exceeds limit
2. Nginx/proxy limits

**Solutions**:

1. **Check Flask config**:
   ```python
   # In config.py:
   MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
   ```

2. **Client-side validation**:
   ```javascript
   // Limit file size before upload
   if (file.size > 16 * 1024 * 1024) {
     alert('File too large. Max 16MB');
     return;
   }
   ```

3. **Use Railway/Vercel limits**:
   - Railway: No specific limit (use Flask config)
   - Vercel Functions: 4.5MB request limit

---

## 🔍 Debugging Tips

### Enable Verbose Logging

**Backend (Railway)**:
```bash
# In Railway dashboard
FLASK_DEBUG=True  # Only for debugging, use False in production
LOG_LEVEL=DEBUG
```

**Check logs**:
```bash
# Railway
# Dashboard → Deployments → View Logs

# Filter by:
# - Error level
# - Time range
# - Search keywords
```

### Test Locally First

**Backend**:
```bash
cd backend
python app.py
# Test: http://localhost:5000/api/health
```

**Frontend**:
```bash
cd frontend
REACT_APP_API_URL=http://localhost:5000 npm start
# Test: http://localhost:3000
```

### Use curl for API Testing

```bash
# Health check
curl https://your-backend.railway.app/api/health

# Test upload
curl -X POST \
  -F "file=@test.jpg" \
  -F "user_id=test" \
  https://your-backend.railway.app/api/wardrobe/upload

# Test with headers
curl -H "Content-Type: application/json" \
  https://your-backend.railway.app/api/recommendations?user_id=test
```

---

## 📞 Getting Help

If you're still stuck after trying these solutions:

1. **Check service status**:
   - [Railway Status](https://status.railway.app/)
   - [Vercel Status](https://www.vercel-status.com/)
   - [MongoDB Atlas Status](https://status.mongodb.com/)

2. **Review documentation**:
   - QUICK_DEPLOY.md
   - backend/DEPLOY_README.md
   - frontend/DEPLOY_README.md
   - DEPLOYMENT.md (comprehensive guide)

3. **Check logs thoroughly**:
   - Railway deployment logs
   - Vercel function logs
   - Browser console (F12)
   - Network tab in DevTools

4. **Common patterns**:
   - Most errors are configuration issues
   - Check environment variables first
   - Verify URLs and connection strings
   - Test locally before debugging remote

---

## ✅ Verification Checklist

Before asking for help, verify:

- [ ] All environment variables set correctly
- [ ] Backend /api/health returns 200
- [ ] Frontend loads without console errors
- [ ] CORS configured with correct frontend URL
- [ ] Database connection works
- [ ] Build completes locally
- [ ] Checked all relevant logs
- [ ] URLs use https:// (not http://)
- [ ] No trailing slashes in URLs
- [ ] Used latest code from repository

---

**Remember**: Most deployment issues are configuration-related. Double-check environment variables, URLs, and connection strings before deep debugging!
