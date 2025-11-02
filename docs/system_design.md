# StyleSense.AI - System Design Document

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Database Schema](#database-schema)
4. [API Flows](#api-flows)
5. [Data Flow Diagrams](#data-flow-diagrams)
6. [Technology Stack](#technology-stack)

## Overview

StyleSense.AI is an AI-powered fashion recommendation platform that provides personalized outfit suggestions, virtual try-on capabilities, and a comprehensive wardrobe management system.

### Key Features
- **Wardrobe Management**: Upload and organize clothing items
- **AI Recommendations**: Context-aware outfit suggestions based on occasion and weather
- **Body Shape Analysis**: MediaPipe-powered body shape detection
- **AR Virtual Try-On**: VTON-HD with OpenCV fallback for garment visualization
- **Product Catalogue**: Browse fashion items with metadata

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │Dashboard │  │ Wardrobe │  │   AR     │  │Catalogue │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│         React + Tailwind CSS + Axios                        │
└─────────────────────────────────────────────────────────────┘
                            │
                   REST API (HTTPS)
                            │
┌─────────────────────────────────────────────────────────────┐
│                      Backend Layer                           │
│                    Flask API Server                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Endpoints: /wardrobe, /recommendations, /ar-tryon    │  │
│  │            /body-shape, /product-catalogue           │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
           │                           │
    ┌──────┴──────┐           ┌───────┴────────┐
    │   MongoDB   │           │   ML Models    │
    │   Database  │           │                │
    └─────────────┘           │ • MediaPipe    │
                              │ • Transformers │
                              │ • OpenCV       │
                              │ • PyTorch      │
                              └────────────────┘
```

### Component Breakdown

#### Frontend Components
- **Dashboard**: System overview and quick actions
- **Wardrobe**: Upload and manage clothing items
- **CameraCapture**: Live camera and gallery upload
- **Recommendations**: Display AI-generated outfit suggestions
- **ARTryOn**: Virtual garment try-on interface
- **ProductCatalogue**: Browse product database

#### Backend Services
- **Flask API**: RESTful endpoints for all operations
- **File Management**: Secure image upload and storage
- **Authentication**: Session management (future enhancement)
- **Error Handling**: Comprehensive error responses

#### ML Models
- **Body Detection**: MediaPipe Pose + OpenCV fallback
- **Recommendation Engine**: Sentence Transformers + rule-based fallback
- **AR Try-On**: VTON-HD + OpenCV TPS fallback
- **Segmentation**: DeepLabV3 + OpenCV fallback

## Database Schema

### MongoDB Collections

#### wardrobe
```javascript
{
  _id: ObjectId,
  user_id: String,
  filename: String,
  original_filename: String,
  category: String,  // tops, bottoms, dresses, etc.
  color: String,
  upload_date: ISODate,
  file_path: String,
  metadata: {
    pattern: String,
    material: String,
    style: String
  }
}
```

#### recommendations
```javascript
{
  _id: ObjectId,
  user_id: String,
  outfit_id: String,
  items: Array,  // Array of item IDs or descriptions
  occasion: String,  // casual, formal, party, etc.
  weather: String,  // hot, cold, rainy, moderate
  confidence: Number,  // 0.0 - 1.0
  description: String,
  created_at: ISODate,
  method: String  // ml, rule_based, fallback
}
```

#### users (future)
```javascript
{
  _id: ObjectId,
  username: String,
  email: String,
  preferences: {
    style: Array,
    favorite_colors: Array,
    body_shape: String
  },
  created_at: ISODate
}
```

## API Flows

### 1. Wardrobe Upload Flow
```
Client                 API                Database           Storage
  │                     │                    │                  │
  │  POST /wardrobe/    │                    │                  │
  │    upload          │                    │                  │
  ├───────────────────>│                    │                  │
  │                     │  Validate Image    │                  │
  │                     │                    │                  │
  │                     │  Save File         │                  │
  │                     ├────────────────────┼─────────────────>│
  │                     │                    │                  │
  │                     │  Insert Document   │                  │
  │                     ├───────────────────>│                  │
  │                     │                    │                  │
  │  <Success Response> │                    │                  │
  │<────────────────────┤                    │                  │
```

### 2. Recommendation Flow
```
Client                 API            ML Models         Database
  │                     │                 │                │
  │  GET /recommend-    │                 │                │
  │    ations?occasion  │                 │                │
  ├───────────────────>│                 │                │
  │                     │  Get User Items │                │
  │                     ├────────────────────────────────>│
  │                     │                 │                │
  │                     │  Generate       │                │
  │                     │  Recommendations│                │
  │                     ├────────────────>│                │
  │                     │<────────────────┤                │
  │                     │                 │                │
  │                     │  Store Results  │                │
  │                     ├────────────────────────────────>│
  │                     │                 │                │
  │  <Recommendations>  │                 │                │
  │<────────────────────┤                 │                │
```

### 3. AR Try-On Flow
```
Client                 API            ML Models         Storage
  │                     │                 │                │
  │  POST /ar-tryon     │                 │                │
  │    (person+garment) │                 │                │
  ├───────────────────>│                 │                │
  │                     │  Save Temp Files│                │
  │                     ├────────────────────────────────>│
  │                     │                 │                │
  │                     │  Apply Try-On   │                │
  │                     ├────────────────>│                │
  │                     │<────────────────┤                │
  │                     │                 │                │
  │  <Result URL>       │  Clean Temp     │                │
  │<────────────────────┤                 │                │
```

## Data Flow Diagrams

### User Interaction Flow
```
┌──────────┐
│  User    │
└────┬─────┘
     │
     ├──> Upload Photo ──> Wardrobe Storage
     │
     ├──> Request Recommendations ──> ML Processing ──> Display Outfits
     │
     ├──> AR Try-On ──> Image Processing ──> Show Result
     │
     └──> Browse Catalogue ──> Product Database ──> Display Items
```

### ML Pipeline Flow
```
Input Image
    │
    ├──> Preprocessing (resize, normalize)
    │
    ├──> Feature Extraction
    │         │
    │         ├──> Body Detection (MediaPipe)
    │         ├──> Clothing Segmentation (DeepLabV3)
    │         └──> Attribute Recognition
    │
    ├──> Recommendation Engine
    │         │
    │         ├──> Context Analysis (occasion, weather)
    │         ├──> Similarity Matching (Sentence Transformers)
    │         └──> Rule-based Filtering
    │
    └──> Output Generation
              │
              ├──> Outfit Combinations
              ├──> Confidence Scores
              └──> Descriptions
```

## Technology Stack

### Frontend
- **Framework**: React 18.2
- **Styling**: Tailwind CSS 3.3
- **HTTP Client**: Axios
- **Camera API**: MediaDevices getUserMedia
- **Build Tool**: Create React App

### Backend
- **Framework**: Flask 3.0
- **Database**: MongoDB (PyMongo 4.6)
- **File Upload**: Werkzeug
- **CORS**: Flask-CORS
- **Environment**: python-dotenv

### ML/AI
- **Body Detection**: MediaPipe 0.10
- **Computer Vision**: OpenCV 4.8
- **Deep Learning**: PyTorch 2.1
- **NLP**: Transformers 4.36, Sentence Transformers 2.2
- **Image Processing**: Pillow 10.1, NumPy 1.24

### Testing
- **Backend**: pytest, pytest-flask
- **Frontend**: Jest, React Testing Library

### Deployment
- **Backend**: Railway / Heroku
- **Frontend**: Vercel / Netlify
- **Database**: MongoDB Atlas
- **Storage**: Cloud storage (future)

## Security Considerations

### Input Validation
- File type checking (images only)
- File size limits (16MB max)
- Filename sanitization
- MIME type verification

### API Security
- CORS configuration
- Request rate limiting (future)
- Input sanitization
- Error message sanitization

### Data Protection
- Environment variables for secrets
- Secure MongoDB connections
- HTTPS for all API calls (production)
- User data isolation

## Scalability

### Horizontal Scaling
- Stateless API design
- Database connection pooling
- Load balancing ready
- CDN for static assets

### Performance Optimization
- Image compression
- Model caching
- Database indexing
- Lazy loading on frontend

### Future Enhancements
- Redis for caching
- Message queue for async tasks
- Microservices architecture
- Kubernetes deployment

## Monitoring & Logging

### Health Checks
- `/api/health` endpoint
- Database connectivity
- ML model availability

### Logging
- Request/response logging
- Error tracking
- Performance metrics
- User activity tracking (future)

---

**Version**: 1.0.0  
**Last Updated**: November 2024  
**Maintainer**: StyleSense.AI Team
