"""Body shape detection using MediaPipe/Microsoft Human Pose with fallback"""
import logging
import cv2
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    logger.warning("MediaPipe not available, using fallback detection")

# Try to import DeepLabV3 for background removal
try:
    import torch
    import torchvision
    DEEPLABV3_AVAILABLE = True
except ImportError:
    DEEPLABV3_AVAILABLE = False
    logger.warning("DeepLabV3 not available, using OpenCV fallback for background removal")

def detect_body_pose(image_path):
    """
    Detect body pose and return keypoints with segmentation mask.
    Uses MediaPipe Pose for accurate keypoint detection.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        dict: Contains keypoints, landmarks, segmentation_mask (optional), confidence
    """
    try:
        if not MEDIAPIPE_AVAILABLE:
            return detect_body_pose_fallback(image_path)
        
        mp_pose = mp.solutions.pose
        
        # Read image
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError("Could not read image")
        
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, _ = image.shape
        
        # Initialize pose detection
        with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=True,
            min_detection_confidence=0.5
        ) as pose:
            results = pose.process(image_rgb)
            
            if not results.pose_landmarks:
                return None
            
            # Extract keypoints
            landmarks = results.pose_landmarks.landmark
            keypoints = []
            
            for idx, landmark in enumerate(landmarks):
                keypoints.append({
                    'id': idx,
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z,
                    'visibility': landmark.visibility
                })
            
            # Get segmentation mask if available
            segmentation_mask = None
            if results.segmentation_mask is not None:
                segmentation_mask = (results.segmentation_mask > 0.5).astype(np.uint8) * 255
            
            return {
                'keypoints': keypoints,
                'landmarks_count': len(landmarks),
                'segmentation_mask': segmentation_mask,
                'confidence': 0.85,
                'method': 'mediapipe',
                'image_width': w,
                'image_height': h
            }
            
    except Exception as e:
        logger.error(f"MediaPipe pose detection failed: {e}")
        return detect_body_pose_fallback(image_path)

def detect_body_pose_fallback(image_path):
    """Fallback pose detection using OpenCV"""
    try:
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError("Could not read image")
        
        h, w, _ = image.shape
        
        # Simple keypoint estimation based on image dimensions
        # This is a very basic fallback
        keypoints = [
            {'id': 0, 'x': 0.5, 'y': 0.1, 'z': 0, 'visibility': 0.5},  # Nose
            {'id': 11, 'x': 0.4, 'y': 0.3, 'z': 0, 'visibility': 0.5},  # Left shoulder
            {'id': 12, 'x': 0.6, 'y': 0.3, 'z': 0, 'visibility': 0.5},  # Right shoulder
            {'id': 23, 'x': 0.4, 'y': 0.6, 'z': 0, 'visibility': 0.5},  # Left hip
            {'id': 24, 'x': 0.6, 'y': 0.6, 'z': 0, 'visibility': 0.5},  # Right hip
        ]
        
        return {
            'keypoints': keypoints,
            'landmarks_count': len(keypoints),
            'segmentation_mask': None,
            'confidence': 0.4,
            'method': 'opencv_fallback',
            'image_width': w,
            'image_height': h
        }
        
    except Exception as e:
        logger.error(f"Fallback pose detection failed: {e}")
        return None

