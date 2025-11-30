"""
ADK-based Vendor Analytics Agent
Enhanced with memory integration, validation, and decision explanations
"""
from typing import Dict, Any, Optional
from backend.tools_vendor import VendorAnalyticsTools
from backend.mongo_client import MongoDBClient
from backend.validators import (
    validate_vendor_id,
    validate_date_range,
    validate_limit,
    validate_last_n_weeks
)
from backend.utils import (
    SimpleMemory,
    format_vendor_summary,
    format_comparison,
    format_trend,
    format_top_performers,
    format_failed_submissions
)
from backend.prompts import AGENT_INSTRUCTION, mock_llm_parse
import os


class VendorAgent:
    """
    Vendor Performance Analysis Agent
    Enhanced with memory, validation, and decision explanations
    """
    
    def __init__(self, mock_mode: bool = False):
        """
        Initialize the agent
        
        Args:
            mock_mode: If True, use mock data instead of real MongoDB
        """
        self.mock_mode = mock_mode
        self.memory = SimpleMemory()
        self.instruction = AGENT_INSTRUCTION
        
        # Initialize MongoDB client
        self.mongo_client = MongoDBClient()
        
        # Initialize tools
        self.tools = VendorAnalyticsTools(self.mongo_client)
        
        # Connect to database if not in mock mode
        if not mock_mode:
            connected = self.mongo_client.connect()
            if not connected:
                print("⚠️  MongoDB connection failed. Switching to mock mode.")
                self.mock_mode = True
    
    def process_query(self, query: str, debug: bool = False) -> Dict[str, Any]:
        """
        Process a natural language query
        Enhanced with validation and decision tracking
        
        Args:
            query: Natural language query
            debug: If True, include detailed debug information
            
        Returns:
            {
                "query": original query,
                "tool": selected tool name,
                "params": extracted parameters,
                "result": tool execution result,
                "formatted": human-readable output,
                "decision": decision explanation,
                "memory_used": memory fields used
            }
        """
        # Parse query to determine tool and params
        parsed = mock_llm_parse(query)
        
        tool_name = parsed["tool"]
        params = parsed["params"]
        confidence = parsed.get("confidence", 0)
        matched_pattern = parsed.get("matched_pattern", "unknown")
        
        # Track decision
        decision = {
            "tool_selected": tool_name,
            "confidence": confidence,
            "matched_pattern": matched_pattern,
            "memory_fields_used": []
        }
        
        # Apply memory context and validate
        params, validation_result = self._apply_memory_and_validate(params, tool_name, decision)
        
        # If validation failed, return error
        if validation_result.get("status") == "error":
            return {
                "query": query,
                "tool": tool_name,
                "params": params,
                "result": validation_result,
                "formatted": f"❌ {validation_result.get('error')}",
                "decision": decision,
                "memory_used": decision["memory_fields_used"]
            }
        
        # Execute tool
        if self.mock_mode:
            result = self._execute_mock_tool(tool_name, params)
        else:
            result = self._execute_tool(tool_name, params)
        
        # Update memory
        self._update_memory(params)
        
        # Format output
        formatted = self._format_result(tool_name, result)
        
        response = {
            "query": query,
            "tool": tool_name,
            "params": params,
            "result": result,
            "formatted": formatted,
            "decision": decision,
            "memory_used": decision["memory_fields_used"]
        }
        
        if debug:
            response["debug"] = {
                "memory_state": self.memory.get_memory_summary(),
                "validation": validation_result,
                "mock_mode": self.mock_mode
            }
        
        return response
    
    def _apply_memory_and_validate(self, params: Dict, tool_name: str, decision: Dict) -> tuple:
        """
        Apply memory context and validate parameters
        Integrated validation with memory support
        
        Returns:
            (updated_params, validation_result)
        """
        validation_result = {"status": "success"}
        
        # Tool-specific validation
        if tool_name == "get_vendor_summary":
            # Validate vendorId
            vendor_validation = validate_vendor_id(params.get("vendorId"), self.memory)
            if not vendor_validation["valid"]:
                return params, vendor_validation
            
            if vendor_validation.get("from_memory"):
                decision["memory_fields_used"].append("vendorId")
            params["vendorId"] = vendor_validation["value"]
            
            # Validate dateRange
            range_validation = validate_date_range(params.get("dateRange"), self.memory)
            if not range_validation["valid"]:
                return params, range_validation
            
            if range_validation.get("from_memory"):
                decision["memory_fields_used"].append("dateRange")
            params["dateRange"] = range_validation["value"]
        
        elif tool_name == "compare_vendors":
            # Validate both vendors
            vendor_a_validation = validate_vendor_id(params.get("vendorA"), self.memory)
            if not vendor_a_validation["valid"]:
                return params, {"status": "error", "error": f"VendorA: {vendor_a_validation['error']}"}
            params["vendorA"] = vendor_a_validation["value"]
            
            vendor_b_validation = validate_vendor_id(params.get("vendorB"), None)  # Don't use memory for second vendor
            if not vendor_b_validation["valid"]:
                return params, {"status": "error", "error": f"VendorB: {vendor_b_validation['error']}"}
            params["vendorB"] = vendor_b_validation["value"]
            
            # Validate dateRange
            range_validation = validate_date_range(params.get("dateRange"), self.memory)
            if not range_validation["valid"]:
                return params, range_validation
            
            if range_validation.get("from_memory"):
                decision["memory_fields_used"].append("dateRange")
            params["dateRange"] = range_validation["value"]
        
        elif tool_name == "get_vendor_trend":
            # Validate vendorId
            vendor_validation = validate_vendor_id(params.get("vendorId"), self.memory)
            if not vendor_validation["valid"]:
                return params, vendor_validation
            
            if vendor_validation.get("from_memory"):
                decision["memory_fields_used"].append("vendorId")
            params["vendorId"] = vendor_validation["value"]
            
            # Validate lastNWeeks
            weeks_validation = validate_last_n_weeks(params.get("lastNWeeks"), self.memory)
            if not weeks_validation["valid"]:
                return params, weeks_validation
            
            if weeks_validation.get("from_memory"):
                decision["memory_fields_used"].append("lastNWeeks")
            params["lastNWeeks"] = weeks_validation["value"]
        
        elif tool_name == "vendor_top_performers":
            # Validate limit
            limit_validation = validate_limit(params.get("limit"), self.memory)
            if not limit_validation["valid"]:
                return params, limit_validation
            params["limit"] = limit_validation["value"]
            
            # Validate dateRange
            range_validation = validate_date_range(params.get("dateRange"), self.memory)
            if not range_validation["valid"]:
                return params, range_validation
            
            if range_validation.get("from_memory"):
                decision["memory_fields_used"].append("dateRange")
            params["dateRange"] = range_validation["value"]
        
        elif tool_name == "vendor_failed_submissions":
            # Validate dateRange
            range_validation = validate_date_range(params.get("dateRange"), self.memory)
            if not range_validation["valid"]:
                return params, range_validation
            
            if range_validation.get("from_memory"):
                decision["memory_fields_used"].append("dateRange")
            params["dateRange"] = range_validation["value"]
        
        return params, validation_result
    
    def _update_memory(self, params: Dict):
        """Store context in memory for future queries"""
        if "vendorId" in params and params["vendorId"]:
            self.memory.set_last_vendor_id(params["vendorId"])
        
        if "dateRange" in params and params["dateRange"]:
            self.memory.set_last_date_range(params["dateRange"])
        
        if "lastNWeeks" in params and params["lastNWeeks"]:
            self.memory.set_last_n_weeks(params["lastNWeeks"])
    
    def _execute_tool(self, tool_name: str, params: Dict) -> Dict[str, Any]:
        """Execute the selected tool with real MongoDB"""
        try:
            if tool_name == "get_vendor_summary":
                return self.tools.get_vendor_summary(
                    params.get("vendorId"),
                    params.get("dateRange")
                )
            
            elif tool_name == "compare_vendors":
                return self.tools.compare_vendors(
                    params.get("vendorA"),
                    params.get("vendorB"),
                    params.get("dateRange")
                )
            
            elif tool_name == "get_vendor_trend":
                return self.tools.get_vendor_trend(
                    params.get("vendorId"),
                    params.get("lastNWeeks")
                )
            
            elif tool_name == "vendor_top_performers":
                return self.tools.vendor_top_performers(
                    params.get("limit"),
                    params.get("dateRange")
                )
            
            elif tool_name == "vendor_failed_submissions":
                return self.tools.vendor_failed_submissions(
                    params.get("dateRange")
                )
            
            else:
                return {
                    "status": "error",
                    "error": f"Unknown tool: {tool_name}"
                }
        
        except Exception as e:
            return {
                "status": "error",
                "error": f"Tool execution failed: {str(e)}"
            }
    
    def _execute_mock_tool(self, tool_name: str, params: Dict) -> Dict[str, Any]:
        """Execute tool with mock data"""
        if tool_name == "get_vendor_summary":
            return {
                "status": "success",
                "data": {
                    "vendorId": params.get("vendorId", "VENDOR_1"),
                    "shared": 45,
                    "interviewed": 32,
                    "onboarded": 18,
                    "joinRatio": 0.40,
                    "avgTimeToOnboarding": 12.5
                }
            }
        
        elif tool_name == "compare_vendors":
            return {
                "status": "success",
                "data": {
                    "vendorA": {
                        "vendorId": params.get("vendorA", "VENDOR_1"),
                        "shared": 45,
                        "interviewed": 32,
                        "onboarded": 18,
                        "joinRatio": 0.40
                    },
                    "vendorB": {
                        "vendorId": params.get("vendorB", "VENDOR_2"),
                        "shared": 38,
                        "interviewed": 28,
                        "onboarded": 15,
                        "joinRatio": 0.39
                    }
                }
            }
        
        elif tool_name == "get_vendor_trend":
            return {
                "status": "success",
                "data": [
                    {"week": 45, "year": 2024, "shared": 12, "interviewed": 8, "onboarded": 4},
                    {"week": 46, "year": 2024, "shared": 15, "interviewed": 11, "onboarded": 6},
                    {"week": 47, "year": 2024, "shared": 18, "interviewed": 13, "onboarded": 8}
                ]
            }
        
        elif tool_name == "vendor_top_performers":
            limit = params.get("limit", 3)
            performers = [
                {"vendorId": "VENDOR_1", "onboarded": 18, "shared": 45, "joinRatio": 0.40},
                {"vendorId": "VENDOR_3", "onboarded": 16, "shared": 42, "joinRatio": 0.38},
                {"vendorId": "VENDOR_2", "onboarded": 15, "shared": 38, "joinRatio": 0.39},
                {"vendorId": "VENDOR_5", "onboarded": 12, "shared": 35, "joinRatio": 0.34},
                {"vendorId": "VENDOR_4", "onboarded": 10, "shared": 30, "joinRatio": 0.33}
            ]
            return {
                "status": "success",
                "data": performers[:limit]
            }
        
        elif tool_name == "vendor_failed_submissions":
            return {
                "status": "success",
                "data": {
                    "totalRejections": 23,
                    "topReasons": [
                        {"reason": "Skills mismatch", "count": 8},
                        {"reason": "Experience insufficient", "count": 6},
                        {"reason": "Location constraint", "count": 5},
                        {"reason": "Salary expectation too high", "count": 4}
                    ]
                }
            }
        
        else:
            return {
                "status": "error",
                "error": f"Unknown tool: {tool_name}"
            }
    
    def _format_result(self, tool_name: str, result: Dict) -> str:
        """Format result for human-readable output"""
        if result["status"] == "error":
            return f"❌ Error: {result['error']}"
        
        data = result.get("data")
        
        if tool_name == "get_vendor_summary":
            return format_vendor_summary(data)
        
        elif tool_name == "compare_vendors":
            return format_comparison(data)
        
        elif tool_name == "get_vendor_trend":
            return format_trend(data)
        
        elif tool_name == "vendor_top_performers":
            return format_top_performers(data)
        
        elif tool_name == "vendor_failed_submissions":
            return format_failed_submissions(data)
        
        else:
            return str(data)
    
    def get_decision_explanation(self, response: Dict) -> str:
        """
        Generate human-readable decision explanation
        Provides transparency into agent's decision-making process
        """
        decision = response.get("decision", {})
        memory_used = response.get("memory_used", [])
        
        lines = []
        lines.append(f"\n🧠 Decision Process:")
        lines.append(f"   • Tool Selected: {decision.get('tool_selected')}")
        lines.append(f"   • Confidence: {decision.get('confidence', 0):.0%}")
        lines.append(f"   • Pattern Matched: '{decision.get('matched_pattern')}'")
        
        if memory_used:
            lines.append(f"   • Memory Used: {', '.join(memory_used)}")
        else:
            lines.append(f"   • Memory Used: None (all params from query)")
        
        return "\n".join(lines)
    
    def close(self):
        """Clean up resources"""
        if self.mongo_client:
            self.mongo_client.disconnect()
