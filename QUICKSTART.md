# StyleSense.AI - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB (or MongoDB Atlas free account)

### Quick Setup

#### 1. Backend Setup (2 minutes)

```bash
# Navigate to backend
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your MongoDB URI
# nano .env  # or use any text editor

# Run the backend
python app.py
```

Backend will start at `http://localhost:5000`

#### 2. Frontend Setup (2 minutes)

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

Frontend will open at `http://localhost:3000`

#### 3. Test the Application (1 minute)

1. Open browser to `http://localhost:3000`
2. Check system status on Dashboard
3. Try uploading an image to Wardrobe
4. Generate outfit recommendations

### MongoDB Setup (If you don't have MongoDB)

#### Option 1: MongoDB Atlas (Free Cloud Database)

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account
3. Create a cluster (free tier available)
4. Create a database user
5. Get your connection string
6. Update `MONGODB_URI` in `backend/.env`

#### Option 2: Local MongoDB

```bash
# On macOS
brew install mongodb-community
brew services start mongodb-community

# On Ubuntu/Debian
sudo apt-get install mongodb
sudo systemctl start mongodb

# On Windows
# Download from https://www.mongodb.com/download-center/community
# Install and start MongoDB service
```

Then use local URI in `.env`:
```
MONGODB_URI=mongodb://localhost:27017/stylesense
```

### Environment Variables

Minimal required setup in `backend/.env`:

```env
MONGODB_URI=mongodb://localhost:27017/stylesense
FLASK_SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
```

### Verify Installation

#### Check Backend Health
```bash
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "ml_models": "fallback_mode"
}
```

#### Check Frontend
Open browser to `http://localhost:3000` - you should see the Dashboard.

### Common Issues

#### Issue: "Module not found" errors
**Solution**: Make sure you installed dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

#### Issue: "Database not connected"
**Solution**: Check your MongoDB URI in `.env`
- Verify MongoDB is running (if local)
- Check connection string format
- Verify network access in MongoDB Atlas

#### Issue: Port already in use
**Solution**: Change ports in configuration
```bash
# Backend: Edit backend/.env
PORT=5001

# Frontend: Set in package.json or use
PORT=3001 npm start
```

#### Issue: CORS errors
**Solution**: Update CORS_ORIGINS in `backend/.env`
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Next Steps

1. **Upload Sample Data**
   ```bash
   cd datasets
   python prepare_data.py
   ```

2. **Explore Features**
   - Upload clothing items in Wardrobe
   - Get AI recommendations
   - Try AR virtual try-on
   - Browse product catalogue

3. **Read Documentation**
   - [API Specification](docs/api_specification.md)
   - [System Design](docs/system_design.md)
   - [Project Timeline](docs/project_timeline.md)

4. **Run Tests**
   ```bash
   # Backend tests
   cd backend
   pytest tests/test_app.py -v

   # Frontend tests
   cd frontend
   npm test
   ```

### Development Tips

#### Hot Reload
Both backend and frontend support hot reload:
- Backend: Changes auto-reload when `FLASK_DEBUG=True`
- Frontend: Changes auto-reload with npm start

#### API Testing
Use the health endpoint to verify backend:
```bash
# Check health
curl http://localhost:5000/api/health

# Test upload (with an image file)
curl -X POST http://localhost:5000/api/wardrobe/upload \
  -F "file=@/path/to/image.jpg" \
  -F "user_id=test_user" \
  -F "category=tops"
```

#### Frontend Development
The frontend is set up with proxy to backend:
```javascript
// In frontend/package.json
"proxy": "http://localhost:5000"
```

This allows calling APIs without full URL:
```javascript
// Instead of: http://localhost:5000/api/health
// Use: /api/health
```

### Project Structure

```
stylesense-ai/
├── backend/          # Flask API
├── frontend/         # React app
├── ml-models/        # AI models
├── datasets/         # Data preparation
└── docs/            # Documentation
```

### Support

- Check [README.md](README.md) for detailed documentation
- Review [docs/](docs/) for architecture and API details
- Open issues on GitHub for bugs or questions

---

**Happy Coding! 🎨✨**

Made with ❤️ by StyleSense.AI Team
