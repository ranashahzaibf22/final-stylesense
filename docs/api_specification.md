# StyleSense.AI - API Specification

## Base URL
```
Development: http://localhost:5000/api
Production: https://api.stylesense.ai/api (example)
```

## Authentication
Currently, the API uses a simple user_id parameter. Future versions will implement JWT-based authentication.

## Common Response Format

### Success Response
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Optional success message"
}
```

### Error Response
```json
{
  "error": "Error message describing what went wrong",
  "status_code": 400
}
```

## API Endpoints

### 1. Health Check

**GET** `/health`

Check system status and availability.

**Response**
```json
{
  "status": "healthy",
  "timestamp": "2024-11-02T10:30:00.000Z",
  "database": "connected",
  "ml_models": "available",
  "version": "1.0.0"
}
```

---

### 2. Upload Wardrobe Item

**POST** `/wardrobe/upload`

Upload a clothing item to the user's wardrobe.

**Request**
- Content-Type: `multipart/form-data`

**Form Data**
| Field    | Type   | Required | Description                    |
|----------|--------|----------|--------------------------------|
| file     | File   | Yes      | Image file (PNG, JPG, JPEG, GIF, WEBP) |
| user_id  | String | No       | User identifier (default: "default_user") |
| category | String | No       | Item category (default: "uncategorized") |
| color    | String | No       | Item color (default: "unknown") |

**Example Request**
```bash
curl -X POST http://localhost:5000/api/wardrobe/upload \
  -F "file=@/path/to/shirt.jpg" \
  -F "user_id=user123" \
  -F "category=tops" \
  -F "color=blue"
```

**Response (201 Created)**
```json
{
  "success": true,
  "message": "File uploaded successfully",
  "data": {
    "id": "64a1b2c3d4e5f6g7h8i9j0k1",
    "filename": "20241102_103000_shirt.jpg",
    "original_filename": "shirt.jpg",
    "category": "tops",
    "color": "blue",
    "upload_date": "2024-11-02T10:30:00.000Z",
    "file_path": "/uploads/20241102_103000_shirt.jpg"
  }
}
```

**Error Responses**
- `400 Bad Request`: Invalid file type or missing file
- `413 Payload Too Large`: File exceeds 16MB limit
- `500 Internal Server Error`: Server error during upload

---

### 3. Get Wardrobe Items

**GET** `/wardrobe/{user_id}`

Retrieve all wardrobe items for a user.

**Parameters**
| Parameter | Type   | Required | Description      |
|-----------|--------|----------|------------------|
| user_id   | String | Yes      | User identifier  |

**Example Request**
```bash
curl http://localhost:5000/api/wardrobe/user123
```

**Response (200 OK)**
```json
{
  "success": true,
  "count": 5,
  "items": [
    {
      "_id": "64a1b2c3d4e5f6g7h8i9j0k1",
      "user_id": "user123",
      "filename": "20241102_103000_shirt.jpg",
      "category": "tops",
      "color": "blue",
      "upload_date": "2024-11-02T10:30:00.000Z"
    }
    // ... more items
  ]
}
```

**Error Responses**
- `503 Service Unavailable`: Database not connected
- `500 Internal Server Error`: Server error

---

### 4. Get Recommendations

**GET** `/recommendations`

Generate AI-powered outfit recommendations.

**Query Parameters**
| Parameter | Type   | Required | Default        | Description                     |
|-----------|--------|----------|----------------|---------------------------------|
| user_id   | String | No       | "default_user" | User identifier                 |
| occasion  | String | No       | "casual"       | Event type (casual, formal, party, workout) |
| weather   | String | No       | "moderate"     | Weather condition (hot, cold, rainy, moderate) |

**Example Request**
```bash
curl "http://localhost:5000/api/recommendations?user_id=user123&occasion=formal&weather=cold"
```

**Response (200 OK)**
```json
{
  "success": true,
  "user_id": "user123",
  "recommendations": [
    {
      "outfit_id": 1,
      "items": [
        {
          "type": "top",
          "item": "dress shirt",
          "color": "white"
        },
        {
          "type": "bottom",
          "item": "suit trousers",
          "color": "black"
        },
        {
          "type": "footwear",
          "item": "oxfords"
        }
      ],
      "occasion": "formal",
      "weather": "cold",
      "confidence": 0.85,
      "description": "Formal outfit: dress shirt with suit trousers",
      "method": "rule_based_fallback",
      "weather_adjusted": true
    }
    // ... more recommendations
  ]
}
```

**Error Responses**
- `500 Internal Server Error`: Server error during generation

---

### 5. Analyze Body Shape

**POST** `/body-shape/analyze`

Analyze body shape from an image using MediaPipe or OpenCV.

**Request**
- Content-Type: `multipart/form-data`

**Form Data**
| Field | Type | Required | Description        |
|-------|------|----------|--------------------|
| file  | File | Yes      | Person image file  |

**Example Request**
```bash
curl -X POST http://localhost:5000/api/body-shape/analyze \
  -F "file=@/path/to/person.jpg"
