"""Configuration management for StyleSense.AI backend"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    
    # MongoDB settings
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/stylesense')
    
    # API Keys
    HF_API_KEY = os.getenv('HF_API_KEY', '')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    
    # File upload settings
    UPLOAD_FOLDER = Path(__file__).parent / 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # ML Model settings
    USE_GPU = os.getenv('USE_GPU', 'False').lower() in ('true', '1', 't')
    MODEL_CACHE_DIR = Path(__file__).parent.parent / 'ml-models' / 'cache'
    
    @staticmethod
    def init_app():
        """Initialize application directories"""
        Config.UPLOAD_FOLDER.mkdir(exist_ok=True)
        Config.MODEL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
