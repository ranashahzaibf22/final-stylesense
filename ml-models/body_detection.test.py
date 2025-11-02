"""Unit tests for body detection module"""
import pytest
import cv2
import numpy as np
from pathlib import Path
import sys
import tempfile
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ml_models.body_detection import (
    detect_body_pose,
    extract_body_measurements,
    remove_background,
    detect_body_shape,
    MEDIAPIPE_AVAILABLE,
    DEEPLABV3_AVAILABLE
)

@pytest.fixture
def test_image():
    """Create a simple test image"""
    # Create a 640x480 test image
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    # Draw a simple person-like shape
    cv2.rectangle(img, (250, 100), (390, 400), (255, 255, 255), -1)  # Body
    cv2.circle(img, (320, 60), 30, (255, 255, 255), -1)  # Head
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(mode='w+b', suffix='.jpg', delete=False) as f:
        cv2.imwrite(f.name, img)
        yield f.name
    
    # Cleanup
    os.unlink(f.name)

@pytest.fixture
def real_test_image():
    """Create a more realistic test image"""
    img = np.ones((480, 640, 3), dtype=np.uint8) * 200  # Gray background
    
    # Draw a more person-like figure
    # Head
    cv2.circle(img, (320, 80), 40, (255, 200, 180), -1)
    # Shoulders
    cv2.rectangle(img, (240, 120), (400, 180), (100, 100, 200), -1)
    # Torso
    cv2.rectangle(img, (260, 180), (380, 320), (100, 100, 200), -1)
    # Hips
    cv2.rectangle(img, (270, 320), (370, 380), (50, 50, 100), -1)
    
    with tempfile.NamedTemporaryFile(mode='w+b', suffix='.jpg', delete=False) as f:
        cv2.imwrite(f.name, img)
        yield f.name
    
    os.unlink(f.name)

class TestBodyPoseDetection:
    """Tests for pose detection functions"""
    
    def test_detect_body_pose_basic(self, test_image):
        """Test basic pose detection"""
        result = detect_body_pose(test_image)
        
        assert result is not None
        assert 'keypoints' in result
        assert 'confidence' in result
        assert 'method' in result
        assert isinstance(result['keypoints'], list)
        assert result['confidence'] > 0
    
    def test_detect_body_pose_invalid_image(self):
        """Test pose detection with invalid image path"""
        result = detect_body_pose('nonexistent.jpg')
        assert result is None or 'error' in result
    
    def test_detect_body_pose_keypoints_structure(self, test_image):
        """Test that keypoints have correct structure"""
        result = detect_body_pose(test_image)
        
        if result and result['keypoints']:
            keypoint = result['keypoints'][0]
            assert 'id' in keypoint
            assert 'x' in keypoint
            assert 'y' in keypoint
            assert 'z' in keypoint
            assert 'visibility' in keypoint
    
    @pytest.mark.skipif(not MEDIAPIPE_AVAILABLE, reason="MediaPipe not available")
    def test_mediapipe_detection(self, real_test_image):
        """Test MediaPipe detection when available"""
        result = detect_body_pose(real_test_image)
        
        assert result is not None
        assert result['method'] in ['mediapipe', 'opencv_fallback']
        if result['method'] == 'mediapipe':
            assert result['landmarks_count'] > 0

