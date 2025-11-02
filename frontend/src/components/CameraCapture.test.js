import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import CameraCapture from './CameraCapture';
import * as cameraUtils from '../utils/camera';
import api from '../utils/api';

// Mock the camera utilities
jest.mock('../utils/camera');
jest.mock('../utils/api');

describe('CameraCapture Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Default mock implementations
    cameraUtils.isCameraAvailable.mockReturnValue(true);
    cameraUtils.requestCameraAccess.mockResolvedValue({
      getTracks: () => [],
      getVideoTracks: () => [{
        getCapabilities: () => ({}),
        applyConstraints: jest.fn()
      }]
    });
    cameraUtils.stopCameraStream.mockImplementation(() => {});
    cameraUtils.captureImageFromVideo.mockReturnValue('data:image/png;base64,test');
    cameraUtils.dataURLtoFile.mockReturnValue(new File([''], 'test.png'));
  });

  test('renders camera capture component', () => {
    render(<CameraCapture />);
    expect(screen.getByText('Camera Capture')).toBeInTheDocument();
  });

  test('shows start camera button when camera is not active', () => {
    render(<CameraCapture />);
    expect(screen.getByText('📸 Start Camera')).toBeInTheDocument();
  });

  test('displays error message when camera is not available', async () => {
    cameraUtils.isCameraAvailable.mockReturnValue(false);
    render(<CameraCapture />);
    
    const startButton = screen.getByText('📸 Start Camera');
    fireEvent.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Camera not available/i)).toBeInTheDocument();
    });
  });

  test('starts camera successfully', async () => {
    render(<CameraCapture />);
    
    const startButton = screen.getByText('📸 Start Camera');
    fireEvent.click(startButton);
    
    await waitFor(() => {
      expect(cameraUtils.requestCameraAccess).toHaveBeenCalled();
      expect(screen.getByText('📷 Capture')).toBeInTheDocument();
    });
  });

  test('captures image from video', async () => {
    const onCapture = jest.fn();
    render(<CameraCapture onCapture={onCapture} />);
    
    // Start camera
    const startButton = screen.getByText('📸 Start Camera');
    fireEvent.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('📷 Capture')).toBeInTheDocument();
    }, { timeout: 3000 });
    
    // Mock API response
    api.post.mockResolvedValue({
      data: {
        success: true,
        analysis: {
          body_type: 'rectangle',
          confidence: 0.85,
          method: 'mediapipe'
        }
      }
    });
    
    // Capture image
    const captureButton = screen.getByText('📷 Capture');
    fireEvent.click(captureButton);
    
    await waitFor(() => {
      expect(cameraUtils.captureImageFromVideo).toHaveBeenCalled();
      expect(onCapture).toHaveBeenCalled();
    }, { timeout: 3000 });
  });

  test('stops camera', async () => {
    render(<CameraCapture />);
    
    // Start camera
    const startButton = screen.getByText('📸 Start Camera');
    fireEvent.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('⏹️ Stop')).toBeInTheDocument();
    });
    
    // Stop camera
    const stopButton = screen.getByText('⏹️ Stop');
    fireEvent.click(stopButton);
    
    await waitFor(() => {
      expect(cameraUtils.stopCameraStream).toHaveBeenCalled();
      expect(screen.getByText('📸 Start Camera')).toBeInTheDocument();
    });
  });

  test('toggles between front and back camera', async () => {
    render(<CameraCapture />);
    
    // Start camera
    const startButton = screen.getByText('📸 Start Camera');
    fireEvent.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('🔄 Switch Camera')).toBeInTheDocument();
    });
    
    // Toggle camera
    const toggleButton = screen.getByText('🔄 Switch Camera');
    fireEvent.click(toggleButton);
    
    await waitFor(() => {
      expect(cameraUtils.requestCameraAccess).toHaveBeenCalledTimes(2);
    });
  });

  test('validates file upload - valid file', async () => {
    const onCapture = jest.fn();
    render(<CameraCapture onCapture={onCapture} />);
    
    const file = new File(['image content'], 'test.jpg', { type: 'image/jpeg' });
    Object.defineProperty(file, 'size', { value: 1024 * 1024 }); // 1MB
    
    const input = screen.getByLabelText(/Upload from Gallery/i).querySelector('input');
    
    api.post.mockResolvedValue({
      data: {
        success: true,
        analysis: { body_type: 'rectangle', confidence: 0.85, method: 'mediapipe' }
      }
    });
    
    // Mock FileReader
    const originalFileReader = global.FileReader;
    global.FileReader = jest.fn(function() {
      this.readAsDataURL = jest.fn(function() {
        setTimeout(() => {
          this.onload({ target: { result: 'data:image/jpeg;base64,test' } });
        }, 0);
      });
    });
    
    fireEvent.change(input, { target: { files: [file] } });
    
    await waitFor(() => {
      expect(onCapture).toHaveBeenCalled();
    }, { timeout: 3000 });
    
    global.FileReader = originalFileReader;
  });

  test('validates file upload - invalid file type', async () => {
    render(<CameraCapture />);
    
    const file = new File(['text content'], 'test.txt', { type: 'text/plain' });
    const input = screen.getByLabelText(/Upload from Gallery/i).querySelector('input');
    
    fireEvent.change(input, { target: { files: [file] } });
    
    await waitFor(() => {
      expect(screen.getByText(/Invalid file type/i)).toBeInTheDocument();
    });
  });

  test('validates file upload - file too large', async () => {
    render(<CameraCapture />);
    
    const file = new File(['image content'], 'large.jpg', { type: 'image/jpeg' });
    Object.defineProperty(file, 'size', { value: 17 * 1024 * 1024 }); // 17MB
    
    const input = screen.getByLabelText(/Upload from Gallery/i).querySelector('input');
    
    fireEvent.change(input, { target: { files: [file] } });
    
    await waitFor(() => {
      expect(screen.getByText(/exceeds 16MB limit/i)).toBeInTheDocument();
    });
  });

  test('displays pose guidance after capture', async () => {
    render(<CameraCapture />);
    
    // Start camera
    const startButton = screen.getByText('📸 Start Camera');
    fireEvent.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('📷 Capture')).toBeInTheDocument();
    });
    
    // Mock API response with pose data
    api.post.mockResolvedValue({
      data: {
        success: true,
        analysis: {
          body_type: 'hourglass',
          confidence: 0.92,
          method: 'mediapipe',
          measurements: {
            shoulder_width: 0.4,
            hip_width: 0.38
          }
        }
      }
    });
    
    // Capture
    const captureButton = screen.getByText('📷 Capture');
    fireEvent.click(captureButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Body Type:/i)).toBeInTheDocument();
      expect(screen.getByText(/hourglass/i)).toBeInTheDocument();
      expect(screen.getByText(/92%/i)).toBeInTheDocument();
    });
  });

  test('allows retaking photo', async () => {
    render(<CameraCapture />);
    
    // Start and capture
    const startButton = screen.getByText('📸 Start Camera');
    fireEvent.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('📷 Capture')).toBeInTheDocument();
    });
    
    api.post.mockResolvedValue({
      data: { success: true, analysis: { body_type: 'rectangle', confidence: 0.85, method: 'mediapipe' } }
    });
    
    const captureButton = screen.getByText('📷 Capture');
    fireEvent.click(captureButton);
    
    await waitFor(() => {
      expect(screen.getByText('🔄 Retake')).toBeInTheDocument();
    });
    
    // Retake
    const retakeButton = screen.getByText('🔄 Retake');
    fireEvent.click(retakeButton);
    
    await waitFor(() => {
      expect(screen.queryByText(/Body Type:/i)).not.toBeInTheDocument();
    });
  });

  test('shows processing indicator during capture', async () => {
    render(<CameraCapture />);
    
    // Start camera
    const startButton = screen.getByText('📸 Start Camera');
    fireEvent.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('📷 Capture')).toBeInTheDocument();
    });
    
    // Mock slow API response
    api.post.mockImplementation(() => new Promise(resolve => setTimeout(() => resolve({
      data: { success: true, analysis: { body_type: 'rectangle', confidence: 0.85, method: 'mediapipe' } }
    }), 100)));
    
    const captureButton = screen.getByText('📷 Capture');
    fireEvent.click(captureButton);
    
    // Should show processing
    expect(screen.getByText('Processing...')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.queryByText('Processing...')).not.toBeInTheDocument();
    });
  });

  test('handles API errors gracefully', async () => {
    render(<CameraCapture />);
    
    // Start camera
    const startButton = screen.getByText('📸 Start Camera');
    fireEvent.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('📷 Capture')).toBeInTheDocument();
    });
    
    // Mock API error
    api.post.mockRejectedValue(new Error('Network error'));
    
    const captureButton = screen.getByText('📷 Capture');
    fireEvent.click(captureButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Pose analysis unavailable/i)).toBeInTheDocument();
    });
  });

  test('displays tips and technical info', () => {
    render(<CameraCapture />);
    
    expect(screen.getByText(/Use good lighting/i)).toBeInTheDocument();
    expect(screen.getByText(/Max 16MB/i)).toBeInTheDocument();
    expect(screen.getByText(/Privacy:/i)).toBeInTheDocument();
  });

  test('is responsive on mobile', () => {
    const { container } = render(<CameraCapture />);
    
    // Check for responsive grid classes
    const controlsContainer = container.querySelector('.grid');
    expect(controlsContainer).toHaveClass('grid-cols-1', 'sm:grid-cols-2', 'lg:grid-cols-4');
  });
});

