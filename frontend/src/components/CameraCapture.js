import React, { useState, useEffect, useRef } from 'react';
import { requestCameraAccess, stopCameraStream, captureImageFromVideo, dataURLtoFile, isCameraAvailable } from '../utils/camera';
import api from '../utils/api';

function CameraCapture({ onCapture }) {
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [error, setError] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const [facingMode, setFacingMode] = useState('user'); // 'user' for front, 'environment' for back
  const [flashSupported, setFlashSupported] = useState(false);
  const [flashEnabled, setFlashEnabled] = useState(false);
  const [poseKeypoints, setPoseKeypoints] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [feedback, setFeedback] = useState('');
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const canvasRef = useRef(null);

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        stopCameraStream(streamRef.current);
      }
    };
  }, []);

  // Check if flash is supported
  useEffect(() => {
    if (streamRef.current) {
      const videoTrack = streamRef.current.getVideoTracks()[0];
      const capabilities = videoTrack?.getCapabilities?.();
      setFlashSupported(capabilities?.torch === true);
    }
  }, [isCameraActive]);

  const startCamera = async (newFacingMode = facingMode) => {
    try {
      if (!isCameraAvailable()) {
        throw new Error('Camera not available on this device');
      }

      // Stop existing stream if any
      if (streamRef.current) {
        stopCameraStream(streamRef.current);
      }

      const constraints = {
        video: {
          facingMode: newFacingMode,
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        }
      };

      const stream = await requestCameraAccess(videoRef.current, constraints);
      streamRef.current = stream;
      setIsCameraActive(true);
      setError(null);
      setFeedback('Camera ready. Position yourself in frame for best results.');
    } catch (err) {
      setError(err.message);
      setIsCameraActive(false);
      setFeedback('');
    }
  };

  const toggleCamera = async () => {
    const newFacingMode = facingMode === 'user' ? 'environment' : 'user';
    setFacingMode(newFacingMode);
    if (isCameraActive) {
      await startCamera(newFacingMode);
    }
  };

  const toggleFlash = async () => {
    if (!streamRef.current) return;
    
    try {
      const videoTrack = streamRef.current.getVideoTracks()[0];
      const capabilities = videoTrack.getCapabilities();
      
      if (capabilities.torch) {
        await videoTrack.applyConstraints({
          advanced: [{ torch: !flashEnabled }]
        });
        setFlashEnabled(!flashEnabled);
      }
    } catch (err) {
      console.error('Flash toggle error:', err);
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      stopCameraStream(streamRef.current);
      streamRef.current = null;
      setIsCameraActive(false);
      setFlashEnabled(false);
      setPoseKeypoints(null);
      setFeedback('');
    }
  };

  const capture = async () => {
    if (videoRef.current && isCameraActive) {
      const imageDataURL = captureImageFromVideo(videoRef.current);
      setCapturedImage(imageDataURL);
      setIsProcessing(true);
      setFeedback('Processing image...');
      
      if (onCapture) {
        const file = dataURLtoFile(imageDataURL, 'capture.png');
        onCapture(file);
        
        // Get pose keypoints for feedback
        try {
          const formData = new FormData();
          formData.append('file', file);
          const response = await api.post('/body-shape/analyze', formData);
          if (response.data.success) {
            setPoseKeypoints(response.data.analysis);
            setFeedback('Image captured successfully!');
          }
        } catch (err) {
          console.error('Pose analysis error:', err);
          setFeedback('Image captured. Pose analysis unavailable.');
        }
      }
      
      setIsProcessing(false);
    }
  };

  const validateFile = (file) => {
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];
    
    if (!allowedTypes.includes(file.type)) {
      throw new Error('Invalid file type. Please upload JPG, PNG, or WebP images.');
    }
    
    if (file.size > maxSize) {
      throw new Error('File size exceeds 16MB limit.');
    }
    
    return true;
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    try {
      validateFile(file);
      setError(null);
      setIsProcessing(true);
      setFeedback('Loading image...');
      
      const reader = new FileReader();
      reader.onload = async (event) => {
        setCapturedImage(event.target.result);
        if (onCapture) {
          onCapture(file);
          
          // Get pose keypoints
          try {
            const formData = new FormData();
            formData.append('file', file);
            const response = await api.post('/body-shape/analyze', formData);
            if (response.data.success) {
              setPoseKeypoints(response.data.analysis);
              setFeedback('Image loaded successfully!');
            }
          } catch (err) {
            console.error('Pose analysis error:', err);
            setFeedback('Image loaded. Pose analysis unavailable.');
          }
        }
        setIsProcessing(false);
      };
      reader.onerror = () => {
        setError('Failed to read file');
        setIsProcessing(false);
      };
      reader.readAsDataURL(file);
    } catch (err) {
      setError(err.message);
      setIsProcessing(false);
    }
  };

  const reset = () => {
    setCapturedImage(null);
    setPoseKeypoints(null);
    setFeedback('');
  };

  // Draw pose overlay on canvas
  useEffect(() => {
    if (poseKeypoints && canvasRef.current && videoRef.current) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');
      canvas.width = videoRef.current.videoWidth || 640;
      canvas.height = videoRef.current.videoHeight || 480;
      
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Draw pose guidance (simple visualization)
      if (poseKeypoints.measurements) {
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 2;
        ctx.font = '16px Arial';
        ctx.fillStyle = '#00ff00';
        ctx.fillText(`Body Type: ${poseKeypoints.body_type}`, 10, 30);
        ctx.fillText(`Confidence: ${(poseKeypoints.confidence * 100).toFixed(0)}%`, 10, 50);
      }
    }
  }, [poseKeypoints]);

  return (
    <div className="bg-white rounded-lg shadow-lg p-4 md:p-6 max-w-4xl mx-auto">
      <h2 className="text-2xl font-semibold mb-4">Camera Capture</h2>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded p-3 mb-4">
          <p className="text-red-800 text-sm">{error}</p>
        </div>
      )}

      {feedback && !error && (
        <div className="bg-blue-50 border border-blue-200 rounded p-3 mb-4">
          <p className="text-blue-800 text-sm">{feedback}</p>
        </div>
      )}

      <div className="space-y-4">
        {/* Camera View or Captured Image with Overlay */}
        <div className="relative bg-gray-900 rounded-lg overflow-hidden aspect-video">
          {capturedImage ? (
            <img
              src={capturedImage}
              alt="Captured"
              className="w-full h-full object-contain"
            />
          ) : isCameraActive ? (
            <>
              <video
                ref={videoRef}
                className="w-full h-full object-cover"
                autoPlay
                playsInline
                muted
              />
              <canvas
                ref={canvasRef}
                className="absolute top-0 left-0 w-full h-full pointer-events-none"
              />
            </>
          ) : (
            <div className="flex flex-col items-center justify-center h-full p-4">
              <p className="text-white text-lg mb-2">📷 Camera not active</p>
              <p className="text-gray-400 text-sm text-center">
                Start camera or upload an image to begin
              </p>
            </div>
          )}
          
          {isProcessing && (
            <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
              <div className="text-white text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-2"></div>
                <p>Processing...</p>
              </div>
            </div>
          )}
        </div>

        {/* Pose Guidance Info */}
        {poseKeypoints && (
          <div className="bg-green-50 border border-green-200 rounded p-3">
            <h3 className="font-semibold text-green-800 mb-2">📊 Analysis Results</h3>
            <div className="text-sm text-green-700 space-y-1">
              <p><strong>Body Type:</strong> {poseKeypoints.body_type}</p>
              <p><strong>Confidence:</strong> {(poseKeypoints.confidence * 100).toFixed(0)}%</p>
              <p><strong>Method:</strong> {poseKeypoints.method}</p>
            </div>
          </div>
        )}

        {/* Controls */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2">
          {!capturedImage && !isCameraActive && (
            <button
              onClick={() => startCamera()}
              className="bg-blue-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors text-sm"
            >
              📸 Start Camera
            </button>
          )}

          {isCameraActive && !capturedImage && (
            <>
              <button
                onClick={capture}
                disabled={isProcessing}
                className="bg-green-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-green-700 transition-colors disabled:opacity-50 text-sm"
              >
                📷 Capture
              </button>
              <button
                onClick={toggleCamera}
                disabled={isProcessing}
                className="bg-indigo-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-indigo-700 transition-colors disabled:opacity-50 text-sm"
              >
                🔄 Switch Camera
              </button>
              {flashSupported && (
                <button
                  onClick={toggleFlash}
                  disabled={isProcessing}
                  className={`${flashEnabled ? 'bg-yellow-600 hover:bg-yellow-700' : 'bg-gray-600 hover:bg-gray-700'} text-white py-2 px-4 rounded-lg font-semibold transition-colors disabled:opacity-50 text-sm`}
                >
                  {flashEnabled ? '💡 Flash On' : '🔦 Flash Off'}
                </button>
              )}
              <button
                onClick={stopCamera}
                disabled={isProcessing}
                className="bg-red-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-red-700 transition-colors disabled:opacity-50 text-sm"
              >
                ⏹️ Stop
              </button>
            </>
          )}

          {capturedImage && (
            <button
              onClick={reset}
              disabled={isProcessing}
              className="bg-gray-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-gray-700 transition-colors disabled:opacity-50 text-sm"
            >
              🔄 Retake
            </button>
          )}

          {/* File Upload Option */}
          <label className="block bg-purple-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-purple-700 transition-colors text-center cursor-pointer text-sm">
            📁 Upload from Gallery
            <input
              type="file"
              accept="image/jpeg,image/jpg,image/png,image/webp"
              onChange={handleFileUpload}
              disabled={isProcessing}
              className="hidden"
            />
          </label>
        </div>

        {/* Technical Info */}
        <div className="text-xs text-gray-500 space-y-1">
          <p>💡 <strong>Tips:</strong> Use good lighting for best results. Camera supports 1080p+ resolution.</p>
          <p>📏 <strong>File Limits:</strong> Max 16MB, supported formats: JPG, PNG, WebP</p>
          <p>🔒 <strong>Privacy:</strong> Images are processed securely and not stored permanently.</p>
        </div>
      </div>
    </div>
  );
}

export default CameraCapture;

