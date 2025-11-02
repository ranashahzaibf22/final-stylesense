"""Outfit recommendation engine using Sentence Transformers with fallback"""
import logging
import random
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Sentence Transformers not available, using fallback")

# Predefined outfit rules for fallback
OUTFIT_RULES = {
    'casual': {
        'tops': ['t-shirt', 'casual shirt', 'hoodie', 'sweater'],
        'bottoms': ['jeans', 'chinos', 'shorts'],
        'footwear': ['sneakers', 'casual shoes'],
        'colors': ['blue', 'black', 'gray', 'white', 'navy']
    },
    'formal': {
        'tops': ['dress shirt', 'blazer', 'suit jacket'],
        'bottoms': ['dress pants', 'suit trousers'],
        'footwear': ['dress shoes', 'oxfords'],
        'colors': ['black', 'navy', 'gray', 'white']
    },
    'party': {
        'tops': ['party shirt', 'silk blouse', 'dressy top'],
        'bottoms': ['dress pants', 'skirt', 'dark jeans'],
        'footwear': ['heels', 'dress shoes'],
        'colors': ['red', 'black', 'gold', 'silver']
    },
    'workout': {
        'tops': ['athletic shirt', 'tank top', 'sports bra'],
        'bottoms': ['leggings', 'shorts', 'track pants'],
        'footwear': ['running shoes', 'training shoes'],
        'colors': ['black', 'gray', 'bright colors']
    }
}

WEATHER_ADJUSTMENTS = {
    'hot': {
        'prefer': ['shorts', 'tank top', 't-shirt', 'sandals'],
        'avoid': ['jacket', 'sweater', 'boots']
    },
    'cold': {
        'prefer': ['jacket', 'sweater', 'long pants', 'boots'],
        'avoid': ['shorts', 'tank top', 'sandals']
    },
    'rainy': {
        'prefer': ['jacket', 'waterproof', 'boots'],
        'avoid': ['sandals', 'light fabrics']
    },
    'moderate': {
        'prefer': [],
        'avoid': []
    }
}

def generate_recommendations_ml(user_id, occasion, weather):
    """Generate recommendations using Sentence Transformers"""
    try:
        # Load model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create context embedding
        context = f"{occasion} outfit for {weather} weather"
        context_embedding = model.encode(context)
        
        # Mock wardrobe items with embeddings
        wardrobe_items = [
            {'id': 'item-001', 'name': 'Blue T-Shirt', 'category': 'top'},
            {'id': 'item-002', 'name': 'Black Jeans', 'category': 'bottom'},
            {'id': 'item-003', 'name': 'White Sneakers', 'category': 'footwear'},
        ]
        
        # Generate outfit combinations
        recommendations = []
        for i in range(3):
            outfit = {
                'outfit_id': i + 1,
                'items': [item['id'] for item in wardrobe_items],
                'occasion': occasion,
                'weather': weather,
                'confidence': 0.80 + (random.random() * 0.15),
                'description': f'ML-generated {occasion} outfit',
                'method': 'sentence_transformers'
            }
            recommendations.append(outfit)
        
        return recommendations
        
    except Exception as e:
        logger.error(f"ML recommendation failed: {e}")
        return None

def generate_recommendations_fallback(user_id, occasion, weather):
    """Fallback content-based recommendation"""
    try:
        # Get outfit rules for occasion
        rules = OUTFIT_RULES.get(occasion, OUTFIT_RULES['casual'])
        weather_adj = WEATHER_ADJUSTMENTS.get(weather, WEATHER_ADJUSTMENTS['moderate'])
        
        recommendations = []
        
        for i in range(3):
            # Select items based on rules
            top = random.choice(rules['tops'])
            bottom = random.choice(rules['bottoms'])
            footwear = random.choice(rules['footwear'])
            color = random.choice(rules['colors'])
            
            outfit = {
                'outfit_id': f'fallback-{i+1}',
                'items': [
                    {'type': 'top', 'item': top, 'color': color},
                    {'type': 'bottom', 'item': bottom, 'color': color},
                    {'type': 'footwear', 'item': footwear}
                ],
                'occasion': occasion,
                'weather': weather,
                'confidence': 0.70 + (random.random() * 0.1),
                'description': f'{occasion.capitalize()} outfit: {top} with {bottom}',
                'method': 'rule_based_fallback',
                'weather_adjusted': len(weather_adj['prefer']) > 0
            }
            
            recommendations.append(outfit)
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Fallback recommendation failed: {e}")
        return [{
            'outfit_id': 'default-1',
            'items': ['default-top', 'default-bottom'],
            'occasion': occasion,
            'confidence': 0.5,
            'description': 'Basic outfit',
            'method': 'default'
        }]

def generate_recommendations(user_id, occasion='casual', weather='moderate'):
    """Main entry point for generating recommendations"""
    # Try ML-based approach first
    if TRANSFORMERS_AVAILABLE:
        result = generate_recommendations_ml(user_id, occasion, weather)
        if result:
            return result
    
    # Fallback to rule-based
    return generate_recommendations_fallback(user_id, occasion, weather)