class TestBodyMeasurements:
    """Tests for measurement extraction"""
    
    def test_extract_measurements_valid_keypoints(self):
        """Test measurement extraction with valid keypoints"""
        # Create sample keypoints
        keypoints = [
            {'id': 0, 'x': 0.5, 'y': 0.1, 'z': 0, 'visibility': 1.0},  # Nose
            {'id': 11, 'x': 0.4, 'y': 0.3, 'z': 0, 'visibility': 1.0},  # Left shoulder
            {'id': 12, 'x': 0.6, 'y': 0.3, 'z': 0, 'visibility': 1.0},  # Right shoulder
            {'id': 23, 'x': 0.42, 'y': 0.6, 'z': 0, 'visibility': 1.0},  # Left hip
            {'id': 24, 'x': 0.58, 'y': 0.6, 'z': 0, 'visibility': 1.0},  # Right hip
        ]
        
        result = extract_body_measurements(keypoints)
        
        assert 'measurements' in result
        assert 'body_shape' in result
        assert 'confidence' in result
        assert result['body_shape'] in ['inverted_triangle', 'pear', 'hourglass', 'rectangle', 'unknown']
    
    def test_extract_measurements_insufficient_keypoints(self):
        """Test measurement extraction with insufficient keypoints"""
        keypoints = [
            {'id': 0, 'x': 0.5, 'y': 0.1, 'z': 0, 'visibility': 1.0}
        ]
        
        result = extract_body_measurements(keypoints)
        assert result['body_shape'] == 'unknown'
    
    def test_extract_measurements_empty_keypoints(self):
        """Test measurement extraction with empty keypoints"""
        result = extract_body_measurements([])
        assert result['body_shape'] == 'unknown'
    
    def test_body_shape_classification_inverted_triangle(self):
        """Test inverted triangle body shape classification"""
        keypoints = [
            {'id': 0, 'x': 0.5, 'y': 0.1, 'z': 0, 'visibility': 1.0},
            {'id': 11, 'x': 0.3, 'y': 0.3, 'z': 0, 'visibility': 1.0},  # Wide shoulders
            {'id': 12, 'x': 0.7, 'y': 0.3, 'z': 0, 'visibility': 1.0},
            {'id': 23, 'x': 0.45, 'y': 0.6, 'z': 0, 'visibility': 1.0},  # Narrow hips
            {'id': 24, 'x': 0.55, 'y': 0.6, 'z': 0, 'visibility': 1.0},
        ]
        
        result = extract_body_measurements(keypoints)
        assert result['body_shape'] == 'inverted_triangle'
    
    def test_body_shape_classification_pear(self):
        """Test pear body shape classification"""
        keypoints = [
            {'id': 0, 'x': 0.5, 'y': 0.1, 'z': 0, 'visibility': 1.0},
            {'id': 11, 'x': 0.45, 'y': 0.3, 'z': 0, 'visibility': 1.0},  # Narrow shoulders
            {'id': 12, 'x': 0.55, 'y': 0.3, 'z': 0, 'visibility': 1.0},
            {'id': 23, 'x': 0.35, 'y': 0.6, 'z': 0, 'visibility': 1.0},  # Wide hips
            {'id': 24, 'x': 0.65, 'y': 0.6, 'z': 0, 'visibility': 1.0},
        ]
        
        result = extract_body_measurements(keypoints)
        assert result['body_shape'] == 'pear'
    
    def test_body_shape_classification_hourglass(self):
        """Test hourglass body shape classification"""
        keypoints = [
            {'id': 0, 'x': 0.5, 'y': 0.1, 'z': 0, 'visibility': 1.0},
            {'id': 11, 'x': 0.4, 'y': 0.3, 'z': 0, 'visibility': 1.0},  # Balanced
            {'id': 12, 'x': 0.6, 'y': 0.3, 'z': 0, 'visibility': 1.0},
            {'id': 23, 'x': 0.4, 'y': 0.6, 'z': 0, 'visibility': 1.0},
            {'id': 24, 'x': 0.6, 'y': 0.6, 'z': 0, 'visibility': 1.0},
        ]
        
        result = extract_body_measurements(keypoints)
        assert result['body_shape'] == 'hourglass'
    
    def test_measurements_values(self):
        """Test that measurement values are reasonable"""
        keypoints = [
            {'id': 0, 'x': 0.5, 'y': 0.1, 'z': 0, 'visibility': 1.0},
            {'id': 11, 'x': 0.4, 'y': 0.3, 'z': 0, 'visibility': 1.0},
            {'id': 12, 'x': 0.6, 'y': 0.3, 'z': 0, 'visibility': 1.0},
            {'id': 23, 'x': 0.42, 'y': 0.6, 'z': 0, 'visibility': 1.0},
            {'id': 24, 'x': 0.58, 'y': 0.6, 'z': 0, 'visibility': 1.0},
        ]
        
        result = extract_body_measurements(keypoints)
        measurements = result['measurements']
        
        assert 'shoulder_width' in measurements
        assert 'hip_width' in measurements
        assert 'torso_length' in measurements
        assert measurements['shoulder_width'] > 0
        assert measurements['hip_width'] > 0
        assert measurements['torso_length'] > 0

