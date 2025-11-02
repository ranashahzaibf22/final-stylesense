"""MongoDB database connection and operations"""
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging
from config import Config

logger = logging.getLogger(__name__)

class Database:
    """MongoDB database handler"""
    
    def __init__(self):
        self.client = None
        self.db = None
        
    def connect(self):
        """Establish MongoDB connection"""
        try:
            self.client = MongoClient(
                Config.MONGODB_URI,
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            self.client.admin.command('ping')
            
            # Get database name from URI or use default
            db_name = Config.MONGODB_URI.split('/')[-1].split('?')[0] or 'stylesense'
            self.db = self.client[db_name]
            
            logger.info(f"Connected to MongoDB database: {db_name}")
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    def get_collection(self, name):
        """Get a collection by name"""
        if self.db is None:
            raise RuntimeError("Database not connected")
        return self.db[name]
    
    def insert_wardrobe_item(self, user_id, item_data):
        """Insert a wardrobe item"""
        collection = self.get_collection('wardrobe')
        item_data['user_id'] = user_id
        result = collection.insert_one(item_data)
        return str(result.inserted_id)
    
    def get_wardrobe_items(self, user_id):
        """Get all wardrobe items for a user"""
        collection = self.get_collection('wardrobe')
        items = list(collection.find({'user_id': user_id}))
        # Convert ObjectId to string
        for item in items:
            item['_id'] = str(item['_id'])
        return items
    
    def insert_recommendation(self, user_id, recommendation_data):
        """Insert a recommendation"""
        collection = self.get_collection('recommendations')
        recommendation_data['user_id'] = user_id
        result = collection.insert_one(recommendation_data)
        return str(result.inserted_id)
    
    def get_recommendations(self, user_id, limit=10):
        """Get recommendations for a user"""
        collection = self.get_collection('recommendations')
        recommendations = list(
            collection.find({'user_id': user_id})
            .sort('created_at', -1)
            .limit(limit)
        )
        for rec in recommendations:
            rec['_id'] = str(rec['_id'])
        return recommendations

# Global database instance
db = Database()
