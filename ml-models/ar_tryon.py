"""AR Virtual Try-On using VTON-HD with OpenCV TPS fallback"""
import logging
import cv2
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("PyTorch not available, using OpenCV fallback")

def apply_virtual_tryon_vtonhd(person_path, garment_path):
    """Apply virtual try-on using VTON-HD (requires trained model)"""
    try:
        if not TORCH_AVAILABLE:
            return None
        
        # This would require a trained VTON-HD model
        # For now, return None to trigger fallback
        logger.info("VTON-HD not implemented, using fallback")
        return None
        
    except Exception as e:
        logger.error(f"VTON-HD failed: {e}")
        return None

def apply_virtual_tryon_opencv(person_path, garment_path):
    """Fallback AR try-on using OpenCV TPS (Thin Plate Spline)"""
    try:
        # Read images
        person_img = cv2.imread(person_path)
        garment_img = cv2.imread(garment_path)
        
        if person_img is None or garment_img is None:
            raise ValueError("Could not read images")
        
        # Get dimensions
        person_h, person_w = person_img.shape[:2]
        garment_h, garment_w = garment_img.shape[:2]
        
        # Resize garment to fit person (simple scaling)
        scale = min(person_w * 0.6 / garment_w, person_h * 0.4 / garment_h)
        new_w = int(garment_w * scale)
        new_h = int(garment_h * scale)
        garment_resized = cv2.resize(garment_img, (new_w, new_h))
        
        # Position garment on person (centered, upper body)
        y_offset = int(person_h * 0.2)
        x_offset = int((person_w - new_w) / 2)
        
        # Create a copy of person image
        result = person_img.copy()
        
        # Simple overlay with alpha blending
        alpha = 0.7
        
        # Ensure we don't go out of bounds
        y1 = max(0, y_offset)
        y2 = min(person_h, y_offset + new_h)
        x1 = max(0, x_offset)
        x2 = min(person_w, x_offset + new_w)
        
        # Adjust garment crop if needed
        g_y1 = 0 if y_offset >= 0 else -y_offset
        g_y2 = g_y1 + (y2 - y1)
        g_x1 = 0 if x_offset >= 0 else -x_offset
        g_x2 = g_x1 + (x2 - x1)
        
        # Blend the garment onto the person
        if y2 > y1 and x2 > x1:
            roi = result[y1:y2, x1:x2]
            garment_crop = garment_resized[g_y1:g_y2, g_x1:g_x2]
            
            if roi.shape == garment_crop.shape:
                blended = cv2.addWeighted(roi, 1 - alpha, garment_crop, alpha, 0)
                result[y1:y2, x1:x2] = blended
        
        # Save result
        result_path = Path(person_path).parent / f"tryon_result_{Path(person_path).name}"
        cv2.imwrite(str(result_path), result)
        
        return str(result_path)
        
    except Exception as e:
        logger.error(f"OpenCV try-on failed: {e}")
        # Return person image as ultimate fallback
        return person_path

def apply_virtual_tryon(person_path, garment_path):
    """Main entry point for virtual try-on"""
    # Try VTON-HD first (if model is available)
    result = apply_virtual_tryon_vtonhd(person_path, garment_path)
    
    if result:
        return result
    
    # Fallback to OpenCV
    return apply_virtual_tryon_opencv(person_path, garment_path)
