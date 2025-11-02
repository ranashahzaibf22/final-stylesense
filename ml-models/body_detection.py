"""Body shape detection using MediaPipe/Microsoft Human Pose with fallback"""
import logging
import cv2
import numpy as np

logger = logging.getLogger(__name__)

try:
    import mediapipe as mp
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False
    logger.warning("MediaPipe not available, using fallback detection")

def detect_body_shape_mediapipe(image_path):
    """Detect body shape using MediaPipe Pose"""
    try:
        mp_pose = mp.solutions.pose
        
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")
        
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Initialize pose detection
        with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            min_detection_confidence=0.5
        ) as pose:
            results = pose.process(image_rgb)
            
            if not results.pose_landmarks:
                return None
            
            # Extract key points
            landmarks = results.pose_landmarks.landmark
            
            # Calculate body proportions
            shoulder_left = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            shoulder_right = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            hip_left = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            hip_right = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
            
            shoulder_width = abs(shoulder_left.x - shoulder_right.x)
            hip_width = abs(hip_left.x - hip_right.x)
            
            # Determine body type based on proportions
            ratio = shoulder_width / hip_width if hip_width > 0 else 1.0
            
            if ratio > 1.1:
                body_type = 'inverted_triangle'
            elif ratio < 0.9:
                body_type = 'pear'
            elif 0.95 <= ratio <= 1.05:
                body_type = 'hourglass'
            else:
                body_type = 'rectangle'
            
            return {
                'body_type': body_type,
                'measurements': {
                    'shoulder_width': float(shoulder_width),
                    'hip_width': float(hip_width),
                    'ratio': float(ratio)
                },
                'confidence': 0.85,
                'method': 'mediapipe',
                'landmarks_detected': len(landmarks)
            }
            
    except Exception as e:
        logger.error(f"MediaPipe detection failed: {e}")
        return None

def detect_body_shape_fallback(image_path):
    """Fallback body shape detection using OpenCV"""
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
    """Main entry point for body shape detection"""
    # Try MediaPipe first
    if MEDIAPIPE_AVAILABLE:
        result = detect_body_shape_mediapipe(image_path)
        if result:
            return result
    
    # Fallback to OpenCV
    return detect_body_shape_fallback(image_path)
