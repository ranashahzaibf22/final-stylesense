"""User Profile Management"""
from datetime import datetime
import re
import logging

logger = logging.getLogger(__name__)

class UserProfile:
    """User profile model for storing body measurements and preferences"""
    
    def __init__(self, user_id, measurements=None, body_shape=None, pose_references=None):
        self.user_id = self._sanitize_user_id(user_id)
        self.measurements = measurements or {}
        self.body_shape = body_shape or 'unknown'
        self.pose_references = pose_references or []
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def _sanitize_user_id(self, user_id):
        """Sanitize user ID to prevent injection"""
        if not user_id or not isinstance(user_id, str):
            raise ValueError("User ID must be a non-empty string")
        
        # Only allow alphanumeric, underscore, and hyphen
        if not re.match(r'^[a-zA-Z0-9_-]+$', user_id):
            raise ValueError("User ID contains invalid characters")
        
        if len(user_id) > 100:
            raise ValueError("User ID too long")
        
        return user_id
    
    def update_measurements(self, measurements):
        """Update body measurements with validation"""
        if not isinstance(measurements, dict):
            raise ValueError("Measurements must be a dictionary")
        
        # Validate measurement values
        for key, value in measurements.items():
            if not isinstance(key, str):
                raise ValueError(f"Measurement key must be string: {key}")
            
            if not isinstance(value, (int, float)):
                raise ValueError(f"Measurement value must be numeric: {value}")
            
            if value < 0 or value > 10:  # Reasonable bounds for normalized measurements
                raise ValueError(f"Measurement value out of range: {value}")
        
        self.measurements = measurements
        self.updated_at = datetime.utcnow()
    
    def update_body_shape(self, body_shape):
        """Update body shape classification with validation"""
        if not isinstance(body_shape, str):
            raise ValueError("Body shape must be a string")
        
        valid_shapes = ['inverted_triangle', 'pear', 'hourglass', 'rectangle', 
                        'average', 'balanced', 'unknown']
        
        if body_shape not in valid_shapes:
            raise ValueError(f"Invalid body shape: {body_shape}")
        
        self.body_shape = body_shape
        self.updated_at = datetime.utcnow()
    
    def add_pose_reference(self, pose_data):
        """Add pose reference image data"""
        if not isinstance(pose_data, dict):
            raise ValueError("Pose data must be a dictionary")
        
        # Limit number of pose references
        if len(self.pose_references) >= 10:
            self.pose_references.pop(0)  # Remove oldest
        
        pose_data['timestamp'] = datetime.utcnow().isoformat()
        self.pose_references.append(pose_data)
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert profile to dictionary"""
        return {
            'user_id': self.user_id,
            'measurements': self.measurements,
            'body_shape': self.body_shape,
            'pose_references': self.pose_references,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create profile from dictionary"""
        profile = cls(
            user_id=data['user_id'],
            measurements=data.get('measurements', {}),
            body_shape=data.get('body_shape', 'unknown'),
            pose_references=data.get('pose_references', [])
        )
        
        if 'created_at' in data:
            profile.created_at = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data:
            profile.updated_at = datetime.fromisoformat(data['updated_at'])
        
        return profile


class UserProfileManager:
    """Manager for user profile operations"""
    
    def __init__(self, db_connection=None):
        self.db = db_connection
        self._cache = {}  # Simple in-memory cache
    
    def create_profile(self, user_id, measurements=None, body_shape=None):
        """Create a new user profile"""
        try:
            # Check if profile already exists
            if self.get_profile(user_id):
                raise ValueError(f"Profile already exists for user: {user_id}")
            
            profile = UserProfile(user_id, measurements, body_shape)
            
            # Save to database if available
            if self.db:
                self.db.insert_one('user_profiles', profile.to_dict())
            
            # Cache the profile
            self._cache[user_id] = profile
            
            logger.info(f"Created profile for user: {user_id}")
            return profile
        
        except Exception as e:
            logger.error(f"Error creating profile: {e}")
            raise
    
    def get_profile(self, user_id):
        """Get user profile by ID"""
        try:
            # Sanitize user ID
            user_id = UserProfile('_temp')._sanitize_user_id(user_id)
            
            # Check cache first
            if user_id in self._cache:
                return self._cache[user_id]
            
            # Query database if available
            if self.db:
                data = self.db.find_one('user_profiles', {'user_id': user_id})
                if data:
                    profile = UserProfile.from_dict(data)
                    self._cache[user_id] = profile
                    return profile
            
            return None
        
        except Exception as e:
            logger.error(f"Error getting profile: {e}")
            return None
    
    def update_profile(self, user_id, updates):
        """Update user profile"""
        try:
            profile = self.get_profile(user_id)
            
            if not profile:
                raise ValueError(f"Profile not found for user: {user_id}")
            
            # Apply updates
            if 'measurements' in updates:
                profile.update_measurements(updates['measurements'])
            
            if 'body_shape' in updates:
                profile.update_body_shape(updates['body_shape'])
            
            if 'pose_reference' in updates:
                profile.add_pose_reference(updates['pose_reference'])
            
            # Save to database
            if self.db:
                self.db.update_one(
                    'user_profiles',
                    {'user_id': user_id},
                    profile.to_dict()
                )
            
            # Update cache
            self._cache[user_id] = profile
            
            logger.info(f"Updated profile for user: {user_id}")
            return profile
        
        except Exception as e:
            logger.error(f"Error updating profile: {e}")
            raise
    
    def delete_profile(self, user_id):
        """Delete user profile"""
        try:
            # Sanitize user ID
            user_id = UserProfile('_temp')._sanitize_user_id(user_id)
            
            # Delete from database
            if self.db:
                self.db.delete_one('user_profiles', {'user_id': user_id})
            
            # Remove from cache
            if user_id in self._cache:
                del self._cache[user_id]
            
            logger.info(f"Deleted profile for user: {user_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting profile: {e}")
            return False
