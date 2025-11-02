"""Dataset preparation script for DeepFashion Category and Attribute Prediction Benchmark"""
import os
import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# DeepFashion dataset info
DATASET_INFO = {
    'name': 'DeepFashion Category and Attribute Prediction Benchmark',
    'description': 'Licensed for academic use, 800,000+ fashion images',
    'url': 'http://mmlab.ie.cuhk.edu.hk/projects/DeepFashion.html',
    'citation': 'Liu et al., DeepFashion: Powering Robust Clothes Recognition and Retrieval with Rich Annotations'
}

# Sample categories
CATEGORIES = [
    'tops', 'bottoms', 'dresses', 'outerwear', 'shoes', 'bags', 'accessories'
]

# Sample attributes
ATTRIBUTES = {
    'color': ['black', 'white', 'red', 'blue', 'green', 'yellow', 'pink', 'gray', 'brown'],
    'pattern': ['solid', 'striped', 'floral', 'geometric', 'animal_print'],
    'material': ['cotton', 'denim', 'leather', 'silk', 'wool', 'synthetic'],
    'style': ['casual', 'formal', 'sporty', 'vintage', 'modern']
}

def create_sample_metadata():
    """Create sample product metadata for demonstration"""
    products = []
    
    for i in range(100):
        product = {
            'id': f'prod-{i+1:04d}',
            'category': CATEGORIES[i % len(CATEGORIES)],
            'name': f'Fashion Item {i+1}',
            'attributes': {
                'color': ATTRIBUTES['color'][i % len(ATTRIBUTES['color'])],
                'pattern': ATTRIBUTES['pattern'][i % len(ATTRIBUTES['pattern'])],
                'material': ATTRIBUTES['material'][i % len(ATTRIBUTES['material'])],
                'style': ATTRIBUTES['style'][i % len(ATTRIBUTES['style'])]
            },
            'price': round(29.99 + (i * 5.5), 2),
            'image_filename': f'product_{i+1:04d}.jpg',
            'description': f'High-quality {CATEGORIES[i % len(CATEGORIES)]} item',
            'created_at': datetime.utcnow().isoformat()
        }
        products.append(product)
    
    return products

def prepare_dataset():
    """Prepare dataset directory structure and metadata"""
    # Get base directory
    base_dir = Path(__file__).parent
    
    # Create directories
    deepfashion_dir = base_dir / 'deepfashion'
    deepfashion_dir.mkdir(exist_ok=True)
    
    product_catalogue_dir = base_dir / 'product_catalogue'
    product_catalogue_dir.mkdir(exist_ok=True)
    
    images_dir = product_catalogue_dir / 'images'
    images_dir.mkdir(exist_ok=True)
    
    # Create README
    readme_content = f"""# StyleSense.AI Datasets

## DeepFashion Dataset

{DATASET_INFO['description']}

**Source:** {DATASET_INFO['url']}

**Citation:** {DATASET_INFO['citation']}

### Dataset Structure
- Images: 800,000+ fashion images
- Categories: 50 categories, 1,000 attributes
- Annotations: Bounding boxes, landmarks, attributes

### Usage
This dataset is licensed for academic use. To use the full dataset:
1. Visit {DATASET_INFO['url']}
2. Request access and download the dataset
3. Extract to the `deepfashion/` directory
4. Run data preprocessing scripts

### Current Status
This directory contains sample metadata for demonstration.
Full dataset should be downloaded separately due to size constraints.

## Product Catalogue

Sample product images and metadata for testing and demonstration.

### Structure
- `images/` - Product images
- `metadata.json` - Product information and attributes

Generated on: {datetime.utcnow().isoformat()}
"""
    
    readme_path = base_dir / 'README.md'
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    
    logger.info(f"Created README at {readme_path}")
    
    # Create sample metadata
    products = create_sample_metadata()
    
    metadata_path = product_catalogue_dir / 'metadata.json'
    with open(metadata_path, 'w') as f:
        json.dump({
            'dataset_info': DATASET_INFO,
            'total_products': len(products),
            'categories': CATEGORIES,
            'attributes': ATTRIBUTES,
            'products': products
        }, f, indent=2)
    
    logger.info(f"Created metadata with {len(products)} products at {metadata_path}")
    
    # Create placeholder for images
    placeholder_path = images_dir / '.gitkeep'
    placeholder_path.touch()
    
    logger.info("Dataset preparation complete!")
    logger.info(f"- DeepFashion directory: {deepfashion_dir}")
    logger.info(f"- Product catalogue: {product_catalogue_dir}")
    logger.info(f"- Images directory: {images_dir}")
    
    return {
        'deepfashion_dir': str(deepfashion_dir),
        'product_catalogue_dir': str(product_catalogue_dir),
        'metadata_file': str(metadata_path),
        'products_created': len(products)
    }

if __name__ == '__main__':
    logger.info("Starting dataset preparation...")
    result = prepare_dataset()
    logger.info(f"Preparation complete: {result}")
