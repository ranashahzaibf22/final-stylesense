"""Clothing segmentation using DeepLabV3 with OpenCV fallback"""
import logging
import cv2
import numpy as np

logger = logging.getLogger(__name__)

try:
    import torch
    import torchvision.models.segmentation as segmentation
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logger.warning("PyTorch not available, using OpenCV fallback")

def segment_clothing_deeplabv3(image_path):
    """Segment clothing using DeepLabV3"""
    try:
        if not TORCH_AVAILABLE:
            return None
        
        # Load pretrained DeepLabV3 model
        model = segmentation.deeplabv3_resnet50(pretrained=True)
        model.eval()
        
        # Read and preprocess image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")
        
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize for model input
        input_image = cv2.resize(image_rgb, (520, 520))
        input_tensor = torch.from_numpy(input_image).float()
        input_tensor = input_tensor.permute(2, 0, 1).unsqueeze(0) / 255.0
        
        # Normalize
        mean = torch.tensor([0.485, 0.456, 0.406]).view(1, 3, 1, 1)
        std = torch.tensor([0.229, 0.224, 0.225]).view(1, 3, 1, 1)
        input_tensor = (input_tensor - mean) / std
        
        # Perform segmentation
        with torch.no_grad():
            output = model(input_tensor)['out'][0]
        
        # Get segmentation mask
        output_predictions = output.argmax(0).byte().cpu().numpy()
        
        # Resize mask to original size
        mask = cv2.resize(output_predictions, (image.shape[1], image.shape[0]))
        
        # Person class is typically 15 in COCO dataset
        person_mask = (mask == 15).astype(np.uint8) * 255
        
        return {
            'mask': person_mask,
            'method': 'deeplabv3',
            'confidence': 0.85,
            'classes_detected': len(np.unique(mask))
        }
        
    except Exception as e:
        logger.error(f"DeepLabV3 segmentation failed: {e}")
        return None

def segment_clothing_opencv(image_path):
    """Fallback segmentation using OpenCV"""
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")
        
        # Convert to HSV for better color segmentation
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Create mask using color range (simple approach)
        # This is a very basic fallback
        lower_bound = np.array([0, 30, 30])
        upper_bound = np.array([180, 255, 255])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        
        # Apply morphological operations to clean up
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        
        # Find largest contour
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Create mask with largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            final_mask = np.zeros_like(mask)
            cv2.drawContours(final_mask, [largest_contour], -1, 255, -1)
        else:
            final_mask = mask
        
        return {
            'mask': final_mask,
            'method': 'opencv_fallback',
            'confidence': 0.60,
            'contours_found': len(contours) if contours else 0
        }
        
    except Exception as e:
        logger.error(f"OpenCV segmentation failed: {e}")
        # Return empty mask as ultimate fallback
        return {
            'mask': np.zeros((100, 100), dtype=np.uint8),
            'method': 'default',
            'confidence': 0.0,
            'error': str(e)
        }

def segment_clothing(image_path):
    """Main entry point for clothing segmentation"""
    # Try DeepLabV3 first
    result = segment_clothing_deeplabv3(image_path)
    
    if result:
        return result
    
    # Fallback to OpenCV
    return segment_clothing_opencv(image_path)
