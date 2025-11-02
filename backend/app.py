"""Flask API for StyleSense.AI"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from pathlib import Path
import logging
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config import Config
from backend.database import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
Config.init_app()

# Enable CORS
CORS(app, origins=Config.CORS_ORIGINS)

# Import ML modules (with fallback if not available)
try:
    from ml_models.body_detection import detect_body_shape
    from ml_models.recommendation_engine import generate_recommendations
    from ml_models.ar_tryon import apply_virtual_tryon
    from ml_models.segmentation import segment_clothing
    ML_AVAILABLE = True
except ImportError as e:
    logger.warning(f"ML modules not available: {e}. Using fallback implementations.")
    ML_AVAILABLE = False

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def validate_image(file):
    """Validate uploaded image file"""
    if not file or file.filename == '':
        return False, "No file provided"
    
    if not allowed_file(file.filename):
        return False, f"Invalid file type. Allowed: {', '.join(Config.ALLOWED_EXTENSIONS)}"
    
    return True, "Valid"

@app.route('/api/health', methods=['GET'])
def health_check():
    """System health check endpoint"""
    db_status = 'connected' if db.db is not None else 'disconnected'
    ml_status = 'available' if ML_AVAILABLE else 'fallback_mode'
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': db_status,
        'ml_models': ml_status,
        'version': '1.0.0'
    })

@app.route('/api/wardrobe/upload', methods=['POST'])
def upload_wardrobe_item():
    """Upload and store wardrobe item"""
    try:
        # Get file from request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        valid, message = validate_image(file)
        
        if not valid:
            return jsonify({'error': message}), 400
        
        # Secure filename and save
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        filepath = Config.UPLOAD_FOLDER / unique_filename
        file.save(str(filepath))
        
        # Get additional metadata from form
        user_id = request.form.get('user_id', 'default_user')
        category = request.form.get('category', 'uncategorized')
        color = request.form.get('color', 'unknown')
        
        # Store in database
        item_data = {
            'filename': unique_filename,
            'original_filename': filename,
            'category': category,
            'color': color,
            'upload_date': datetime.utcnow(),
            'file_path': str(filepath)
        }
        
        if db.db is not None:
            item_id = db.insert_wardrobe_item(user_id, item_data)
            item_data['id'] = item_id
        
        logger.info(f"Uploaded wardrobe item: {unique_filename}")
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully',
            'data': item_data
        }), 201
        
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/wardrobe/<user_id>', methods=['GET'])
def get_wardrobe(user_id):
    """Get all wardrobe items for a user"""
    try:
        if db.db is None:
            return jsonify({'error': 'Database not connected'}), 503
        
        items = db.get_wardrobe_items(user_id)
        
        return jsonify({
            'success': True,
            'count': len(items),
            'items': items
        })
        
    except Exception as e:
        logger.error(f"Error fetching wardrobe: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    """Generate outfit recommendations"""
    try:
        user_id = request.args.get('user_id', 'default_user')
        occasion = request.args.get('occasion', 'casual')
        weather = request.args.get('weather', 'moderate')
        
        # Generate recommendations using ML or fallback
        if ML_AVAILABLE:
            recommendations = generate_recommendations(user_id, occasion, weather)
        else:
            # Fallback: simple rule-based recommendations
            recommendations = [
                {
                    'outfit_id': 1,
                    'items': ['top-001', 'bottom-001'],
                    'occasion': occasion,
                    'confidence': 0.85,
                    'description': f'Casual {occasion} outfit'
                }
            ]
        
        if db.db is not None:
            for rec in recommendations:
                rec['created_at'] = datetime.utcnow()
                db.insert_recommendation(user_id, rec)
        
        return jsonify({
            'success': True,
            'user_id': user_id,
            'recommendations': recommendations
        })
        
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/body-shape/analyze', methods=['POST'])
def analyze_body_shape():
    """Analyze body shape from image"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        valid, message = validate_image(file)
        
        if not valid:
            return jsonify({'error': message}), 400
        
        # Save temporarily
        filename = secure_filename(file.filename)
        temp_path = Config.UPLOAD_FOLDER / f"temp_{filename}"
        file.save(str(temp_path))
        
        # Analyze body shape
        if ML_AVAILABLE:
            analysis = detect_body_shape(str(temp_path))
        else:
            # Fallback: basic analysis
            analysis = {
                'body_type': 'average',
                'measurements': {
                    'shoulders': 'medium',
                    'waist': 'medium',
                    'hips': 'medium'
                },
                'confidence': 0.75,
                'method': 'fallback'
            }
        
        # Clean up temp file
        temp_path.unlink()
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
        
    except Exception as e:
        logger.error(f"Error analyzing body shape: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ar-tryon', methods=['POST'])
def ar_tryon():
    """Apply AR virtual try-on"""
    try:
        if 'person_image' not in request.files or 'garment_image' not in request.files:
            return jsonify({'error': 'Both person_image and garment_image required'}), 400
        
        person_file = request.files['person_image']
        garment_file = request.files['garment_image']
        
        # Validate both files
        for file in [person_file, garment_file]:
            valid, message = validate_image(file)
            if not valid:
                return jsonify({'error': message}), 400
        
        # Save temporarily
        person_path = Config.UPLOAD_FOLDER / f"temp_person_{secure_filename(person_file.filename)}"
        garment_path = Config.UPLOAD_FOLDER / f"temp_garment_{secure_filename(garment_file.filename)}"
        
        person_file.save(str(person_path))
        garment_file.save(str(garment_path))
        
        # Apply virtual try-on
        if ML_AVAILABLE:
            result_path = apply_virtual_tryon(str(person_path), str(garment_path))
        else:
            # Fallback: return original person image
            result_path = str(person_path)
        
        # Clean up temp files
        person_path.unlink()
        garment_path.unlink()
        
        return jsonify({
            'success': True,
            'result_url': f'/api/uploads/{Path(result_path).name}',
            'method': 'ml' if ML_AVAILABLE else 'fallback'
        })
        
    except Exception as e:
        logger.error(f"Error in AR try-on: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/product-catalogue', methods=['GET'])
def get_product_catalogue():
    """Get product catalogue with images and metadata"""
    try:
        category = request.args.get('category', None)
        limit = int(request.args.get('limit', 50))
        
        # Load products from catalogue
        catalogue_path = Path(__file__).parent.parent / 'datasets' / 'product_catalogue'
        products = []
        
        # Mock products for demonstration
        for i in range(min(limit, 10)):
            products.append({
                'id': f'prod-{i+1:03d}',
                'name': f'Fashion Item {i+1}',
                'category': category or 'tops',
                'price': 29.99 + (i * 10),
                'image_url': f'/api/catalogue/images/product_{i+1}.jpg',
                'description': f'Stylish {category or "fashion"} item'
            })
        
        return jsonify({
            'success': True,
            'count': len(products),
            'products': products
        })
        
    except Exception as e:
        logger.error(f"Error fetching catalogue: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/uploads/<filename>')
def serve_upload(filename):
    """Serve uploaded files"""
    return send_from_directory(Config.UPLOAD_FOLDER, filename)

@app.errorhandler(413)
def file_too_large(e):
    """Handle file size limit exceeded"""
    return jsonify({'error': 'File too large. Maximum size is 16MB'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Connect to database
    if not db.connect():
        logger.warning("Running without database connection")
    
    # Run the app
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)
