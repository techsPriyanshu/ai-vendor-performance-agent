"""
Input validators for vendor analytics tools
Enhanced with structured errors, memory support, and range validation
"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


def validate_vendor_id(vendor_id: Optional[str], memory=None) -> Dict[str, Any]:
    """
    Validate vendor ID with memory support
    
    Args:
        vendor_id: Vendor identifier
        memory: Memory object to retrieve last vendorId if missing
        
    Returns:
        {"valid": bool, "error": str, "value": str, "from_memory": bool}
    """
    from_memory = False
    
    # Try to get from memory if missing
    if not vendor_id and memory:
        vendor_id = memory.get_last_vendor_id()
        if vendor_id:
            from_memory = True
    
    if not vendor_id:
        return {
            "valid": False,
            "error": "VendorId is required. Please specify a vendor or run a query with a vendor first.",
            "status": "error"
        }
    
    if not isinstance(vendor_id, str):
        return {
            "valid": False,
            "error": "VendorId must be a string",
            "status": "error"
        }
    
    # Validate format (VENDOR_X)
    if not vendor_id.startswith("VENDOR_"):
        return {
            "valid": False,
            "error": f"VendorId '{vendor_id}' has invalid format. Expected format: VENDOR_X",
            "status": "error"
        }
    
    return {
        "valid": True,
        "value": vendor_id,
        "from_memory": from_memory
    }


def validate_date_range(date_range: Optional[Dict], memory=None) -> Dict[str, Any]:
    """
    Validate date range with memory support and range checks
    Expected format: {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}
    
    Args:
        date_range: Date range dictionary
        memory: Memory object to retrieve last dateRange if missing
        
    Returns:
        {"valid": bool, "error": str, "value": dict, "from_memory": bool}
    """
    from_memory = False
    
    # Try to get from memory if missing
    if not date_range and memory:
        date_range = memory.get_last_date_range()
        if date_range:
            from_memory = True
    
    if not date_range:
        return {
            "valid": False,
            "error": "DateRange is required. Please specify a date range (e.g., 'in 2024', 'last month').",
            "status": "error"
        }
    
    if not isinstance(date_range, dict):
        return {
            "valid": False,
            "error": "DateRange must be a dictionary with 'start' and 'end'",
            "status": "error"
        }
    
    if "start" not in date_range or "end" not in date_range:
        return {
            "valid": False,
            "error": "DateRange must contain 'start' and 'end' keys",
            "status": "error"
        }
    
    # Try parsing dates
    try:
        start_date = datetime.strptime(date_range["start"], "%Y-%m-%d")
        end_date = datetime.strptime(date_range["end"], "%Y-%m-%d")
    except ValueError:
        return {
            "valid": False,
            "error": "Dates must be in YYYY-MM-DD format",
            "status": "error"
        }
    
    # Check if end is after start
    if end_date < start_date:
        return {
            "valid": False,
            "error": "End date must be after start date",
            "status": "error"
        }
    
    # Check if range is too long (> 1 year)
    date_diff = end_date - start_date
    if date_diff.days > 365:
        return {
            "valid": False,
            "error": "Please specify a date range up to 1 year only. Your range spans {} days.".format(date_diff.days),
            "status": "error"
        }
    
    return {
        "valid": True,
        "value": date_range,
        "from_memory": from_memory
    }


def validate_limit(limit: Optional[int], memory=None) -> Dict[str, Any]:
    """
    Validate limit parameter
    
    Args:
        limit: Number of results to return
        memory: Memory object (not used for limit, but kept for consistency)
        
    Returns:
        {"valid": bool, "error": str, "value": int}
    """
    if limit is None:
        return {
            "valid": False,
            "error": "Limit is required. Please specify how many results you want (e.g., 'top 5').",
            "status": "error"
        }
    
    if not isinstance(limit, int):
        return {
            "valid": False,
            "error": "Limit must be an integer",
            "status": "error"
        }
    
    if limit <= 0:
        return {
            "valid": False,
            "error": "Limit must be greater than 0",
            "status": "error"
        }
    
    if limit > 100:
        return {
            "valid": False,
            "error": "Limit cannot exceed 100. Please request 100 or fewer results.",
            "status": "error"
        }
    
    return {
        "valid": True,
        "value": limit
    }


def validate_last_n_weeks(weeks: Optional[int], memory=None) -> Dict[str, Any]:
    """
    Validate lastNWeeks parameter with memory support
    
    Args:
        weeks: Number of weeks to analyze
        memory: Memory object to retrieve last lastNWeeks if missing
        
    Returns:
        {"valid": bool, "error": str, "value": int, "from_memory": bool}
    """
    from_memory = False
    
    # Try to get from memory if missing
    if weeks is None and memory:
        weeks = memory.get("lastNWeeks")
        if weeks:
            from_memory = True
    
    if weeks is None:
        return {
            "valid": False,
            "error": "LastNWeeks is required. Please specify number of weeks (e.g., 'last 8 weeks').",
            "status": "error"
        }
    
    if not isinstance(weeks, int):
        return {
            "valid": False,
            "error": "LastNWeeks must be an integer",
            "status": "error"
        }
    
    if weeks <= 0:
        return {
            "valid": False,
            "error": "LastNWeeks must be greater than 0",
            "status": "error"
        }
    
    if weeks > 52:
        return {
            "valid": False,
            "error": "LastNWeeks cannot exceed 52 (1 year). Please request 52 or fewer weeks.",
            "status": "error"
        }
    
    return {
        "valid": True,
        "value": weeks,
        "from_memory": from_memory
    }