class TestBackgroundRemoval:
    """Tests for background removal"""
    
    def test_remove_background_basic(self, test_image):
        """Test basic background removal"""
        output_path = remove_background(test_image)
        
        assert output_path is not None
        assert isinstance(output_path, str)
        # Should either create new file or return original
        assert Path(output_path).exists() or output_path == test_image
        
        # Cleanup if new file created
        if output_path != test_image and Path(output_path).exists():
            os.unlink(output_path)
    
    def test_remove_background_custom_output(self, test_image):
        """Test background removal with custom output path"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            output_path = f.name
        
        result_path = remove_background(test_image, output_path)
        
        # Should use custom output path
        assert result_path is not None
        
        # Cleanup
        if Path(result_path).exists() and result_path != test_image:
            os.unlink(result_path)
    
    def test_remove_background_invalid_image(self):
        """Test background removal with invalid image"""
        result = remove_background('nonexistent.jpg')
        # Should handle gracefully
        assert result is not None

class TestLegacyFunctions:
    """Tests for legacy compatibility functions"""
    
    def test_detect_body_shape_legacy(self, test_image):
        """Test legacy detect_body_shape function"""
        result = detect_body_shape(test_image)
        
        assert result is not None
        assert 'body_type' in result
        assert 'confidence' in result
        assert 'method' in result
    
    def test_body_shape_types(self, test_image):
        """Test that body shape types are valid"""
        result = detect_body_shape(test_image)
        
        valid_types = ['inverted_triangle', 'pear', 'hourglass', 'rectangle', 
                       'average', 'balanced', 'unknown']
        assert result['body_type'] in valid_types

class TestErrorHandling:
    """Tests for error handling"""
    
    def test_none_image_path(self):
        """Test handling of None image path"""
        result = detect_body_pose(None)
        assert result is None or 'error' in result
    
    def test_empty_string_path(self):
        """Test handling of empty string path"""
        result = detect_body_pose('')
        assert result is None or 'error' in result
    
    def test_measurement_with_none(self):
        """Test measurement extraction with None"""
        result = extract_body_measurements(None)
        assert result['body_shape'] == 'unknown'

class TestIntegration:
    """Integration tests combining multiple functions"""
    
    def test_full_pipeline(self, real_test_image):
        """Test complete pipeline from pose detection to measurements"""
        # Detect pose
        pose_data = detect_body_pose(real_test_image)
        assert pose_data is not None
        
        # Extract measurements
        if pose_data and pose_data.get('keypoints'):
            measurements = extract_body_measurements(pose_data['keypoints'])
            assert measurements is not None
            assert 'body_shape' in measurements
        
        # Remove background
        output_path = remove_background(real_test_image)
        assert output_path is not None
        
        # Cleanup
        if output_path != real_test_image and Path(output_path).exists():
            os.unlink(output_path)
    
    def test_multiple_body_types(self):
        """Test detection works for various body proportions"""
        test_cases = [
            # (shoulder_width, hip_width, expected_shape)
            (0.4, 0.3, 'inverted_triangle'),
            (0.3, 0.4, 'pear'),
            (0.4, 0.4, 'hourglass'),
        ]
        
        for shoulder_w, hip_w, expected_shape in test_cases:
            keypoints = [
                {'id': 0, 'x': 0.5, 'y': 0.1, 'z': 0, 'visibility': 1.0},
                {'id': 11, 'x': 0.5 - shoulder_w/2, 'y': 0.3, 'z': 0, 'visibility': 1.0},
                {'id': 12, 'x': 0.5 + shoulder_w/2, 'y': 0.3, 'z': 0, 'visibility': 1.0},
                {'id': 23, 'x': 0.5 - hip_w/2, 'y': 0.6, 'z': 0, 'visibility': 1.0},
                {'id': 24, 'x': 0.5 + hip_w/2, 'y': 0.6, 'z': 0, 'visibility': 1.0},
            ]
            
            result = extract_body_measurements(keypoints)
            assert result['body_shape'] == expected_shape

class TestPerformance:
    """Performance tests"""
    
    def test_detection_speed(self, test_image):
        """Test that detection completes in reasonable time"""
        import time
        start = time.time()
        result = detect_body_pose(test_image)
        elapsed = time.time() - start
        
        # Should complete within 5 seconds (generous for CI)
        assert elapsed < 5.0
        assert result is not None
