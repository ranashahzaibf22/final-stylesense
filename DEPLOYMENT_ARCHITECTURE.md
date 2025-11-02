# Deployment Architecture

This document illustrates the deployment architecture for StyleSense.AI on Railway (backend) and Vercel (frontend).

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS / BROWSERS                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           │ HTTPS
                           │
                           ▼
           ┌───────────────────────────────────┐
           │    Vercel Edge Network (CDN)      │
           │  ┌─────────────────────────────┐  │
           │  │   React Frontend (SPA)      │  │
           │  │   • Build Output: build/    │  │
           │  │   • Route: /* → index.html  │  │
           │  │   • Static Assets Cached    │  │
           │  └─────────────────────────────┘  │
           │  Environment:                     │
           │  • REACT_APP_API_URL              │
           │  • REACT_APP_HF_KEY               │
           └───────────────┬───────────────────┘
                           │
                           │ API Requests
                           │ (CORS Enabled)
                           │
                           ▼
           ┌───────────────────────────────────┐
           │    Railway.app Platform           │
           │  ┌─────────────────────────────┐  │
           │  │  Flask/Gunicorn Backend     │  │
           │  │  • Workers: 4 (default)     │  │
           │  │  • Timeout: 120s            │  │
           │  │  • Health: /api/health      │  │
           │  │  • Port: $PORT (dynamic)    │  │
           │  └─────────────────────────────┘  │
           │  Environment:                     │
           │  • MONGODB_URI                    │
           │  • FLASK_SECRET_KEY               │
           │  • CORS_ORIGINS                   │
           │  • HF_API_KEY                     │
           │  • OPENWEATHER_API_KEY            │
           └───────────────┬───────────────────┘
                           │
                           │ MongoDB Driver
                           │ (SSL/TLS)
                           │
                           ▼
           ┌───────────────────────────────────┐
           │    MongoDB Atlas (Cloud DB)       │
           │  ┌─────────────────────────────┐  │
           │  │   Database: stylesense      │  │
           │  │   Collections:              │  │
           │  │   • wardrobe                │  │
           │  │   • recommendations         │  │
           │  │   • users                   │  │
           │  │   Tier: M0 (Free)           │  │
           │  └─────────────────────────────┘  │
           │  Network Access:                  │
           │  • 0.0.0.0/0 (Railway IP)         │
           └───────────────────────────────────┘
```

## 🔄 Request Flow

### Frontend Request Flow

```
User Browser
    │
    ├─→ Static Assets (JS, CSS, Images)
    │   └─→ Vercel CDN (Cached, Fast)
    │
    └─→ API Calls (fetch/axios)
        └─→ Railway Backend
            ├─→ /api/health (Health Check)
            ├─→ /api/wardrobe/* (Wardrobe Management)
            ├─→ /api/recommendations (AI Recommendations)
            ├─→ /api/ar-tryon (Virtual Try-on)
            └─→ /api/product-catalogue (Product Data)
```

### Backend Request Flow

```
Railway Backend (Gunicorn)
    │
    ├─→ File Uploads
    │   └─→ Local Storage: backend/uploads/
    │       └─→ Validated & Processed
    │
    ├─→ Database Operations
    │   └─→ MongoDB Atlas
    │       ├─→ Insert/Update Documents
    │       ├─→ Query Collections
    │       └─→ Aggregate Results
    │
    └─→ ML Operations (if ML_AVAILABLE)
        ├─→ Body Shape Detection
        ├─→ Pose Estimation
        ├─→ Background Removal
        └─→ Outfit Recommendations
```

## 📦 Deployment Pipeline

### Frontend (Vercel)

```
GitHub Push
    │
    └─→ Vercel Webhook Triggered
        │
        ├─→ 1. Clone Repository
        │   └─→ frontend/ directory
        │
        ├─→ 2. Install Dependencies
        │   └─→ npm install (with cache)
        │
        ├─→ 3. Build
        │   └─→ npm run build
        │       └─→ Output: build/
        │           ├─→ index.html
        │           └─→ static/
        │               ├─→ js/
        │               ├─→ css/
        │               └─→ media/
        │
        ├─→ 4. Deploy to Edge Network
        │   └─→ Upload to Vercel CDN
        │       └─→ Global Distribution
        │
        └─→ 5. Assign URL
            └─→ https://<project>.vercel.app
```

### Backend (Railway)

```
GitHub Push
    │
    └─→ Railway Webhook Triggered
        │
        ├─→ 1. Clone Repository
        │   └─→ backend/ directory
        │
        ├─→ 2. Build Phase
        │   └─→ pip install -r requirements.txt
        │       └─→ Install Python dependencies
        │
        ├─→ 3. Start Service
        │   └─→ Execute: bash start.sh
        │       └─→ Start Gunicorn
        │           ├─→ Bind: 0.0.0.0:$PORT
        │           ├─→ Workers: 4
        │           ├─→ Timeout: 120s
        │           └─→ App: app:app
        │
        ├─→ 4. Health Check
        │   └─→ GET /api/health
        │       └─→ Returns: 200 OK
        │
        └─→ 5. Service Ready
            └─→ https://<project>.up.railway.app
```

## 🔐 Security Architecture

### SSL/TLS Encryption

```
User → Vercel: HTTPS (TLS 1.3)
User → Railway: HTTPS (TLS 1.3)
Railway → MongoDB: SSL/TLS Connection
```

### Authentication Flow

```
Frontend
    │
    ├─→ User Authentication (if implemented)
    │   └─→ JWT Token / Session
    │
    └─→ API Requests
        └─→ Backend validates auth
            └─→ Database operations authorized
```

### CORS Configuration

```
Railway Backend
    │
    └─→ CORS_ORIGINS setting
        ├─→ Allowed: https://<frontend>.vercel.app
        ├─→ Methods: GET, POST, PUT, DELETE
        └─→ Headers: Content-Type, Authorization
```

## 💾 Data Flow

### Upload Flow

```
User uploads image
    │
    └─→ Frontend (React)
        └─→ FormData object
            └─→ POST /api/wardrobe/upload
                │
                Railway Backend
                    │
                    ├─→ Validate file type/size
                    ├─→ Save to backend/uploads/
                    ├─→ Process with ML (optional)
                    └─→ Store metadata in MongoDB
                        └─→ Collection: wardrobe
```

### Recommendation Flow

```
User requests recommendations
    │
    └─→ Frontend (React)
        └─→ GET /api/recommendations?user_id=X
            │
            Railway Backend
                │
                ├─→ Query wardrobe items from MongoDB
                ├─→ Generate recommendations (ML)
                ├─→ Store recommendations in MongoDB
                └─→ Return JSON response
                    └─→ Frontend displays results
```

## 🌐 Environment Configuration

### Development Environment

```
Frontend: localhost:3000
    │
    └─→ REACT_APP_API_URL=http://localhost:5000

Backend: localhost:5000
    │
    ├─→ MONGODB_URI=mongodb://localhost:27017/stylesense
    ├─→ FLASK_DEBUG=True
    └─→ CORS_ORIGINS=http://localhost:3000
```

### Production Environment

```
Frontend: https://<project>.vercel.app
    │
    └─→ REACT_APP_API_URL=https://<project>.up.railway.app

Backend: https://<project>.up.railway.app
    │
    ├─→ MONGODB_URI=mongodb+srv://...@cluster.mongodb.net/stylesense
    ├─→ FLASK_DEBUG=False
    └─→ CORS_ORIGINS=https://<project>.vercel.app
```

## 📊 Monitoring & Logging

### Vercel Monitoring

```
Vercel Dashboard
    │
    ├─→ Analytics
    │   ├─→ Page Views
    │   ├─→ Performance Metrics
    │   └─→ Core Web Vitals
    │
    ├─→ Logs
    │   ├─→ Build Logs
    │   ├─→ Function Logs
    │   └─→ Error Logs
    │
    └─→ Deployments
        └─→ History & Rollback
```

### Railway Monitoring

```
Railway Dashboard
    │
    ├─→ Metrics
    │   ├─→ CPU Usage
    │   ├─→ Memory Usage
    │   └─→ Network Traffic
    │
    ├─→ Logs
    │   ├─→ Application Logs
    │   ├─→ Build Logs
    │   └─→ System Logs
    │
    └─→ Deployments
        └─→ History & Rollback
```

### MongoDB Monitoring

```
MongoDB Atlas Dashboard
    │
    ├─→ Metrics
    │   ├─→ Connections
    │   ├─→ Operations/sec
    │   └─→ Storage Usage
    │
    ├─→ Performance
    │   ├─→ Slow Queries
    │   └─→ Index Usage
    │
    └─→ Backups
        └─→ Automated snapshots
```

## 🚀 Scaling Strategy

### Horizontal Scaling

```
Low Traffic:
    Vercel: Auto-scales (edge network)
    Railway: 1 instance, 4 workers

Medium Traffic:
    Vercel: Auto-scales (edge network)
    Railway: 2-3 instances, 4 workers each

High Traffic:
    Vercel: Auto-scales (edge network)
    Railway: 5+ instances, load balanced
    MongoDB: Upgrade to M10+ cluster
```

### Performance Optimization

```
Frontend:
    ├─→ Code Splitting
    ├─→ Lazy Loading
    ├─→ Asset Optimization
    └─→ CDN Caching

Backend:
    ├─→ Database Indexing
    ├─→ Query Optimization
    ├─→ Model Caching
    └─→ Response Compression

Database:
    ├─→ Indexes on user_id, category
    ├─→ Connection pooling
    └─→ Read replicas (if needed)
```

## 🔄 CI/CD Pipeline

```
Git Push to main branch
    │
    ├─→ GitHub Actions
    │   ├─→ Lint Frontend
    │   ├─→ Lint Backend
    │   ├─→ Test Frontend
    │   ├─→ Test Backend
    │   ├─→ Build Frontend
    │   └─→ Security Scan
    │
    ├─→ Vercel Auto-Deploy
    │   └─→ Build & deploy frontend
    │       └─→ Live in ~2 minutes
    │
    └─→ Railway Auto-Deploy
        └─→ Build & deploy backend
            └─→ Live in ~3 minutes
```

## 📱 Multi-Platform Support

```
Users can access from:
    │
    ├─→ Desktop Browsers
    │   ├─→ Chrome/Edge
    │   ├─→ Firefox
    │   └─→ Safari
    │
    ├─→ Mobile Browsers
    │   ├─→ iOS Safari
    │   ├─→ Android Chrome
    │   └─→ Mobile Firefox
    │
    └─→ Tablets
        └─→ Responsive design adapts
```

## 🎯 Key Features of Architecture

1. **Fully Serverless** - No server management required
2. **Auto-Scaling** - Handles traffic spikes automatically
3. **Global CDN** - Fast content delivery worldwide
4. **High Availability** - 99.9% uptime on all platforms
5. **Secure** - HTTPS everywhere, secure database connections
6. **Monitored** - Built-in monitoring and logging
7. **CI/CD Ready** - Automatic deployments on push
8. **Cost-Effective** - Free tier available for all services

---

**This architecture ensures StyleSense.AI is scalable, secure, and performant for production use.**