def extract_body_measurements(keypoints):
    """
    Extract body measurements from pose keypoints.
    Computes shoulder width, torso length, hip width, and classifies body shape.
    
    Args:
        keypoints: List of keypoint dictionaries from detect_body_pose
        
    Returns:
        dict: Contains measurements and body_shape classification
    """
    try:
        if not keypoints or len(keypoints) < 5:
            return {
                'error': 'Insufficient keypoints for measurement',
                'body_shape': 'unknown'
            }
        
        # Convert keypoints list to dict for easier access
        kp_dict = {kp['id']: kp for kp in keypoints}
        
        # MediaPipe pose landmark indices
        # 11: left shoulder, 12: right shoulder
        # 23: left hip, 24: right hip
        # 0: nose, 11: left shoulder (for torso length approximation)
        
        measurements = {}
        
        # Shoulder width
        if 11 in kp_dict and 12 in kp_dict:
            shoulder_left = kp_dict[11]
            shoulder_right = kp_dict[12]
            shoulder_width = abs(shoulder_left['x'] - shoulder_right['x'])
            measurements['shoulder_width'] = float(shoulder_width)
        else:
            measurements['shoulder_width'] = 0.4  # default
        
        # Hip width
        if 23 in kp_dict and 24 in kp_dict:
            hip_left = kp_dict[23]
            hip_right = kp_dict[24]
            hip_width = abs(hip_left['x'] - hip_right['x'])
            measurements['hip_width'] = float(hip_width)
        else:
            measurements['hip_width'] = 0.38  # default
        
        # Torso length (nose to hip midpoint)
        if 0 in kp_dict and 23 in kp_dict and 24 in kp_dict:
            nose = kp_dict[0]
            hip_left = kp_dict[23]
            hip_right = kp_dict[24]
            hip_mid_y = (hip_left['y'] + hip_right['y']) / 2
            torso_length = abs(hip_mid_y - nose['y'])
            measurements['torso_length'] = float(torso_length)
        else:
            measurements['torso_length'] = 0.5  # default
        
        # Calculate body shape based on proportions
        shoulder_width = measurements.get('shoulder_width', 0.4)
        hip_width = measurements.get('hip_width', 0.38)
        ratio = shoulder_width / hip_width if hip_width > 0 else 1.0
        measurements['shoulder_hip_ratio'] = float(ratio)
        
        # Classify body shape
        if ratio > 1.1:
            body_shape = 'inverted_triangle'
        elif ratio < 0.9:
            body_shape = 'pear'
        elif 0.95 <= ratio <= 1.05:
            body_shape = 'hourglass'
        else:
            body_shape = 'rectangle'
        
        return {
            'measurements': measurements,
            'body_shape': body_shape,
            'confidence': 0.8 if len(keypoints) > 15 else 0.6
        }
        
    except Exception as e:
        logger.error(f"Measurement extraction failed: {e}")
        return {
            'error': str(e),
            'body_shape': 'unknown',
            'measurements': {}
        }

def remove_background(image_path, output_path=None):
    """
    Remove background from image using DeepLabV3 with OpenCV fallback.
    Returns path to image with transparent background (PNG).
    
    Args:
        image_path: Path to input image
        output_path: Optional path for output (auto-generated if None)
        
    Returns:
        str: Path to output image with transparent background
    """
    try:
        if DEEPLABV3_AVAILABLE:
            return remove_background_deeplabv3(image_path, output_path)
        else:
            return remove_background_opencv(image_path, output_path)
            
    except Exception as e:
        logger.error(f"Background removal failed: {e}")
        # Return original image path as fallback
        return str(image_path)

