"""
CLI Runner for Vendor Analytics Agent
Enhanced with debug mode and better output formatting
"""
import argparse
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agent import VendorAgent


def main():
    parser = argparse.ArgumentParser(
        description="Vendor Performance Analytics Agent"
    )
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Natural language query"
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help="Run in mock mode (no MongoDB required)"
    )
    parser.add_argument(
        "--real",
        action="store_true",
        help="Force real database mode (opposite of --mock)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show detailed debug information including decision process"
    )
    parser.add_argument(
        "--json-only",
        action="store_true",
        help="Output only JSON result"
    )
    
    args = parser.parse_args()
    
    # Determine mode (default to mock unless --real is specified)
    mock_mode = not args.real if args.real else args.mock
    
    # Initialize agent
    agent = VendorAgent(mock_mode=mock_mode)
    
    if not args.json_only:
        print("\n" + "="*60)
        print("🤖 VENDOR ANALYTICS AGENT")
        print("="*60)
        if mock_mode:
            print("⚡ Mode: MOCK (no database required)")
        else:
            print("💾 Mode: REAL DATABASE")
        print(f"\n📝 Query: {args.query}")
        print("-"*60)
    
    # Process query
    response = agent.process_query(args.query, debug=args.debug)
    
    if args.json_only:
        # Output only JSON
        print(json.dumps(response, indent=2))
    else:
        # Show decision explanation
        decision_text = agent.get_decision_explanation(response)
        print(decision_text)
        
        # Show parameters
        print(f"\n📊 Parameters:")
        for key, value in response['params'].items():
            if isinstance(value, dict):
                print(f"   • {key}: {json.dumps(value)}")
            else:
                print(f"   • {key}: {value}")
        
        # Show formatted result
        print(f"\n{response['formatted']}")
        
        # Debug mode: show additional info
        if args.debug:
            print("\n" + "="*60)
            print("🔍 DEBUG INFORMATION")
            print("="*60)
            print("\n📄 Raw JSON Result:")
            print(json.dumps(response['result'], indent=2))
            
            if 'debug' in response:
                print("\n🧠 Memory State:")
                print(json.dumps(response['debug']['memory_state'], indent=2))
                print(f"\n⚙️  Mock Mode: {response['debug']['mock_mode']}")
        
        print("\n" + "="*60 + "\n")
    
    # Cleanup
    agent.close()


if __name__ == "__main__":
    main()