```

**Response (200 OK)**
```json
{
  "success": true,
  "analysis": {
    "body_type": "hourglass",
    "measurements": {
      "shoulder_width": 0.42,
      "hip_width": 0.40,
      "ratio": 1.05
    },
    "confidence": 0.85,
    "method": "mediapipe",
    "landmarks_detected": 33
  }
}
```

**Body Types**
- `inverted_triangle`: Shoulders wider than hips
- `pear`: Hips wider than shoulders
- `hourglass`: Balanced proportions
- `rectangle`: Similar measurements
- `average`: Default fallback

**Error Responses**
- `400 Bad Request`: No file or invalid file type
- `500 Internal Server Error`: Processing error

---

### 6. AR Virtual Try-On

**POST** `/ar-tryon`

Apply virtual try-on effect to overlay garment on person image.

**Request**
- Content-Type: `multipart/form-data`

**Form Data**
| Field         | Type | Required | Description          |
|---------------|------|----------|----------------------|
| person_image  | File | Yes      | Person photo         |
| garment_image | File | Yes      | Garment to try on    |

**Example Request**
```bash
curl -X POST http://localhost:5000/api/ar-tryon \
  -F "person_image=@/path/to/person.jpg" \
  -F "garment_image=@/path/to/shirt.jpg"
```

**Response (200 OK)**
```json
{
  "success": true,
  "result_url": "/api/uploads/tryon_result_person.jpg",
  "method": "opencv_fallback"
}
```

**Methods**
- `ml`: VTON-HD model (when available)
- `opencv_fallback`: OpenCV-based overlay
- `fallback`: Returns original person image

**Error Responses**
- `400 Bad Request`: Missing files or invalid file types
- `500 Internal Server Error`: Processing error

---

### 7. Get Product Catalogue

**GET** `/product-catalogue`

Retrieve products from the catalogue with optional filtering.

**Query Parameters**
| Parameter | Type    | Required | Default | Description                    |
|-----------|---------|----------|---------|--------------------------------|
| category  | String  | No       | None    | Filter by category             |
| limit     | Integer | No       | 50      | Maximum number of products (max: 100) |

**Example Request**
```bash
curl "http://localhost:5000/api/product-catalogue?category=tops&limit=10"
```

**Response (200 OK)**
```json
{
  "success": true,
  "count": 10,
  "products": [
    {
      "id": "prod-001",
      "name": "Fashion Item 1",
      "category": "tops",
      "price": 29.99,
      "image_url": "/api/catalogue/images/product_1.jpg",
      "description": "Stylish tops item"
    }
    // ... more products
  ]
}
```

**Categories**
- tops
- bottoms
- dresses
- outerwear
- shoes
- bags
- accessories

**Error Responses**
- `500 Internal Server Error`: Server error

---

### 8. Serve Uploaded Files

**GET** `/uploads/{filename}`

Retrieve uploaded images.

**Parameters**
| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| filename  | String | Yes      | File name   |

**Example Request**
```bash
curl http://localhost:5000/api/uploads/20241102_103000_shirt.jpg
```

**Response**
- Returns the image file with appropriate content-type

**Error Responses**
- `404 Not Found`: File doesn't exist

---

## Rate Limiting

Currently not implemented. Future versions will include:
- 100 requests per minute per IP
- 1000 requests per hour per user

## CORS Policy

The API accepts requests from:
- Development: `http://localhost:3000`
- Production: Configure via `CORS_ORIGINS` environment variable

## Error Codes

| Code | Description                    |
|------|--------------------------------|
| 400  | Bad Request                    |
| 404  | Not Found                      |
| 413  | Payload Too Large              |
| 500  | Internal Server Error          |
| 503  | Service Unavailable            |

## File Upload Constraints

- **Maximum File Size**: 16 MB
- **Allowed Formats**: PNG, JPG, JPEG, GIF, WEBP
- **Validation**: MIME type and extension checking

## Testing with Postman

### Collection Setup

1. **Base URL Variable**
   - Variable: `base_url`
   - Value: `http://localhost:5000/api`

2. **Health Check**
   ```
   GET {{base_url}}/health
   ```

3. **Upload Wardrobe Item**
   ```
   POST {{base_url}}/wardrobe/upload
   Body: form-data
     - file: [select image file]
     - user_id: test_user
     - category: tops
     - color: blue
   ```

4. **Get Recommendations**
   ```
   GET {{base_url}}/recommendations?user_id=test_user&occasion=casual
   ```

5. **Body Shape Analysis**
   ```
   POST {{base_url}}/body-shape/analyze
   Body: form-data
     - file: [select person image]
   ```

6. **AR Try-On**
   ```
   POST {{base_url}}/ar-tryon
   Body: form-data
     - person_image: [select person image]
     - garment_image: [select garment image]
   ```

## SDK Examples

### JavaScript/Axios
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000/api'
});

// Upload wardrobe item
const uploadItem = async (file, metadata) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('user_id', metadata.user_id);
  formData.append('category', metadata.category);
  
  const response = await api.post('/wardrobe/upload', formData);
  return response.data;
};

// Get recommendations
const getRecommendations = async (userId, occasion, weather) => {
  const response = await api.get('/recommendations', {
    params: { user_id: userId, occasion, weather }
  });
  return response.data;
};
```

### Python/Requests
```python
import requests

BASE_URL = 'http://localhost:5000/api'

# Upload wardrobe item
def upload_item(file_path, user_id, category, color):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        data = {
            'user_id': user_id,
            'category': category,
            'color': color
        }
        response = requests.post(f'{BASE_URL}/wardrobe/upload', 
                                files=files, data=data)
        return response.json()

# Get recommendations
def get_recommendations(user_id, occasion='casual', weather='moderate'):
    params = {
        'user_id': user_id,
        'occasion': occasion,
        'weather': weather
    }
    response = requests.get(f'{BASE_URL}/recommendations', params=params)
    return response.json()
```

---

**Version**: 1.0.0  
**Last Updated**: November 2024  
**Maintainer**: StyleSense.AI Team
