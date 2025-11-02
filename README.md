# StyleSense.AI - AI-Powered Fashion Recommendation Platform

<div align="center">

![StyleSense.AI](https://img.shields.io/badge/StyleSense.AI-Fashion%20AI-purple?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18.2-61dafb?style=for-the-badge&logo=react)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask)
![MongoDB](https://img.shields.io/badge/MongoDB-4.6-green?style=for-the-badge&logo=mongodb)

**Your AI-powered fashion companion for personalized outfit recommendations**

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [API Docs](docs/api_specification.md) • [Architecture](docs/system_design.md)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

**StyleSense.AI** is a cutting-edge full-stack application that leverages artificial intelligence to revolutionize personal fashion. The platform provides:

- 👕 **Smart Wardrobe Management**: Organize and manage your clothing collection digitally
- ✨ **AI-Powered Recommendations**: Get personalized outfit suggestions based on occasion and weather
- 📸 **AR Virtual Try-On**: See how clothes look on you before buying
- 📊 **Body Shape Analysis**: AI-powered body shape detection for better fit recommendations
- 🛍️ **Product Catalogue**: Browse and discover new fashion items

Built with modern web technologies and state-of-the-art ML models, StyleSense.AI makes fashion accessible and personalized for everyone.

---

## 🚀 Features

### Core Features

#### 1. **Wardrobe Management**
- Upload clothing items with images
- Categorize by type (tops, bottoms, dresses, etc.)
- Tag with colors and attributes
- View and manage your entire wardrobe

#### 2. **AI Recommendations**
- Context-aware outfit suggestions
- Occasion-based filtering (casual, formal, party, workout)
- Weather-adaptive recommendations
- Multiple ML models with intelligent fallbacks

#### 3. **Body Shape Analysis**
- MediaPipe-powered pose detection
- Automatic body type classification
- Measurement extraction
- OpenCV fallback for reliability

#### 4. **AR Virtual Try-On**
- Upload person and garment images
- AI-powered garment overlay
- Real-time camera integration
- Download and share results

#### 5. **Product Catalogue**
- Browse 100+ fashion items
- Category filtering
- Detailed product information
- Integration with DeepFashion dataset

### Technical Features

- **Dual-Stack Architecture**: Flask backend + React frontend
- **Multiple ML Models**: MediaPipe, Sentence Transformers, DeepLabV3
- **Intelligent Fallbacks**: Graceful degradation when ML models unavailable
- **Responsive Design**: Mobile-first Tailwind CSS implementation
- **RESTful API**: Well-documented endpoints with examples
- **MongoDB Integration**: Scalable NoSQL database
- **Security**: Input validation, file type checking, CORS protection

---

## 🛠️ Tech Stack

### Frontend
- **React 18.2**: Modern UI library
- **Tailwind CSS 3.3**: Utility-first styling
- **Axios**: HTTP client
- **MediaDevices API**: Camera integration

### Backend
- **Flask 3.0**: Python web framework
- **Flask-CORS**: Cross-origin resource sharing
- **PyMongo 4.6**: MongoDB driver
- **Python-dotenv**: Environment management

### Machine Learning
- **MediaPipe 0.10**: Body pose detection
- **OpenCV 4.8**: Computer vision
- **PyTorch 2.1**: Deep learning framework
- **Transformers 4.36**: NLP models
- **Sentence Transformers 2.2**: Semantic similarity
- **Pillow 10.1**: Image processing

### Database
- **MongoDB**: NoSQL document database
- **MongoDB Atlas**: Cloud-hosted database

### Testing
- **pytest**: Backend testing
- **Jest**: Frontend testing
- **React Testing Library**: Component testing

---

## 📁 Project Structure

```
stylesense-ai/
├── backend/
│   ├── app.py                  # Flask API server
│   ├── config.py               # Configuration management
│   ├── database.py             # MongoDB operations
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment template
│   ├── uploads/                # User-uploaded images
│   └── tests/
│       └── test_app.py         # Backend unit tests
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.js
│   │   │   ├── Wardrobe.js
│   │   │   ├── CameraCapture.js
│   │   │   ├── Recommendations.js
│   │   │   ├── ARTryOn.js
│   │   │   └── ProductCatalogue.js
│   │   ├── utils/
│   │   │   ├── api.js          # API client
│   │   │   └── camera.js       # Camera utilities
│   │   ├── styles/
│   │   │   └── index.css       # Tailwind styles
│   │   ├── App.js              # Main app component
│   │   └── index.js            # Entry point
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── tests/
│       └── App.test.js
│
├── ml-models/
│   ├── body_detection.py       # MediaPipe + fallback
│   ├── recommendation_engine.py # Transformers + rules
│   ├── ar_tryon.py             # VTON-HD + OpenCV
│   └── segmentation.py         # DeepLabV3 + fallback
│
├── datasets/
│   ├── prepare_data.py         # Dataset preparation
│   ├── README.md
│   └── product_catalogue/
│       ├── metadata.json
│       └── images/
│
├── docs/
│   ├── system_design.md        # Architecture docs
│   ├── api_specification.md    # API reference
│   └── project_timeline.md     # Development plan
│
├── .gitignore
└── README.md
```

---

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- MongoDB (local or Atlas account)
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ranashahzaibf22/final-stylesense.git
   cd final-stylesense
   ```

2. **Set up Python virtual environment**
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI and API keys
   ```

5. **Run the backend server**
   ```bash
   python app.py
   ```
   Server will start at `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```
   App will open at `http://localhost:3000`

### Dataset Preparation (Optional)

1. **Prepare sample data**
   ```bash
   cd datasets
   python prepare_data.py
   ```

2. **Download DeepFashion dataset** (optional, large files)
   - Visit [DeepFashion website](http://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html)
   - Request academic access
   - Download and extract to `datasets/deepfashion/`

---

## ⚙️ Configuration

### Backend Configuration

Create `backend/.env` file:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/stylesense
HF_API_KEY=your_huggingface_key
WEATHER_API_KEY=your_weather_key
FLASK_SECRET_KEY=your_secret_key
FLASK_DEBUG=False
CORS_ORIGINS=http://localhost:3000
USE_GPU=False
PORT=5000
```

### Frontend Configuration

Create `frontend/.env` file:

```env
REACT_APP_API_URL=http://localhost:5000/api
```

### MongoDB Setup

1. **Create MongoDB Atlas account** (free tier available)
2. **Create a cluster**
3. **Create database user**
4. **Get connection string**
5. **Update MONGODB_URI in backend/.env**

---

## 🎯 Usage

### Running the Application

1. **Start Backend**
   ```bash
   cd backend
   python app.py
   ```

2. **Start Frontend** (in new terminal)
   ```bash
   cd frontend
   npm start
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000/api
   - API Health: http://localhost:5000/api/health

### Using the Features

#### Upload Wardrobe Items
1. Navigate to "Wardrobe" section
2. Click "Select Image" and choose a clothing photo
3. Select category and color
4. Click "Upload Item"

#### Get Recommendations
1. Navigate to "Recommendations" section
2. Select occasion (casual, formal, party, etc.)
3. Select weather condition
4. Click "Get Recommendations"
5. View personalized outfit suggestions

#### AR Virtual Try-On
1. Navigate to "AR Try-On" section
2. Upload or capture your photo
3. Upload a garment image
4. Click "Try On Garment"
5. View and download the result

#### Browse Products
1. Navigate to "Catalogue" section
2. Filter by category
3. Adjust items per page
4. Click "Apply Filters"

---

## 📚 API Documentation

Full API documentation available in [API Specification](docs/api_specification.md)

### Quick Reference

#### Health Check
```bash
GET /api/health
```

#### Upload Item
```bash
POST /api/wardrobe/upload
Content-Type: multipart/form-data

file: [image file]
user_id: "user123"
category: "tops"
color: "blue"
```

#### Get Recommendations
```bash
GET /api/recommendations?user_id=user123&occasion=casual&weather=moderate
```

#### Body Shape Analysis
```bash
POST /api/body-shape/analyze
Content-Type: multipart/form-data

file: [person image]
```

#### AR Try-On
```bash
POST /api/ar-tryon
Content-Type: multipart/form-data

person_image: [person photo]
garment_image: [garment photo]
```

See [full API documentation](docs/api_specification.md) for detailed examples.

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/test_app.py -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

### Manual Testing

Use Postman collection for API testing:
1. Import API endpoints from documentation
2. Test each endpoint individually
3. Verify response formats

---

## 🚀 Deployment

### Backend Deployment (Railway)

1. Create Railway account
2. Create new project
3. Connect GitHub repository
4. Verify `railway.toml` exists at repository root (configures Docker build context)
5. Set environment variables (MONGODB_URI, FLASK_SECRET_KEY, CORS_ORIGINS)
6. Deploy

**Note**: The repository includes a `railway.toml` configuration file that ensures the Docker build uses the correct context. This prevents common build errors related to missing files.

### Frontend Deployment (Vercel)

1. Create Vercel account
2. Import Git repository
3. Configure build settings:
   - Build Command: `npm run build`
   - Output Directory: `build`
4. Set environment variables
5. Deploy

### Database (MongoDB Atlas)

1. Create production cluster
2. Configure network access
3. Update MONGODB_URI in production
4. Enable backup and monitoring

See [System Design](docs/system_design.md) for detailed deployment architecture.

---

## 📖 Documentation

- [System Design](docs/system_design.md) - Architecture and data flow
- [API Specification](docs/api_specification.md) - Complete API reference
- [Project Timeline](docs/project_timeline.md) - Development roadmap

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed for academic use. See project documentation for details.

### Dataset Attribution

This project uses the **DeepFashion Category and Attribute Prediction Benchmark** dataset:
- **Citation**: Liu et al., "DeepFashion: Powering Robust Clothes Recognition and Retrieval with Rich Annotations"
- **License**: Academic use only
- **URL**: http://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html

---

## 👥 Team

- **Project Lead**: StyleSense.AI Team
- **Version**: 1.0.0
- **Last Updated**: November 2024

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check documentation in `docs/` folder
- Review API specification

---

## 🙏 Acknowledgments

- MediaPipe by Google for pose detection
- Hugging Face for transformer models
- DeepFashion dataset by CUHK
- OpenCV community
- React and Flask communities

---

<div align="center">

**Made with ❤️ by StyleSense.AI Team**

[⬆ Back to Top](#stylesenseai---ai-powered-fashion-recommendation-platform)

</div>