// Cross-browser compatibility tests
describe('CameraCapture - Cross-browser compatibility', () => {
  test('handles missing MediaDevices API', () => {
    cameraUtils.isCameraAvailable.mockReturnValue(false);
    
    render(<CameraCapture />);
    const startButton = screen.getByText('📸 Start Camera');
    fireEvent.click(startButton);
    
    expect(screen.getByText(/Camera not available/i)).toBeInTheDocument();
  });

  test('handles camera permission denied', async () => {
    cameraUtils.requestCameraAccess.mockRejectedValue(new Error('Permission denied'));
    
    render(<CameraCapture />);
    const startButton = screen.getByText('📸 Start Camera');
    fireEvent.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText(/Permission denied/i)).toBeInTheDocument();
    });
  });
});

// Mobile-specific tests
describe('CameraCapture - Mobile devices', () => {
  test('supports front and back camera toggle', async () => {
    render(<CameraCapture />);
    
    const startButton = screen.getByText('📸 Start Camera');
    fireEvent.click(startButton);
    
    await waitFor(() => {
      expect(screen.getByText('🔄 Switch Camera')).toBeInTheDocument();
    });
    
    const toggleButton = screen.getByText('🔄 Switch Camera');
    fireEvent.click(toggleButton);
    
    await waitFor(() => {
      expect(cameraUtils.requestCameraAccess).toHaveBeenCalledTimes(2);
      const secondCall = cameraUtils.requestCameraAccess.mock.calls[1];
      expect(secondCall[1].video.facingMode).toBe('environment');
    });
  });

  test('requests high resolution on capable devices', async () => {
    render(<CameraCapture />);
    
    const startButton = screen.getByText('📸 Start Camera');
    fireEvent.click(startButton);
    
    await waitFor(() => {
      expect(cameraUtils.requestCameraAccess).toHaveBeenCalled();
      const callArgs = cameraUtils.requestCameraAccess.mock.calls[0];
      expect(callArgs[1]).toHaveProperty('video');
      expect(callArgs[1].video).toMatchObject({
        facingMode: 'user',
        width: { ideal: 1920 },
        height: { ideal: 1080 }
      });
    });
  });
});
