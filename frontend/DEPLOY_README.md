# Frontend Deployment - Vercel

This directory contains the React frontend for StyleSense.AI, optimized for Vercel deployment.

## 🚀 Deployment Files

- **`vercel.json`**: Vercel deployment configuration
- **`.vercel/project.json`**: Project-specific Vercel settings
- **`package.json`**: Build scripts and dependencies

## 📋 Vercel Deployment Steps

### 1. Automatic Deployment
Vercel automatically detects Create React App and will:
1. Install dependencies: `npm install`
2. Build production bundle: `npm run build`
3. Deploy static files from `build/` directory
4. Assign a public URL

### 2. Project Configuration

When importing to Vercel, use these settings:

```
Framework Preset: Create React App
Root Directory: frontend
Build Command: npm install && npm run build
Output Directory: build
Install Command: npm install
Node Version: 18.x
```

### 3. Required Environment Variables

Set these in Vercel Dashboard → Settings → Environment Variables:

```bash
# Backend API URL (Required)
REACT_APP_API_URL=https://your-backend-url.railway.app

# AI/ML Keys (Optional - if used in frontend)
REACT_APP_HF_KEY=your_huggingface_key

# Feature Flags (Optional)
REACT_APP_ENABLE_CAMERA=true
REACT_APP_ENABLE_AR_TRYON=true
REACT_APP_ENABLE_RECOMMENDATIONS=true

# Build Configuration
CI=false
```

**Important**: 
- Environment variables starting with `REACT_APP_` are embedded in build
- Changes require redeployment
- Set for both "Production" and "Preview" environments

### 4. Verify Deployment

Once deployed, test your frontend:
```bash
# Visit your URL
https://your-project.vercel.app

# Check API connection in browser console
# Should see API calls to your backend URL
```

## 🔧 Configuration Details

### vercel.json
Configures:
- Build command and output directory
- Static asset caching (1 year for immutable files)
- SPA routing (all routes → index.html)
- Environment variable injection

### .vercel/project.json
Defines:
- Framework detection
- Build/dev commands
- Environment variable requirements

### package.json Scripts
```json
{
  "start": "react-scripts start",    // Development server
  "build": "react-scripts build",    // Production build
  "test": "react-scripts test",      // Run tests
  "eject": "react-scripts eject"     // Eject CRA config
}
```

## 🐛 Troubleshooting

### Build Fails - "Cannot find build output"
- **Error**: Vercel can't find build artifacts
  - **Check**: `vercel.json` specifies `outputDirectory: "build"`
  - **Verify**: `package.json` has `"build"` script
  - **Test**: Run `npm run build` locally

### Blank Page After Deployment
- **Error**: White screen or no content
  - **Check**: Browser console for JavaScript errors
  - **Verify**: `REACT_APP_API_URL` is set correctly
  - **Test**: Static assets load (check Network tab)

### API Calls Fail - CORS Error
- **Error**: "CORS policy: No 'Access-Control-Allow-Origin'"
  - **Check**: Backend CORS_ORIGINS includes your Vercel URL
  - **Verify**: URL format matches (https://, no trailing slash)
  - **Test**: Backend health endpoint from browser

### Environment Variables Not Working
- **Error**: `undefined` when accessing process.env variables
  - **Check**: Variables start with `REACT_APP_` prefix
  - **Verify**: Variables set in Vercel dashboard
  - **Redeploy**: Environment changes require redeployment

### Build Timeout
- **Error**: Build exceeds time limit
  - **Check**: Dependency size (consider using `npm ci`)
  - **Optimize**: Remove unused dependencies
  - **Test**: Build time locally

## 📊 Monitoring

### View Logs
Vercel Dashboard → Deployments → Select deployment → View Function Logs

### Check Analytics
Vercel Dashboard → Analytics
- Page views
- Performance metrics
- Real User Monitoring (RUM)

### Preview Deployments
Every pull request gets a unique preview URL:
- Test changes before production
- Share with team for review
- Automatic deployment on PR update

## 🔒 Security & Performance

### Security Headers
Vercel automatically adds:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `X-XSS-Protection: 1; mode=block`

### Asset Optimization
- Automatic compression (Gzip/Brotli)
- CDN distribution (global edge network)
- Cache headers for static assets
- Image optimization available

### Environment Isolation
- Production variables ≠ Preview variables
- Separate environment for each branch
- Test changes safely before production

## 🔄 Continuous Deployment

### Automatic Deployments
- **Production**: Deploys on push to `main` branch
- **Preview**: Deploys on PR creation/update
- **Manual**: Can trigger from Vercel dashboard

### Custom Domains
1. Vercel Dashboard → Settings → Domains
2. Add your domain
3. Configure DNS records (A/CNAME)
4. Automatic SSL certificate

### Rollback
If deployment fails or has issues:
1. Vercel Dashboard → Deployments
2. Find previous working deployment
3. Click "..." → "Promote to Production"

## 🎯 Best Practices

1. **Environment Variables**
   - Keep API URLs configurable
   - Never commit secrets to Git
   - Use different values for dev/prod

2. **Build Optimization**
   - Use `npm ci` for consistent builds
   - Minimize bundle size
   - Code splitting with React.lazy()

3. **Testing**
   - Test build locally: `npm run build && serve -s build`
   - Verify all features work
   - Check mobile responsiveness

4. **Performance**
   - Optimize images
   - Lazy load components
   - Monitor Core Web Vitals

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Create React App Deployment](https://create-react-app.dev/docs/deployment/)
- [React Production Build](https://reactjs.org/docs/optimizing-performance.html)
- [Environment Variables in CRA](https://create-react-app.dev/docs/adding-custom-environment-variables/)

## 🆘 Need Help?

1. Check Vercel build logs for detailed errors
2. Review environment variables in Vercel dashboard
3. Test API connectivity from browser console
4. Consult main DEPLOYMENT.md for comprehensive guide

## ✅ Deployment Checklist

- [ ] Repository connected to Vercel
- [ ] Root directory set to `frontend`
- [ ] Build command: `npm install && npm run build`
- [ ] Output directory: `build`
- [ ] `REACT_APP_API_URL` environment variable set
- [ ] Backend CORS includes Vercel URL
- [ ] Build completes successfully
- [ ] Site loads without errors
- [ ] API calls work correctly
- [ ] All features functional
