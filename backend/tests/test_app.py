"""Unit tests for Flask API"""
import pytest
import json
import sys
from pathlib import Path
from io import BytesIO

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.app import app
from backend.config import Config

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    Config.UPLOAD_FOLDER = Path(__file__).parent / 'test_uploads'
    Config.UPLOAD_FOLDER.mkdir(exist_ok=True)
    
    with app.test_client() as client:
        yield client
    
    # Cleanup
    import shutil
    if Config.UPLOAD_FOLDER.exists():
        shutil.rmtree(Config.UPLOAD_FOLDER)

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'database' in data
    assert 'ml_models' in data

def test_wardrobe_upload_no_file(client):
    """Test wardrobe upload without file"""
    response = client.post('/api/wardrobe/upload')
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert 'error' in data

def test_wardrobe_upload_invalid_file(client):
    """Test wardrobe upload with invalid file type"""
    data = {
        'file': (BytesIO(b'test content'), 'test.txt')
    }
    response = client.post('/api/wardrobe/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    
    result = json.loads(response.data)
    assert 'error' in result

def test_wardrobe_upload_valid_file(client):
    """Test wardrobe upload with valid image"""
    # Create a simple 1x1 PNG image
    import struct
    
    # Minimal PNG header
    png_data = (
        b'\x89PNG\r\n\x1a\n'  # PNG signature
        b'\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89'
        b'\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4'
        b'\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    
    data = {
        'file': (BytesIO(png_data), 'test.png'),
        'user_id': 'test_user',
        'category': 'tops',
        'color': 'blue'
    }
    response = client.post('/api/wardrobe/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 201
    
    result = json.loads(response.data)
    assert result['success'] is True
    assert 'data' in result

def test_get_recommendations(client):
    """Test recommendations endpoint"""
    response = client.get('/api/recommendations?user_id=test_user&occasion=casual&weather=moderate')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'recommendations' in data
    assert len(data['recommendations']) > 0

def test_body_shape_analyze_no_file(client):
    """Test body shape analysis without file"""
    response = client.post('/api/body-shape/analyze')
    assert response.status_code == 400

def test_product_catalogue(client):
    """Test product catalogue endpoint"""
    response = client.get('/api/product-catalogue?category=tops&limit=5')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'products' in data
    assert len(data['products']) > 0

def test_404_error(client):
    """Test 404 error handling"""
    response = client.get('/api/nonexistent')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data

def test_ar_tryon_missing_files(client):
    """Test AR try-on without required files"""
    response = client.post('/api/ar-tryon')
    assert response.status_code == 400
    
    data = json.loads(response.data)
    assert 'error' in data
