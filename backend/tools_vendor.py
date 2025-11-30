"""
5 Predefined vendor analytics tools with hardcoded MongoDB aggregations
"""
from typing import Dict, Any
from datetime import datetime, timedelta
from backend.mongo_client import MongoDBClient
from backend.validators import (
    validate_vendor_id,
    validate_date_range,
    validate_limit,
    validate_last_n_weeks
)


class VendorAnalyticsTools:
    """Collection of vendor analytics tools"""
    
    def __init__(self, mongo_client: MongoDBClient):
        self.mongo = mongo_client
    
    def get_vendor_summary(self, vendor_id: str, date_range: Dict) -> Dict[str, Any]:
        """
        Tool 1: Get vendor summary with counts and metrics
        
        Args:
            vendor_id: Vendor identifier
            date_range: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
            
        Returns:
            {"status": "success", "data": {...}} or {"status": "error", "error": "..."}
        """
        # Validate inputs
        validation = validate_vendor_id(vendor_id)
        if not validation["valid"]:
            return {"status": "error", "error": validation["error"]}
        
        validation = validate_date_range(date_range)
        if not validation["valid"]:
            return {"status": "error", "error": validation["error"]}
        
        # Parse dates
        start_date = datetime.strptime(date_range["start"], "%Y-%m-%d")
        end_date = datetime.strptime(date_range["end"], "%Y-%m-%d")
        
        # Predefined aggregation pipeline
        pipeline = [
            {
                "$match": {
                    "vendorId": vendor_id,
                    "sharedDate": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": "$vendorId",
                    "shared": {"$sum": 1},
                    "interviewed": {
                        "$sum": {
                            "$cond": [{"$ne": ["$interviewDate", None]}, 1, 0]
                        }
                    },
                    "onboarded": {
                        "$sum": {
                            "$cond": [{"$ne": ["$onboardingDate", None]}, 1, 0]
                        }
                    },
                    "avgDaysToOnboard": {
                        "$avg": {
                            "$cond": [
                                {"$ne": ["$onboardingDate", None]},
                                {
                                    "$divide": [
                                        {"$subtract": ["$onboardingDate", "$sharedDate"]},
                                        86400000  # milliseconds to days
                                    ]
                                },
                                None
                            ]
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "vendorId": "$_id",
                    "shared": 1,
                    "interviewed": 1,
                    "onboarded": 1,
                    "joinRatio": {
                        "$cond": [
                            {"$gt": ["$shared", 0]},
                            {"$divide": ["$onboarded", "$shared"]},
                            0
                        ]
                    },
                    "avgTimeToOnboarding": {"$ifNull": ["$avgDaysToOnboard", 0]}
                }
            }
        ]
        
        result = self.mongo.execute_aggregation("shares", pipeline)
        
        if result["status"] == "success":
            data = result["data"]
            if data:
                return {"status": "success", "data": data[0]}
            else:
                return {
                    "status": "success",
                    "data": {
                        "vendorId": vendor_id,
                        "shared": 0,
                        "interviewed": 0,
                        "onboarded": 0,
                        "joinRatio": 0,
                        "avgTimeToOnboarding": 0
                    }
                }
        
        return result
    
    def compare_vendors(self, vendor_a: str, vendor_b: str, date_range: Dict) -> Dict[str, Any]:
        """
        Tool 2: Compare two vendors side-by-side
        
        Args:
            vendor_a: First vendor ID
            vendor_b: Second vendor ID
            date_range: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
            
        Returns:
            {"status": "success", "data": {"vendorA": {...}, "vendorB": {...}}}
        """
        # Validate inputs
        validation = validate_vendor_id(vendor_a)
        if not validation["valid"]:
            return {"status": "error", "error": f"vendorA: {validation['error']}"}
        
        validation = validate_vendor_id(vendor_b)
        if not validation["valid"]:
            return {"status": "error", "error": f"vendorB: {validation['error']}"}
        
        validation = validate_date_range(date_range)
        if not validation["valid"]:
            return {"status": "error", "error": validation["error"]}
        
        # Get summary for both vendors
        result_a = self.get_vendor_summary(vendor_a, date_range)
        result_b = self.get_vendor_summary(vendor_b, date_range)
        
        if result_a["status"] == "error":
            return result_a
        if result_b["status"] == "error":
            return result_b
        
        return {
            "status": "success",
            "data": {
                "vendorA": result_a["data"],
                "vendorB": result_b["data"]
            }
        }
    
    def get_vendor_trend(self, vendor_id: str, last_n_weeks: int) -> Dict[str, Any]:
        """
        Tool 3: Get weekly trend for a vendor
        
        Args:
            vendor_id: Vendor identifier
            last_n_weeks: Number of weeks to analyze
            
        Returns:
            {"status": "success", "data": [{week, year, shared, interviewed, onboarded}, ...]}
        """
        # Validate inputs
        validation = validate_vendor_id(vendor_id)
        if not validation["valid"]:
            return {"status": "error", "error": validation["error"]}
        
        validation = validate_last_n_weeks(last_n_weeks)
        if not validation["valid"]:
            return {"status": "error", "error": validation["error"]}
        
        # Calculate cutoff date
        cutoff_date = datetime.now() - timedelta(weeks=last_n_weeks)
        
        # Predefined aggregation pipeline
        pipeline = [
            {
                "$match": {
                    "vendorId": vendor_id,
                    "sharedDate": {"$gte": cutoff_date}
                }
            },
            {
                "$group": {
                    "_id": {
                        "week": {"$isoWeek": "$sharedDate"},
                        "year": {"$year": "$sharedDate"}
                    },
                    "shared": {"$sum": 1},
                    "interviewed": {
                        "$sum": {
                            "$cond": [{"$ne": ["$interviewDate", None]}, 1, 0]
                        }
                    },
                    "onboarded": {
                        "$sum": {
                            "$cond": [{"$ne": ["$onboardingDate", None]}, 1, 0]
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "week": "$_id.week",
                    "year": "$_id.year",
                    "shared": 1,
                    "interviewed": 1,
                    "onboarded": 1
                }
            },
            {
                "$sort": {"year": 1, "week": 1}
            }
        ]
        
        return self.mongo.execute_aggregation("shares", pipeline)
    
    def vendor_top_performers(self, limit: int, date_range: Dict) -> Dict[str, Any]:
        """
        Tool 4: Get top performing vendors by onboardings
        
        Args:
            limit: Number of top vendors to return
            date_range: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
            
        Returns:
            {"status": "success", "data": [{vendorId, onboarded, shared, joinRatio}, ...]}
        """
        # Validate inputs
        validation = validate_limit(limit)
        if not validation["valid"]:
            return {"status": "error", "error": validation["error"]}
        
        validation = validate_date_range(date_range)
        if not validation["valid"]:
            return {"status": "error", "error": validation["error"]}
        
        # Parse dates
        start_date = datetime.strptime(date_range["start"], "%Y-%m-%d")
        end_date = datetime.strptime(date_range["end"], "%Y-%m-%d")
        
        # Predefined aggregation pipeline
        pipeline = [
            {
                "$match": {
                    "sharedDate": {
                        "$gte": start_date,
                        "$lte": end_date
                    }
                }
            },
            {
                "$group": {
                    "_id": "$vendorId",
                    "shared": {"$sum": 1},
                    "onboarded": {
                        "$sum": {
                            "$cond": [{"$ne": ["$onboardingDate", None]}, 1, 0]
                        }
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "vendorId": "$_id",
                    "shared": 1,
                    "onboarded": 1,
                    "joinRatio": {
                        "$cond": [
                            {"$gt": ["$shared", 0]},
                            {"$divide": ["$onboarded", "$shared"]},
                            0
                        ]
                    }
                }
            },
            {
                "$sort": {"onboarded": -1}
            },
            {
                "$limit": limit
            }
        ]
        
        return self.mongo.execute_aggregation("shares", pipeline)
    
    def vendor_failed_submissions(self, date_range: Dict) -> Dict[str, Any]:
        """
        Tool 5: Get failed submissions with reasons
        
        Args:
            date_range: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
            
        Returns:
            {"status": "success", "data": {totalRejections, topReasons: [{reason, count}]}}
        """
        # Validate inputs
        validation = validate_date_range(date_range)
        if not validation["valid"]:
            return {"status": "error", "error": validation["error"]}
        
        # Parse dates
        start_date = datetime.strptime(date_range["start"], "%Y-%m-%d")
        end_date = datetime.strptime(date_range["end"], "%Y-%m-%d")
        
        # Predefined aggregation pipeline for total rejections
        pipeline_total = [
            {
                "$match": {
                    "sharedDate": {
                        "$gte": start_date,
                        "$lte": end_date
                    },
                    "status": "rejected"
                }
            },
            {
                "$count": "totalRejections"
            }
        ]
        
        # Predefined aggregation pipeline for top reasons
        pipeline_reasons = [
            {
                "$match": {
                    "sharedDate": {
                        "$gte": start_date,
                        "$lte": end_date
                    },
                    "status": "rejected"
                }
            },
            {
                "$group": {
                    "_id": "$rejectionReason",
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "reason": "$_id",
                    "count": 1
                }
            },
            {
                "$sort": {"count": -1}
            },
            {
                "$limit": 5
            }
        ]
        
        result_total = self.mongo.execute_aggregation("shares", pipeline_total)
        result_reasons = self.mongo.execute_aggregation("shares", pipeline_reasons)
        
        if result_total["status"] == "error":
            return result_total
        if result_reasons["status"] == "error":
            return result_reasons
        
        total = result_total["data"][0]["totalRejections"] if result_total["data"] else 0
        
        return {
            "status": "success",
            "data": {
                "totalRejections": total,
                "topReasons": result_reasons["data"]
            }
        }
