/**
 * Camera utility for capturing images
 */

/**
 * Check if camera is available
 */
export function isCameraAvailable() {
  return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
}

/**
 * Request camera access
 */
export async function requestCameraAccess(videoElement, constraints = {}) {
  if (!isCameraAvailable()) {
    throw new Error('Camera not available on this device');
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: constraints.video || { facingMode: 'user' },
      audio: false,
      ...constraints,
    });

    if (videoElement) {
      videoElement.srcObject = stream;
      await videoElement.play();
    }

    return stream;
  } catch (error) {
    console.error('Camera access error:', error);
    throw new Error(`Camera access denied: ${error.message}`);
  }
}

/**
 * Stop camera stream
 */
export function stopCameraStream(stream) {
  if (stream) {
    stream.getTracks().forEach(track => track.stop());
  }
}

/**
 * Capture image from video element
 */
export function captureImageFromVideo(videoElement, width, height) {
  const canvas = document.createElement('canvas');
  canvas.width = width || videoElement.videoWidth;
  canvas.height = height || videoElement.videoHeight;

  const context = canvas.getContext('2d');
  context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

  return canvas.toDataURL('image/png');
}

/**
 * Convert data URL to File object
 */
export function dataURLtoFile(dataURL, filename) {
  const arr = dataURL.split(',');
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);

  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }

  return new File([u8arr], filename, { type: mime });
}

/**
 * Get available cameras
 */
export async function getAvailableCameras() {
  if (!isCameraAvailable()) {
    return [];
  }

  try {
    const devices = await navigator.mediaDevices.enumerateDevices();
    return devices.filter(device => device.kind === 'videoinput');
  } catch (error) {
    console.error('Error enumerating devices:', error);
    return [];
  }
}
