"""Outfit recommendation engine using Sentence Transformers with fallback"""
import logging
import random
import os
import numpy as np
from datetime import datetime

logger = logging.getLogger(__name__)

try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Sentence Transformers not available, using fallback")

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.warning("Requests not available, weather API disabled")

# OpenWeatherMap API configuration
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

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
        'prefer': ['shorts', 'tank top', 't-shirt', 'sandals', 'light fabrics'],
        'avoid': ['jacket', 'sweater', 'boots', 'heavy fabrics'],
        'temp_range': (25, 45)  # Celsius
    },
    'cold': {
        'prefer': ['jacket', 'sweater', 'long pants', 'boots', 'layers'],
        'avoid': ['shorts', 'tank top', 'sandals', 'thin fabrics'],
        'temp_range': (-10, 15)
    },
    'rainy': {
        'prefer': ['jacket', 'waterproof', 'boots', 'umbrella'],
        'avoid': ['sandals', 'light fabrics', 'white clothing'],
        'temp_range': (10, 25)
    },
    'moderate': {
        'prefer': ['versatile', 'layerable'],
        'avoid': [],
        'temp_range': (15, 25)
    }
}

def get_weather_from_api(city='New York', country_code='US'):
    """
    Fetch real-time weather data from OpenWeatherMap API.
    
    Args:
        city: City name
        country_code: ISO country code
        
    Returns:
        dict with weather info or None
    """
    try:
        if not REQUESTS_AVAILABLE or not OPENWEATHER_API_KEY:
            logger.warning("Weather API not configured, using default")
            return None
        
        params = {
            'q': f"{city},{country_code}",
            'appid': OPENWEATHER_API_KEY,
            'units': 'metric'  # Use Celsius
        }
        
        response = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        
        weather_info = {
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'condition': data['weather'][0]['main'].lower(),
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'city': data['name']
        }
        
        # Classify weather
        temp = weather_info['temperature']
        condition = weather_info['condition']
        
        if 'rain' in condition or 'drizzle' in condition:
            weather_info['classification'] = 'rainy'
        elif temp > 25:
            weather_info['classification'] = 'hot'
        elif temp < 15:
            weather_info['classification'] = 'cold'
        else:
            weather_info['classification'] = 'moderate'
        
        logger.info(f"Weather: {weather_info['temperature']}°C, {weather_info['condition']} in {weather_info['city']}")
        return weather_info
        
    except Exception as e:
        logger.error(f"Weather API error: {e}")
        return None

def classify_weather_from_temp(temperature):
    """Classify weather based on temperature when API is not available"""
    if temperature > 25:
        return 'hot'
    elif temperature < 15:
        return 'cold'
    else:
        return 'moderate'

def generate_recommendations_ml(user_id, occasion, weather, user_profile=None):
    """Generate recommendations using Sentence Transformers with embeddings"""
    try:
        # Load model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get weather info if available
        weather_info = get_weather_from_api() if REQUESTS_AVAILABLE else None
        if weather_info:
            weather = weather_info['classification']
            logger.info(f"Using real-time weather: {weather}")
        
        # Create context embedding
        context = f"{occasion} outfit for {weather} weather"
        if user_profile and 'body_shape' in user_profile:
            context += f" for {user_profile['body_shape']} body shape"
        
        context_embedding = model.encode(context)
        
        # Load product catalogue with embeddings
        from pathlib import Path
        import json
        
        catalogue_path = Path(__file__).parent.parent / 'datasets' / 'product_catalogue' / 'metadata.json'
        products = []
        
        if catalogue_path.exists():
            with open(catalogue_path, 'r') as f:
                catalogue_data = json.load(f)
                products = catalogue_data.get('products', [])[:20]  # Limit for performance
        
        # Compute product embeddings
        product_embeddings = []
        for product in products:
            product_text = f"{product.get('category', '')} {product.get('name', '')} {product['attributes'].get('color', '')} {product['attributes'].get('style', '')}"
            embedding = model.encode(product_text)
            product_embeddings.append({
                'product': product,
                'embedding': embedding,
                'score': 0
            })
        
        # Compute similarity scores
        from numpy.linalg import norm
        for item in product_embeddings:
            similarity = np.dot(context_embedding, item['embedding']) / (
                norm(context_embedding) * norm(item['embedding']))
            item['score'] = float(similarity)
        
        # Sort by score
        product_embeddings.sort(key=lambda x: x['score'], reverse=True)
        
        # Generate outfit combinations
        recommendations = []
        tops = [p for p in product_embeddings if p['product'].get('category') == 'tops'][:3]
        bottoms = [p for p in product_embeddings if p['product'].get('category') == 'bottoms'][:3]
        
        for i, (top, bottom) in enumerate(zip(tops, bottoms)):
            outfit = {
                'outfit_id': f'ml-{i+1}',
                'items': [
                    {
                        'id': top['product']['id'],
                        'name': top['product']['name'],
                        'category': 'top',
                        'image': top['product'].get('image_filename'),
                        'score': top['score']
                    },
                    {
                        'id': bottom['product']['id'],
                        'name': bottom['product']['name'],
                        'category': 'bottom',
                        'image': bottom['product'].get('image_filename'),
                        'score': bottom['score']
                    }
                ],
                'occasion': occasion,
                'weather': weather,
                'confidence': (top['score'] + bottom['score']) / 2,
                'description': f"ML-generated {occasion} outfit for {weather} weather",
                'method': 'sentence_transformers',
                'weather_source': 'api' if weather_info else 'manual'
            }
            recommendations.append(outfit)
        
        logger.info(f"Generated {len(recommendations)} ML recommendations")
        return recommendations if recommendations else None
        
    except Exception as e:
        logger.error(f"ML recommendation failed: {e}")
        import traceback
        traceback.print_exc()
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

def generate_recommendations(user_id, occasion='casual', weather='moderate', user_profile=None, location=None):
    """
    Main entry point for generating recommendations with multiple strategies.
    
    Args:
        user_id: User identifier
        occasion: Event type (casual, formal, party, workout)
        weather: Weather condition or temperature
        user_profile: Optional user profile with body measurements
        location: Optional (city, country_code) tuple for weather API
        
    Returns:
        List of outfit recommendations
    """
    # Fetch real-time weather if location provided
    if location and REQUESTS_AVAILABLE:
        weather_info = get_weather_from_api(location[0], location[1])
        if weather_info:
            weather = weather_info['classification']
    
    # Try ML-based approach first
    if TRANSFORMERS_AVAILABLE:
        result = generate_recommendations_ml(user_id, occasion, weather, user_profile)
        if result:
            logger.info(f"Generated {len(result)} recommendations using ML")
            return result
    
    # Fallback to rule-based
    logger.info("Using rule-based fallback for recommendations")
    return generate_recommendations_fallback(user_id, occasion, weather)
