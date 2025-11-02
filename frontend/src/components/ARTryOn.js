import React, { useState } from 'react';
import { applyARTryOn } from '../utils/api';
import CameraCapture from './CameraCapture';

function ARTryOn() {
  const [personImage, setPersonImage] = useState(null);
  const [garmentImage, setGarmentImage] = useState(null);
  const [resultImage, setResultImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showCamera, setShowCamera] = useState(false);
  
  // Real-time adjustment controls
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [scale, setScale] = useState(1.0);
  const [rotation, setRotation] = useState(0);
  const [showControls, setShowControls] = useState(false);

  const handlePersonImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setPersonImage(file);
      const reader = new FileReader();
      reader.onload = (event) => {
        // For preview purposes
      };
      reader.readAsDataURL(file);
    }
  };

  const handleGarmentImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setGarmentImage(file);
    }
  };

  const handleCameraCapture = (file) => {
    setPersonImage(file);
    setShowCamera(false);
  };

  const applyTryOn = async () => {
    if (!personImage || !garmentImage) {
      alert('Please provide both person and garment images');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const data = await applyARTryOn(personImage, garmentImage);
      setResultImage(data.result_url);
      setShowControls(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const adjustOverlay = async (adjustmentType, value) => {
    // Update local state
    if (adjustmentType === 'position-x') {
      setPosition({ ...position, x: value });
    } else if (adjustmentType === 'position-y') {
      setPosition({ ...position, y: value });
    } else if (adjustmentType === 'scale') {
      setScale(value);
    } else if (adjustmentType === 'rotation') {
      setRotation(value);
    }
    
    // In a real implementation, this would call an API to re-render
    // For now, we just update the CSS transform
  };

  const reset = () => {
    setPersonImage(null);
    setGarmentImage(null);
    setResultImage(null);
    setError(null);
    setPosition({ x: 0, y: 0 });
    setScale(1.0);
    setRotation(0);
    setShowControls(false);
  };

  // Calculate transform style for real-time preview
  const getTransformStyle = () => {
    return {
      transform: `translate(${position.x}px, ${position.y}px) scale(${scale}) rotate(${rotation}deg)`,
      transition: 'transform 0.2s ease'
    };
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-gray-800 mb-8">
          AR Virtual Try-On
        </h1>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
            <p className="text-red-800">Error: {error}</p>
          </div>
        )}

        {/* Camera Option */}
        {showCamera && (
          <div className="mb-6">
            <CameraCapture onCapture={handleCameraCapture} />
            <button
              onClick={() => setShowCamera(false)}
              className="mt-4 text-gray-600 hover:text-gray-800"
            >
              Cancel Camera
            </button>
          </div>
        )}

        {!showCamera && !resultImage && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            {/* Person Image Upload */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Your Photo</h2>
              
              <div className="space-y-4">
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                  {personImage ? (
                    <div>
                      <p className="text-green-600 font-medium mb-2">✓ Image selected</p>
                      <p className="text-sm text-gray-500">{personImage.name}</p>
                    </div>
                  ) : (
                    <p className="text-gray-500">No image selected</p>
                  )}
                </div>

                <div className="space-y-2">
                  <label className="block w-full bg-blue-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors text-center cursor-pointer">
                    📁 Upload Photo
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handlePersonImageUpload}
                      className="hidden"
                    />
                  </label>

                  <button
                    onClick={() => setShowCamera(true)}
                    className="w-full bg-purple-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-purple-700 transition-colors"
                  >
                    📸 Use Camera
                  </button>
                </div>
              </div>
            </div>

            {/* Garment Image Upload */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-xl font-semibold mb-4">Garment</h2>
              
              <div className="space-y-4">
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                  {garmentImage ? (
                    <div>
                      <p className="text-green-600 font-medium mb-2">✓ Image selected</p>
                      <p className="text-sm text-gray-500">{garmentImage.name}</p>
                    </div>
                  ) : (
                    <p className="text-gray-500">No image selected</p>
                  )}
                </div>

                <label className="block w-full bg-pink-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-pink-700 transition-colors text-center cursor-pointer">
                  👕 Upload Garment
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleGarmentImageUpload}
                    className="hidden"
                  />
                </label>
              </div>
            </div>
          </div>
        )}

        {/* Try On Button */}
        {!showCamera && !resultImage && (
          <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
            <button
              onClick={applyTryOn}
              disabled={!personImage || !garmentImage || loading}
              className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white py-4 px-6 rounded-lg font-bold text-lg hover:from-purple-700 hover:to-pink-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all"
            >
              {loading ? '⏳ Processing...' : '✨ Try On Garment'}
            </button>
          </div>
        )}

        {/* Result Display with Real-time Controls */}
        {resultImage && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-4">Result</h2>
            
            <div className="bg-gray-100 rounded-lg p-4 mb-4 relative overflow-hidden">
              <img
                src={resultImage}
                alt="Try-on result"
                className="max-w-full h-auto mx-auto rounded"
                style={getTransformStyle()}
              />
            </div>

            {/* Real-time Adjustment Controls */}
            {showControls && (
              <div className="bg-blue-50 rounded-lg p-4 mb-4">
                <h3 className="font-semibold text-blue-900 mb-3">Adjust Fit</h3>
                
                <div className="space-y-3">
                  {/* Position X */}
                  <div>
                    <label className="text-sm text-gray-700 font-medium">Position X: {position.x}px</label>
                    <input
                      type="range"
                      min="-50"
                      max="50"
                      value={position.x}
                      onChange={(e) => adjustOverlay('position-x', parseInt(e.target.value))}
                      className="w-full"
                    />
                  </div>
                  
                  {/* Position Y */}
                  <div>
                    <label className="text-sm text-gray-700 font-medium">Position Y: {position.y}px</label>
                    <input
                      type="range"
                      min="-50"
                      max="50"
                      value={position.y}
                      onChange={(e) => adjustOverlay('position-y', parseInt(e.target.value))}
                      className="w-full"
                    />
                  </div>
                  
                  {/* Scale */}
                  <div>
                    <label className="text-sm text-gray-700 font-medium">Size: {(scale * 100).toFixed(0)}%</label>
                    <input
                      type="range"
                      min="0.5"
                      max="1.5"
                      step="0.05"
                      value={scale}
                      onChange={(e) => adjustOverlay('scale', parseFloat(e.target.value))}
                      className="w-full"
                    />
                  </div>
                  
                  {/* Rotation */}
                  <div>
                    <label className="text-sm text-gray-700 font-medium">Rotation: {rotation}°</label>
                    <input
                      type="range"
                      min="-15"
                      max="15"
                      value={rotation}
                      onChange={(e) => adjustOverlay('rotation', parseInt(e.target.value))}
                      className="w-full"
                    />
                  </div>
                </div>
                
                <button
                  onClick={() => {
                    setPosition({ x: 0, y: 0 });
                    setScale(1.0);
                    setRotation(0);
                  }}
                  className="mt-3 w-full bg-gray-500 text-white py-2 px-4 rounded font-medium hover:bg-gray-600 transition-colors text-sm"
                >
                  Reset Adjustments
                </button>
              </div>
            )}

            <div className="flex gap-4">
              <button
                onClick={reset}
                className="flex-1 bg-gray-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-gray-700 transition-colors"
              >
                🔄 Try Another
              </button>
              <button
                onClick={() => setShowControls(!showControls)}
                className="flex-1 bg-purple-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-purple-700 transition-colors"
              >
                {showControls ? '🎨 Hide Controls' : '🎨 Adjust Fit'}
              </button>
              <button
                onClick={() => window.open(resultImage, '_blank')}
                className="flex-1 bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
              >
                💾 Download
              </button>
            </div>
          </div>
        )}

        {/* Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mt-6">
          <h3 className="font-semibold text-blue-900 mb-2">Tips for Best Results:</h3>
          <ul className="text-blue-800 space-y-1 text-sm">
            <li>• Use a clear, well-lit photo of yourself</li>
            <li>• Stand straight and face the camera</li>
            <li>• Choose a garment image with clear visibility</li>
            <li>• Avoid busy backgrounds for better accuracy</li>
          </ul>
        </div>
      </div>
    </div>
  );
}

export default ARTryOn;
