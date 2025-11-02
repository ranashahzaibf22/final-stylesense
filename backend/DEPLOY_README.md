# Backend Deployment - Railway

This directory contains the FastAPI/Flask backend for StyleSense.AI, configured for Railway deployment.

## 🚀 Deployment Files

- **`start.sh`**: Primary startup script using Gunicorn (recommended)
- **`Procfile`**: Alternative startup configuration (fallback)
- **`railway.toml`**: Railway-specific configuration
- **`requirements.txt`**: Python dependencies

## 📋 Railway Deployment Steps

### 1. Automatic Deployment
Railway automatically detects Python projects and will:
1. Install dependencies: `pip install -r requirements.txt`
2. Execute: `bash start.sh` (or use `Procfile` if start.sh fails)
3. Assign a public URL

### 2. Required Environment Variables

Set these in Railway Dashboard → Variables:

```bash
# Database (Required)
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/stylesense

# Security (Required)
FLASK_SECRET_KEY=generate-a-strong-random-key-here

# AI/ML APIs (Optional)
HF_API_KEY=your_huggingface_api_key
OPENWEATHER_API_KEY=your_openweather_api_key

# CORS (Required for frontend)
CORS_ORIGINS=https://your-frontend-url.vercel.app

# Configuration (Optional - defaults are set)
FLASK_DEBUG=False
USE_GPU=False
WORKERS=4
TIMEOUT=120
```

### 3. Verify Deployment

Once deployed, test the health endpoint:
```bash
curl https://your-backend-url.railway.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "...",
  "database": "connected",
  "ml_models": "available",
  "version": "1.0.0"
}
```

## 🔧 Configuration Details

### start.sh
- Uses **Gunicorn** WSGI server (production-ready)
- Configures 4 workers by default (adjustable via WORKERS env var)
- Sets 120s timeout for ML operations (adjustable via TIMEOUT env var)
- Binds to `0.0.0.0:$PORT` (Railway provides PORT automatically)
- Enables access and error logging

### Procfile (Fallback)
Simple one-line configuration:
```
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app
```

### railway.toml
Defines:
- Build command
- Start command
- Health check endpoint
- Restart policy

## 🐛 Troubleshooting

### Build Fails
- **Error**: "Script start.sh not found"
  - **Solution**: Ensure start.sh exists and is executable
  - **Alternative**: Railway will use Procfile automatically

### Application Error
- **Error**: Server returns 500 or crashes on startup
  - **Check**: Railway logs (Deployments → Logs)
  - **Verify**: All required environment variables are set
  - **Test**: MongoDB connection string is valid

### Database Connection Timeout
- **Error**: "Database connection failed"
  - **Check**: MongoDB Atlas network access (allow 0.0.0.0/0)
  - **Verify**: Connection string format and credentials
  - **Test**: Database user has read/write permissions

### CORS Errors
- **Error**: Frontend cannot access API
  - **Check**: CORS_ORIGINS includes frontend URL
  - **Verify**: No trailing slashes in URLs
  - **Test**: Both http and https protocols match

## 📊 Monitoring

### View Logs
Railway Dashboard → Your Service → Deployments → View Logs

### Check Metrics
Railway Dashboard → Your Service → Metrics
- CPU usage
- Memory usage
- Network traffic
- Request count

### Health Checks
Railway automatically pings `/api/health` every 30 seconds
- Restarts service if health check fails 3 times

## 🔐 Security Notes

1. **Never commit secrets**: Use environment variables
2. **Strong passwords**: Use random generated keys
3. **CORS restrictions**: Only allow specific domains
4. **HTTPS only**: Railway provides automatic SSL
5. **Regular updates**: Keep dependencies updated

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app/)
- [Gunicorn Deployment](https://docs.gunicorn.org/en/stable/deploy.html)
- [Flask Production Best Practices](https://flask.palletsprojects.com/en/latest/deploying/)

## 🆘 Need Help?

1. Check Railway logs for detailed error messages
2. Review environment variables in Railway dashboard
3. Test health endpoint: `/api/health`
4. Consult main DEPLOYMENT.md for comprehensive guide
