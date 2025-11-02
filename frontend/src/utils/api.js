/**
 * API utility for making requests to the backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

/**
 * Generic API request handler
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'API request failed');
    }

    return await response.json();
  } catch (error) {
    console.error('API Request Error:', error);
    throw error;
  }
}

/**
 * Get system health status
 */
export async function getHealthStatus() {
  return apiRequest('/health');
}

/**
 * Upload wardrobe item
 */
export async function uploadWardrobeItem(file, metadata) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('user_id', metadata.user_id || 'default_user');
  formData.append('category', metadata.category || 'uncategorized');
  formData.append('color', metadata.color || 'unknown');

  return apiRequest('/wardrobe/upload', {
    method: 'POST',
    body: formData,
  });
}

/**
 * Get wardrobe items for a user
 */
export async function getWardrobeItems(userId = 'default_user') {
  return apiRequest(`/wardrobe/${userId}`);
}

/**
 * Get outfit recommendations
 */
export async function getRecommendations(params = {}) {
  const queryParams = new URLSearchParams({
    user_id: params.user_id || 'default_user',
    occasion: params.occasion || 'casual',
    weather: params.weather || 'moderate',
  });

  return apiRequest(`/recommendations?${queryParams}`);
}

/**
 * Analyze body shape from image
 */
export async function analyzeBodyShape(file) {
  const formData = new FormData();
  formData.append('file', file);

  return apiRequest('/body-shape/analyze', {
    method: 'POST',
    body: formData,
  });
}

/**
 * Apply AR virtual try-on
 */
export async function applyARTryOn(personImage, garmentImage) {
  const formData = new FormData();
  formData.append('person_image', personImage);
  formData.append('garment_image', garmentImage);

  return apiRequest('/ar-tryon', {
    method: 'POST',
    body: formData,
  });
}

/**
 * Get product catalogue
 */
export async function getProductCatalogue(params = {}) {
  const queryParams = new URLSearchParams({
    category: params.category || '',
    limit: params.limit || 50,
  });

  return apiRequest(`/product-catalogue?${queryParams}`);
}
