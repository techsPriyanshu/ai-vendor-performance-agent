"""
Prompts and mock LLM mapping for vendor analytics agent
Phase-2: Enhanced with expanded patterns and better NL understanding
"""

AGENT_INSTRUCTION = """
You are a Vendor Performance Analytics Agent.

Your job is to:
1. Understand natural language queries about vendor performance
2. Map them to one of 5 available analytics tools
3. Extract required parameters from the query or use memory for follow-ups
4. Validate all inputs before execution
5. Return human-friendly, dashboard-quality results

Available Tools:
1. get_vendor_summary(vendorId, dateRange) - Get summary metrics for a vendor
2. compare_vendors(vendorA, vendorB, dateRange) - Compare two vendors
3. get_vendor_trend(vendorId, lastNWeeks) - Get weekly trend for a vendor
4. vendor_top_performers(limit, dateRange) - Get top performing vendors
5. vendor_failed_submissions(dateRange) - Get failed submissions report

Features:
- Memory-aware: Remembers last vendorId, dateRange, and lastNWeeks for follow-up queries
- Smart validation: Checks all parameters and provides helpful error messages
- Context retention: Handles vague queries like "show trend" by using stored context

Always validate inputs and provide clear, actionable insights.
"""

# Mock LLM mapping: patterns → (tool_name, param_extractor)
# Expanded with multiple patterns for better matching
MOCK_PATTERNS = [
    # Pattern 1: Vendor summary
    {
        "patterns": [
            "show vendor summary",
            "vendor summary for",
            "get summary for vendor",
            "summary of vendor",
            "vendor performance for",
            "how is vendor",
            "vendor stats",
            "vendor metrics",
            "performance of vendor",
            "show me vendor"
        ],
        "tool": "get_vendor_summary",
        "priority": 2
    },
    
    # Pattern 2: Compare vendors
    {
        "patterns": [
            "compare vendor",
            "compare vendors",
            "vendor comparison",
            "difference between vendor",
            "vs vendor",
            "versus vendor",
            "vendor 1 vs vendor 2",
            "vendor 1 and vendor 2",
            "how do vendor",
            "which is better"
        ],
        "tool": "compare_vendors",
        "priority": 3
    },
    
    # Pattern 3: Vendor trend
    {
        "patterns": [
            "vendor trend",
            "trend for vendor",
            "weekly trend",
            "show me trend",
            "performance trend",
            "show trend",
            "now show trend",
            "trend over time",
            "historical performance",
            "week by week"
        ],
        "tool": "get_vendor_trend",
        "priority": 2
    },
    
    # Pattern 4: Top performers
    {
        "patterns": [
            "top vendor",
            "top performing vendor",
            "best vendor",
            "top 3 vendor",
            "top 5 vendor",
            "top 10 vendor",
            "highest performing",
            "best performing",
            "rank vendor",
            "leading vendor",
            "who are the best"
        ],
        "tool": "vendor_top_performers",
        "priority": 3
    },
    
    # Pattern 5: Failed submissions
    {
        "patterns": [
            "failed submission",
            "rejection",
            "failed candidate",
            "why are candidates rejected",
            "rejection reason",
            "why rejected",
            "failure reason",
            "what went wrong",
            "rejection analysis",
            "failed profiles"
        ],
        "tool": "vendor_failed_submissions",
        "priority": 3
    }
]


def mock_llm_parse(query: str) -> dict:
    """
    Mock LLM query parser - maps common patterns to tools
    Enhanced with priority-based matching and confidence scoring
    
    Args:
        query: Natural language query
        
    Returns:
        {
            "tool": tool_name,
            "params": {...},
            "confidence": float,
            "matched_pattern": str
        }
    """
    query_lower = query.lower()
    
    # Track all matches with scores
    matches = []
    
    # Try to match patterns
    for pattern_group in MOCK_PATTERNS:
        for pattern in pattern_group["patterns"]:
            if pattern in query_lower:
                # Calculate confidence based on pattern length and priority
                pattern_length_score = len(pattern) / len(query_lower)
                priority_score = pattern_group.get("priority", 1) * 0.1
                confidence = min(0.7 + pattern_length_score + priority_score, 0.95)
                
                matches.append({
                    "tool": pattern_group["tool"],
                    "pattern": pattern,
                    "confidence": confidence
                })
    
    # Select best match
    if matches:
        best_match = max(matches, key=lambda x: x["confidence"])
        params = extract_params_from_query(query, best_match["tool"])
        
        return {
            "tool": best_match["tool"],
            "params": params,
            "confidence": best_match["confidence"],
            "matched_pattern": best_match["pattern"]
        }
    
    # Default fallback for unrecognized queries
    return {
        "tool": "get_vendor_summary",
        "params": {},
        "confidence": 0.2,
        "matched_pattern": "fallback"
    }


def extract_params_from_query(query: str, tool_name: str) -> dict:
    """
    Extract parameters from natural language query
    Simple pattern matching for mock mode
    """
    import re
    from datetime import datetime, timedelta
    
    params = {}
    query_lower = query.lower()
    
    # Extract vendor IDs
    vendor_match = re.search(r'vendor[_\s]?(\d+)', query_lower)
    if vendor_match:
        vendor_num = vendor_match.group(1)
        params["vendorId"] = f"VENDOR_{vendor_num}"
    
    # Extract two vendors for comparison
    if tool_name == "compare_vendors":
        vendors = re.findall(r'vendor[_\s]?(\d+)', query_lower)
        if len(vendors) >= 2:
            params["vendorA"] = f"VENDOR_{vendors[0]}"
            params["vendorB"] = f"VENDOR_{vendors[1]}"
        else:
            params["vendorA"] = "VENDOR_1"
            params["vendorB"] = "VENDOR_2"
    
    # Extract limit
    limit_match = re.search(r'top\s+(\d+)', query_lower)
    if limit_match:
        params["limit"] = int(limit_match.group(1))
    elif tool_name == "vendor_top_performers":
        params["limit"] = 3
    
    # Extract weeks
    weeks_match = re.search(r'(\d+)\s+weeks?', query_lower)
    if weeks_match:
        params["lastNWeeks"] = int(weeks_match.group(1))
    elif tool_name == "get_vendor_trend":
        params["lastNWeeks"] = 8
    
    # Extract date range
    if "last month" in query_lower:
        end = datetime.now()
        start = end - timedelta(days=30)
        params["dateRange"] = {
            "start": start.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d")
        }
    elif "last week" in query_lower:
        end = datetime.now()
        start = end - timedelta(days=7)
        params["dateRange"] = {
            "start": start.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d")
        }
    elif "this year" in query_lower or "2024" in query:
        params["dateRange"] = {
            "start": "2024-01-01",
            "end": "2024-12-31"
        }
    else:
        # Default to last 3 months
        end = datetime.now()
        start = end - timedelta(days=90)
        params["dateRange"] = {
            "start": start.strftime("%Y-%m-%d"),
            "end": end.strftime("%Y-%m-%d")
        }
    
    # Set default vendorId if needed
    if tool_name in ["get_vendor_summary", "get_vendor_trend"] and "vendorId" not in params:
        params["vendorId"] = "VENDOR_1"
    
    return params
