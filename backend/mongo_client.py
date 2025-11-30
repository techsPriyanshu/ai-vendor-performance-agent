"""
MongoDB client for vendor analytics
Handles connection and safe query execution
"""
from pymongo import MongoClient
from typing import Dict, List, Any, Optional
import os


class MongoDBClient:
    def __init__(self, connection_string: Optional[str] = None):
        """Initialize MongoDB client"""
        self.connection_string = connection_string or os.getenv(
            "MONGODB_URI", "mongodb://localhost:27017/"
        )
        self.db_name = os.getenv("MONGODB_DB", "vendor_analytics")
        self.client = None
        self.db = None
        
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(
                self.connection_string,
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            self.client.server_info()
            self.db = self.client[self.db_name]
            return True
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
    
    def execute_aggregation(
        self, 
        collection: str, 
        pipeline: List[Dict], 
        max_time_ms: int = 10000
    ) -> Dict[str, Any]:
        """
        Execute aggregation pipeline safely
        
        Args:
            collection: Collection name
            pipeline: Aggregation pipeline
            max_time_ms: Maximum execution time
            
        Returns:
            {"status": "success", "data": [...]} or {"status": "error", "error": "..."}
        """
        try:
            if self.db is None:
                return {
                    "status": "error",
                    "error": "Database not connected"
                }
            
            result = list(
                self.db[collection].aggregate(
                    pipeline,
                    maxTimeMS=max_time_ms,
                    allowDiskUse=False
                )
            )
            
            return {
                "status": "success",
                "data": result
            }
        except Exception as e:
            return {
                "status": "error",
                "error": f"Aggregation failed: {str(e)}"
            }
    
    def get_collection_count(self, collection: str) -> int:
        """Get document count for a collection"""
        try:
            if self.db is None:
                return 0
            return self.db[collection].count_documents({})
        except:
            return 0
