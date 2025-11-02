import React, { useState, useEffect, useRef } from 'react';
import { requestCameraAccess, stopCameraStream, captureImageFromVideo, dataURLtoFile, isCameraAvailable } from '../utils/camera';

function CameraCapture({ onCapture }) {
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [error, setError] = useState(null);
  const [capturedImage, setCapturedImage] = useState(null);
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        stopCameraStream(streamRef.current);
      }
    };
  }, []);

  const startCamera = async () => {
    try {
      if (!isCameraAvailable()) {
        throw new Error('Camera not available on this device');
      }

      const stream = await requestCameraAccess(videoRef.current);
      streamRef.current = stream;
      setIsCameraActive(true);
      setError(null);
    } catch (err) {
      setError(err.message);
      setIsCameraActive(false);
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      stopCameraStream(streamRef.current);
      streamRef.current = null;
      setIsCameraActive(false);
    }
  };

  const capture = () => {
    if (videoRef.current && isCameraActive) {
      const imageDataURL = captureImageFromVideo(videoRef.current);
      setCapturedImage(imageDataURL);
      
      if (onCapture) {
        const file = dataURLtoFile(imageDataURL, 'capture.png');
        onCapture(file);
      }
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setCapturedImage(event.target.result);
        if (onCapture) {
          onCapture(file);
        }
      };
      reader.readAsDataURL(file);
    }
  };

  const reset = () => {
    setCapturedImage(null);
  };

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-semibold mb-4">Camera Capture</h2>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded p-4 mb-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      <div className="space-y-4">
        {/* Camera View or Captured Image */}
        <div className="relative bg-gray-900 rounded-lg overflow-hidden aspect-video">
          {capturedImage ? (
            <img
              src={capturedImage}
              alt="Captured"
              className="w-full h-full object-contain"
            />
          ) : isCameraActive ? (
            <video
              ref={videoRef}
              className="w-full h-full object-cover"
              autoPlay
              playsInline
            />
          ) : (
            <div className="flex items-center justify-center h-full">
              <p className="text-white text-lg">Camera not active</p>
            </div>
          )}
        </div>

        {/* Controls */}
        <div className="flex flex-wrap gap-3">
          {!capturedImage && !isCameraActive && (
            <button
              onClick={startCamera}
              className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              📸 Start Camera
            </button>
          )}

          {isCameraActive && !capturedImage && (
            <>
              <button
                onClick={capture}
                className="flex-1 bg-green-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-green-700 transition-colors"
              >
                📷 Capture
              </button>
              <button
                onClick={stopCamera}
                className="flex-1 bg-red-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-red-700 transition-colors"
              >
                ⏹️ Stop
              </button>
            </>
          )}

          {capturedImage && (
            <button
              onClick={reset}
              className="flex-1 bg-gray-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-gray-700 transition-colors"
            >
              🔄 Retake
            </button>
          )}

          {/* File Upload Option */}
          <div className="flex-1">
            <label className="block w-full bg-purple-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-purple-700 transition-colors text-center cursor-pointer">
              📁 Upload from Gallery
              <input
                type="file"
                accept="image/*"
                onChange={handleFileUpload}
                className="hidden"
              />
            </label>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CameraCapture;
