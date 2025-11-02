# Railway Backend Deployment Guide (Docker)

This guide explains how to deploy the StyleSense.AI backend to Railway using Docker.

## Prerequisites

- Railway account (https://railway.app)
- GitHub repository connected to Railway
- MongoDB Atlas database set up

## Deployment Steps

### 1. Connect Repository to Railway

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Select your `final-stylesense` repository
5. Railway will detect the Dockerfile automatically

### 2. Configure Environment Variables

In Railway Dashboard → Project → Variables, add the following:

**Required Variables:**
```
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/stylesense
FLASK_SECRET_KEY=your-strong-random-secret-key
CORS_ORIGINS=https://your-vercel-app.vercel.app,https://your-custom-domain.com
```

**Optional Variables:**
```
HF_API_KEY=your-huggingface-api-key
OPENWEATHER_API_KEY=your-openweather-api-key
FLASK_DEBUG=False
USE_GPU=False
WORKERS=4
TIMEOUT=120
```

**Note:** Railway automatically provides the `PORT` variable. Do not set it manually.

### 3. Deploy

1. Railway will automatically build and deploy using the Dockerfile
2. Wait for the build to complete (usually 2-5 minutes)
3. Railway will provide a public URL (e.g., `https://your-app.up.railway.app`)

### 4. Verify Deployment

Test the health endpoint:
```bash
curl https://your-app.up.railway.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000000",
  "database": "connected",
  "ml_models": "available",
  "version": "1.0.0"
}
```

## Dockerfile Details

The backend uses a multi-stage Docker build:

1. **Base Stage**: Sets up Python 3.11 slim image with system dependencies
2. **Dependencies Stage**: Installs Python packages from requirements.txt
3. **Production Stage**: Creates final image with application code

### Key Features:

- **Multi-stage build**: Reduces final image size
- **Non-root user**: Runs app as `appuser` for security
- **Optimized caching**: Dependencies are cached separately from app code
- **Production-ready**: Uses Gunicorn with optimized settings

## Troubleshooting

### Build Fails

1. Check Railway build logs
2. Verify all required files are present (requirements.txt, app.py, etc.)
3. Ensure system dependencies are correct in Dockerfile

### App Crashes on Start

1. Check Railway logs: Dashboard → Deployments → View Logs
2. Verify environment variables are set correctly
3. Check database connection string
4. Ensure PORT variable is not manually set

### API Not Responding

1. Verify the health endpoint works
2. Check CORS_ORIGINS includes your frontend URL
3. Review application logs for errors

### Database Connection Issues

1. Verify MONGODB_URI is correct
2. Ensure MongoDB Atlas allows connections from Railway IPs (0.0.0.0/0)
3. Check database user credentials

## Railway Configuration Files

The following files are used for Railway deployment:

- `../railway.toml` - Railway-specific configuration at repository root (REQUIRED for Docker builds)
  - Configures Docker builder
  - Sets dockerfilePath to `backend/Dockerfile`
  - Sets dockerContext to `backend` directory
  - This prevents "requirements.txt not found" errors
- `Dockerfile` - Docker build configuration (primary)
- `.dockerignore` - Files to exclude from Docker build
- `railway.toml` - Backend-specific Railway configuration (contains environment variable documentation)
- `Procfile` - Fallback if Docker build fails
- `start.sh` - Startup script used by Docker

**Important**: The root-level `railway.toml` is essential for correct Docker builds. It ensures Railway uses the backend directory as the build context. The backend-level `railway.toml` provides additional configuration and documentation but is overridden by the root configuration.

## Monitoring

### Health Checks

Railway automatically monitors the `/api/health` endpoint (configured in railway.toml).

### Logs

Access logs in Railway Dashboard:
- Deployment logs: Shows build process
- Application logs: Shows runtime logs (stdout/stderr)

### Metrics

Railway provides:
- CPU usage
- Memory usage
- Network traffic
- Build time

## Updating the Deployment

1. Push changes to GitHub
2. Railway automatically detects changes and rebuilds
3. Zero-downtime deployment (new version replaces old)

## Cost Optimization

- Railway free tier: 500 hours/month
- Reduce workers if traffic is low (set WORKERS=2)
- Use smaller timeout values for faster worker recycling
- Consider disabling ML features if not needed (reduces memory)

## Security Best Practices

1. Never commit .env files
2. Use strong FLASK_SECRET_KEY
3. Restrict CORS_ORIGINS to your frontend domains only
4. Keep dependencies updated
5. Review Railway build logs for sensitive data exposure
6. Use Railway's encrypted environment variables

## Next Steps

After deploying the backend:
1. Update frontend REACT_APP_API_URL with Railway URL
2. Deploy frontend to Vercel
3. Test end-to-end functionality
4. Set up monitoring and alerts
