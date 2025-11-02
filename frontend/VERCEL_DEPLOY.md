# Vercel Frontend Deployment Guide

This guide explains how to deploy the StyleSense.AI frontend to Vercel with proper environment configuration.

## Prerequisites

- Vercel account (https://vercel.com)
- GitHub repository connected to Vercel
- Backend deployed on Railway (with public URL)

## Deployment Steps

### 1. Connect Repository to Vercel

1. Go to https://vercel.com
2. Click "Add New..." → "Project"
3. Import your GitHub repository (`final-stylesense`)
4. Select the `frontend` directory as the root directory
5. Vercel will auto-detect it as a Create React App project

### 2. Configure Build Settings

Vercel should auto-detect these settings, but verify:

```
Framework Preset: Create React App
Build Command: npm run build
Output Directory: build
Install Command: npm install
```

### 3. Configure Environment Variables

**CRITICAL**: Before deploying, add these environment variables in Vercel Dashboard:

Go to: Project Settings → Environment Variables

#### Required Variables

| Variable | Value | Environment |
|----------|-------|-------------|
| `REACT_APP_API_URL` | `https://your-railway-app.up.railway.app/api` | Production, Preview |
| `CI` | `false` | Production, Preview, Development |

#### Optional Variables

| Variable | Value | Environment |
|----------|-------|-------------|
| `REACT_APP_API_TIMEOUT` | `30000` | All |
| `REACT_APP_ENABLE_CAMERA` | `true` | All |
| `REACT_APP_ENABLE_AR_TRYON` | `true` | All |
| `REACT_APP_ENABLE_RECOMMENDATIONS` | `true` | All |
| `REACT_APP_HF_KEY` | `your-hf-key` | Production |

**Important Notes:**
- Replace `https://your-railway-app.up.railway.app` with your actual Railway backend URL
- The `/api` suffix is important - don't forget it!
- Set variables for all environments: Production, Preview, and Development

### 4. Deploy

1. Click "Deploy" in Vercel
2. Wait for build to complete (usually 1-3 minutes)
3. Vercel will provide a URL (e.g., `https://your-app.vercel.app`)

### 5. Update Backend CORS

**CRITICAL**: Update your backend CORS_ORIGINS to allow your Vercel domain:

In Railway → Variables → `CORS_ORIGINS`:
```
https://your-app.vercel.app,https://your-custom-domain.com
```

Then redeploy the backend.

### 6. Verify Deployment

1. Visit your Vercel URL
2. Open browser DevTools → Network tab
3. Check that API requests go to your Railway backend
4. Verify no CORS errors in console

## Troubleshooting

### Common Issues

#### 1. API Requests Failing

**Symptoms:**
- Network errors in console
- "Failed to fetch" errors
- API calls return 404

**Solutions:**
1. Verify `REACT_APP_API_URL` is set correctly in Vercel
2. Include `/api` suffix in the URL
3. Check Railway backend is running
4. Test backend health: `curl https://your-railway-app.up.railway.app/api/health`

#### 2. CORS Errors

**Symptoms:**
- "Access-Control-Allow-Origin" errors in console
- Requests blocked by CORS policy

**Solutions:**
1. Add Vercel domain to backend `CORS_ORIGINS` in Railway
2. Redeploy backend after changing CORS_ORIGINS
3. Clear browser cache and retry

#### 3. Environment Variables Not Working

**Symptoms:**
- API URL shows "localhost:5000"
- Features not working as expected

**Solutions:**
1. Verify variables are set in Vercel Dashboard
2. Variables must start with `REACT_APP_`
3. Redeploy to apply variable changes
4. Check build logs for variable values (not sensitive ones)

#### 4. Build Fails

**Symptoms:**
- Build stops with errors
- TypeScript or linting errors

**Solutions:**
1. Set `CI=false` to ignore warnings
2. Check build logs in Vercel
3. Test build locally: `npm run build`
4. Fix any code issues

#### 5. Blank Page After Deploy

**Symptoms:**
- App loads but shows blank page
- No errors in console

**Solutions:**
1. Check browser console for JavaScript errors
2. Verify all assets loaded (Network tab)
3. Check routing configuration in vercel.json
4. Clear cache and hard reload

### Checking Environment Variables

To verify environment variables are working:

1. Add this to a component temporarily:
```javascript
console.log('API URL:', process.env.REACT_APP_API_URL);
```

2. Deploy and check browser console
3. Remove debugging code after verification

## vercel.json Configuration

The `vercel.json` file configures:

1. **Rewrites**: All routes go to index.html (for SPA routing)
2. **Headers**: Cache control for static assets
3. **Build settings**: Sets CI=false to ignore warnings

### Current Configuration:
```json
{
  "version": 2,
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "framework": "create-react-app",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

## Custom Domain Setup (Optional)

1. Go to Vercel Dashboard → Project → Settings → Domains
2. Click "Add Domain"
3. Enter your custom domain
4. Follow DNS configuration instructions
5. Update backend CORS_ORIGINS with new domain

## Monitoring and Analytics

### Vercel Analytics

Enable in Project Settings → Analytics:
- Page views
- Unique visitors
- Top pages
- Load times

### Error Tracking

Consider adding:
- Sentry for error tracking
- Google Analytics for user tracking
- Custom logging to backend

## Deployment Workflow

### Automatic Deployments

Vercel automatically deploys when you:
1. Push to main branch (Production)
2. Create pull request (Preview)
3. Push to any branch (Preview)

### Manual Deployments

In Vercel Dashboard:
1. Go to Deployments tab
2. Click "..." menu on any deployment
3. Select "Redeploy"

## Environment-Specific Deployments

### Production
- Main branch deployments
- Uses Production environment variables
- Gets production domain

### Preview
- PR and branch deployments
- Uses Preview environment variables
- Gets unique preview URL

### Development
- Local development with `vercel dev`
- Uses Development environment variables

## Performance Optimization

### 1. Enable Compression
Vercel automatically compresses responses

### 2. Image Optimization
Use Vercel Image Optimization:
```javascript
import Image from 'next/image'
```

### 3. Code Splitting
React automatically splits code by routes

### 4. Caching
Static assets are cached automatically (see vercel.json)

## Security Best Practices

1. **Never expose secrets in frontend**
   - API keys should be in backend only
   - Only pass necessary tokens to frontend

2. **Use HTTPS only**
   - Vercel provides SSL automatically
   - Force HTTPS in your app

3. **Validate environment variables**
   - Check variables are set before using
   - Provide fallbacks for non-critical vars

4. **Review build logs**
   - Ensure no secrets are logged
   - Check for security warnings

## Cost

- Vercel free tier: Unlimited deployments
- No cost for hobby projects
- Pro plan available for advanced features

## Next Steps

After successful deployment:
1. ✅ Test all features end-to-end
2. ✅ Set up custom domain (optional)
3. ✅ Configure analytics
4. ✅ Set up error tracking
5. ✅ Add monitoring alerts
6. ✅ Document API endpoints for team

## Support Resources

- Vercel Documentation: https://vercel.com/docs
- Vercel Support: support@vercel.com
- Community Discord: https://vercel.com/discord
- GitHub Issues: Report bugs in repository