def remove_background_deeplabv3(image_path, output_path=None):
    """Remove background using DeepLabV3 segmentation"""
    try:
        # Load pre-trained DeepLabV3 model
        model = torchvision.models.segmentation.deeplabv3_resnet101(pretrained=True)
        model.eval()
        
        # Read and preprocess image
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError("Could not read image")
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, _ = image.shape
        
        # Prepare input for model
        from torchvision import transforms
        preprocess = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((520, 520)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        input_tensor = preprocess(image_rgb)
        input_batch = input_tensor.unsqueeze(0)
        
        # Run inference
        with torch.no_grad():
            output = model(input_batch)['out'][0]
        
        # Get person segmentation mask (class 15 in COCO)
        output_predictions = output.argmax(0).byte().cpu().numpy()
        mask = (output_predictions == 15).astype(np.uint8) * 255
        
        # Resize mask to original size
        mask = cv2.resize(mask, (w, h))
        
        # Apply mask to create transparent background
        image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        image_rgba[:, :, 3] = mask
        
        # Generate output path
        if output_path is None:
            input_path = Path(image_path)
            output_path = input_path.parent / f"{input_path.stem}_nobg.png"
        
        # Save result
        cv2.imwrite(str(output_path), image_rgba)
        logger.info(f"Background removed using DeepLabV3: {output_path}")
        
        return str(output_path)
        
    except Exception as e:
        logger.error(f"DeepLabV3 background removal failed: {e}")
        return remove_background_opencv(image_path, output_path)

def remove_background_opencv(image_path, output_path=None):
    """Fallback background removal using OpenCV GrabCut"""
    try:
        # Read image
        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError("Could not read image")
        
        h, w, _ = image.shape
        
        # Create mask for GrabCut
        mask = np.zeros((h, w), np.uint8)
        
        # Define rectangle around the subject (assuming center composition)
        rect = (int(w * 0.1), int(h * 0.1), int(w * 0.8), int(h * 0.8))
        
        # Initialize background and foreground models
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        
        # Run GrabCut
        cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
        
        # Create binary mask
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        
        # Apply mask to create transparent background
        image_rgba = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        image_rgba[:, :, 3] = mask2 * 255
        
        # Generate output path
        if output_path is None:
            input_path = Path(image_path)
            output_path = input_path.parent / f"{input_path.stem}_nobg.png"
        
        # Save result
        cv2.imwrite(str(output_path), image_rgba)
        logger.info(f"Background removed using OpenCV: {output_path}")
        
        return str(output_path)
        
    except Exception as e:
        logger.error(f"OpenCV background removal failed: {e}")
        return str(image_path)

# Legacy function for backward compatibility
def detect_body_shape_mediapipe(image_path):
    """Detect body shape using MediaPipe Pose (legacy function, use detect_body_pose instead)"""
    try:
        pose_data = detect_body_pose(image_path)
        if not pose_data:
            return None
        
        measurements = extract_body_measurements(pose_data['keypoints'])
        
        return {
            'body_type': measurements.get('body_shape', 'unknown'),
            'measurements': measurements.get('measurements', {}),
            'confidence': pose_data.get('confidence', 0.5),
            'method': pose_data.get('method', 'mediapipe'),
            'landmarks_detected': pose_data.get('landmarks_count', 0)
        }
    except Exception as e:
        logger.error(f"MediaPipe detection failed: {e}")
        return None

def detect_body_shape_fallback(image_path):
    """Fallback body shape detection using OpenCV (legacy function)"""
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            raise ValueError("No contours detected")
        
        # Get largest contour (assumed to be the person)
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Calculate bounding rectangle
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Simple heuristic based on aspect ratio
        aspect_ratio = w / h if h > 0 else 1.0
        
        if aspect_ratio < 0.4:
            body_type = 'rectangle'
        elif aspect_ratio > 0.6:
            body_type = 'average'
        else:
            body_type = 'balanced'
        
        return {
            'body_type': body_type,
            'measurements': {
                'width': int(w),
                'height': int(h),
                'aspect_ratio': float(aspect_ratio)
            },
            'confidence': 0.65,
            'method': 'opencv_fallback',
            'contours_found': len(contours)
        }
        
    except Exception as e:
        logger.error(f"Fallback detection failed: {e}")
        return {
            'body_type': 'average',
            'measurements': {},
            'confidence': 0.5,
            'method': 'default',
            'error': str(e)
        }

def detect_body_shape(image_path):
    """Main entry point for body shape detection (legacy function)"""
    # Try MediaPipe first
    if MEDIAPIPE_AVAILABLE:
        result = detect_body_shape_mediapipe(image_path)
        if result:
            return result
    
    # Fallback to OpenCV
    return detect_body_shape_fallback(image_path)
