# 📊 Vendor Performance Analytics Agent

**Google AI Intensive 5-Day Capstone Project**

An intelligent agent that analyzes vendor performance data using natural language queries. Built with Google's Agent Development Kit (ADK) pattern, MongoDB aggregations, and conversational memory.

---

## 🎯 Project Overview

### What This Agent Does

The **Vendor Performance Analytics Agent** helps recruitment teams analyze vendor performance through natural language conversations. Instead of writing complex database queries or navigating dashboards, users can simply ask questions like:

- *"Show me the top 5 vendors this year"*
- *"Compare VENDOR_1 and VENDOR_2"*
- *"Why are candidates getting rejected?"*

The agent understands the intent, selects the appropriate analytics tool, validates inputs, executes predefined MongoDB aggregations, and returns dashboard-quality results.

### Why Predefined Tools?

For this capstone project, we use **predefined MongoDB aggregation pipelines** rather than LLM-generated queries. This approach:

- ✅ **Ensures reliability** - No risk of incorrect SQL/MongoDB generation
- ✅ **Maintains security** - No injection vulnerabilities
- ✅ **Provides consistency** - Same query always returns same structure
- ✅ **Demonstrates ADK concepts** - Focus on agent orchestration, not query generation
- ✅ **Production-ready** - Suitable for real-world deployment

### How ADK is Used

This project demonstrates the **Google Agent Development Kit (ADK)** pattern through:

1. **Tool-Calling Architecture**
   - Agent selects from 5 predefined analytics tools
   - Each tool has specific parameters and return formats
   - Tools are executed based on natural language intent

2. **Short-Term Memory**
   - Agent remembers context from previous queries
   - Enables follow-up questions like "now show me the trend"
   - Stores vendorId, dateRange, and lastNWeeks

3. **Multi-Step Planning**
   - Query parsing → Parameter extraction → Validation → Tool execution → Formatting
   - Memory integration at validation step
   - Decision transparency showing reasoning

4. **Conversational Interface**
   - Natural language input
   - Context-aware responses
   - Human-friendly output formatting

### ADK Concepts Demonstrated

| Concept | Implementation |
|---------|----------------|
| **Tool Selection** | Pattern matching with 40+ NL patterns, confidence scoring |
| **Parameter Extraction** | Regex-based extraction from natural language |
| **Validation** | Memory-aware validation with helpful error messages |
| **Memory Management** | Short-term context storage for follow-up queries |
| **Output Formatting** | Dashboard-quality results with visual indicators |
| **Error Handling** | Structured errors with actionable suggestions |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER QUERY                          │
│              "Show top 5 vendors in 2024"                   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    VENDOR AGENT                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  1. NL Parser (prompts.py)                           │  │
│  │     • Pattern matching (40+ patterns)                │  │
│  │     • Confidence scoring                             │  │
│  │     • Tool selection                                 │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  2. Memory System (utils.py)                         │  │
│  │     • Check for stored context                       │  │
│  │     • Auto-fill missing parameters                   │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  3. Validator (validators.py)                        │  │
│  │     • Validate all parameters                        │  │
│  │     • Return helpful errors if invalid              │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  4. Tool Executor (tools_vendor.py)                  │  │
│  │     • Execute predefined MongoDB aggregation         │  │
│  │     • Return structured results                      │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  5. Formatter (utils.py)                             │  │
│  │     • Dashboard-quality output                       │  │
│  │     • Visual indicators (🟢🟡🔴)                      │  │
│  └──────────────────────┬───────────────────────────────┘  │
└─────────────────────────┼───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    FORMATTED RESULT                         │
│         🏆 TOP PERFORMING VENDORS LEADERBOARD               │
│  🥇 #1 | VENDOR_1 | 18 onboarded | 40.0% join ratio        │
│  🥈 #2 | VENDOR_3 | 16 onboarded | 38.0% join ratio        │
│  🥉 #3 | VENDOR_2 | 15 onboarded | 39.0% join ratio        │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Folder Structure

```
ai-vendor-agent/
├── backend/
│   ├── __init__.py              # Package marker
│   ├── agent.py                 # Main VendorAgent class (ADK orchestration)
│   ├── prompts.py               # NL patterns, tool selection logic
│   ├── validators.py            # Input validation with memory support
│   ├── utils.py                 # Memory system & output formatters
│   ├── tools_vendor.py          # 5 predefined analytics tools
│   ├── mongo_client.py          # MongoDB connection & safe execution
│   └── runner.py                # CLI interface
│
├── data/
│   ├── sample_data.json         # 50 anonymized sample documents
│   └── import_data.sh           # MongoDB import script
│
├── notebooks/
│   └── kaggle_demo.ipynb        # Interactive Jupyter demo
│
├── examples/
│   └── queries.md               # Example queries with expected outputs
│
├── .env.example                 # Environment configuration template
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── IMPLEMENTATION_SUMMARY.md    # Technical feature overview
├── STATUS.md                    # Current project status
└── COMPLETION_REPORT.md         # Final delivery report
```

---

## 🚀 How to Run Locally

### Prerequisites

- Python 3.10 or higher
- MongoDB (optional - only needed for real database mode)
- Terminal/Command Line

### Step 1: Install Dependencies

```bash
# Clone or navigate to project directory
cd ai-vendor-agent

# Install Python packages
pip3 install -r requirements.txt
```

### Step 2: Run in Mock Mode (No Database Required)

The agent works 100% in mock mode without any database setup:

```bash
# Basic query
python3 backend/runner.py --mock --query "top vendors last month"

# Vendor summary
python3 backend/runner.py --mock --query "show vendor summary for VENDOR_1 in 2024"

# Comparison
python3 backend/runner.py --mock --query "compare VENDOR_1 and VENDOR_2"

# With debug information
python3 backend/runner.py --mock --debug --query "top 5 vendors in 2024"
```

### Step 3: (Optional) Run with Real Database

If you want to use real MongoDB data:

```bash
# 1. Start MongoDB
brew services start mongodb-community  # macOS
# OR
sudo systemctl start mongod            # Linux

# 2. Import sample data
cd data
bash import_data.sh

# 3. Run queries with real database
cd ..
python3 backend/runner.py --real --query "top 5 vendors in 2024"
```

### Step 4: (Optional) Try Jupyter Notebook

```bash
# Install Jupyter if not already installed
pip3 install jupyter

# Start Jupyter
jupyter notebook

# Open: notebooks/kaggle_demo.ipynb
```

---

## 🔑 How to Run with Google Gemini API (Optional)

**Note**: The current implementation uses mock mode for the capstone. Real Gemini integration is planned for future versions.

If you want to prepare for future Gemini integration:

1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Add your API key to `.env`:
```
GOOGLE_API_KEY=your_api_key_here
MONGODB_URI=mongodb://localhost:27017/
MONGODB_DB=vendor_analytics
```

4. Future versions will use this for enhanced NL understanding

---

## 💬 Example Queries

### 1. Vendor Summary
**Query**: `"show vendor summary for VENDOR_1 in 2024"`

**Output**:
```
============================================================
📊 VENDOR PERFORMANCE DASHBOARD - VENDOR_1
============================================================

📈 Candidate Flow:
   • Profiles Shared:       45
   • Interviews Conducted:   32
   • Successfully Onboarded:   18

🎯 Key Metrics:
   • Join Ratio:           40.0%  🟡
   • Avg Time to Hire:      12.5 days

💡 Assessment: Good performance 👍
============================================================
```

### 2. Top Performers
**Query**: `"top 5 vendors in 2024"`

**Output**:
```
============================================================
🏆 TOP PERFORMING VENDORS LEADERBOARD
============================================================

Rank |       Vendor | Onboarded | Shared |  Join % | Rating
------------------------------------------------------------
🥇 # 1 |     VENDOR_1 |        18 |     45 |  40.0% | ████░░░░░░
🥈 # 2 |     VENDOR_3 |        16 |     42 |  38.0% | ███░░░░░░░
🥉 # 3 |     VENDOR_2 |        15 |     38 |  39.0% | ███░░░░░░░
============================================================
```

### 3. Vendor Comparison
**Query**: `"compare VENDOR_1 and VENDOR_2 in 2024"`

**Output**:
```
============================================================
🔄 VENDOR COMPARISON DASHBOARD
============================================================

          VENDOR_1           vs           VENDOR_2          
------------------------------------------------------------
     Profiles Shared:     45  🏆  |      38    
          Interviews:     32  🏆  |      28    
           Onboarded:     18      |      15  🏆
          Join Ratio:  40.0%      |   39.5%  

------------------------------------------------------------
💡 Winner: VENDOR_1 with 40.0% join ratio
============================================================
```

### 4. Performance Trend
**Query**: `"show trend for VENDOR_1 last 8 weeks"`

**Output**:
```
============================================================
📈 WEEKLY PERFORMANCE TREND
============================================================

    Week |  Shared | Interviewed | Onboarded | Trend
------------------------------------------------------------
W45/2024 |      12 |           8 |         4 | —
W46/2024 |      15 |          11 |         6 | 📈 Up
W47/2024 |      18 |          13 |         8 | 📈 Up
------------------------------------------------------------

📊 Period Summary:
   • Total Shared: 45
   • Total Onboarded: 18
   • Average Join Ratio: 40.0%
============================================================
```

### 5. Rejection Analysis
**Query**: `"why are candidates rejected in 2024"`

**Output**:
```
============================================================
❌ REJECTION ANALYSIS DASHBOARD
============================================================

📊 Total Rejections: 23

🔍 Top Rejection Reasons:
------------------------------------------------------------
1. Skills mismatch                  8 ( 34.8%) ███░░░░░░░
2. Experience insufficient          6 ( 26.1%) ██░░░░░░░░
3. Location constraint              5 ( 21.7%) ██░░░░░░░░
4. Salary expectation too high      4 ( 17.4%) █░░░░░░░░░

💡 Actionable Insights:
   • Primary issue: Skills mismatch
   • Focus on improving candidate screening for this area
============================================================
```

---

## 🎓 Capstone Submission Description

### Project Summary

**Vendor Performance Analytics Agent** is an intelligent system that enables recruitment teams to analyze vendor performance through natural language conversations. Built for the Google AI Intensive 5-Day Capstone, this project demonstrates practical application of Agent Development Kit (ADK) concepts.

**Problem Solved**: Recruitment teams need quick insights into vendor performance but lack technical skills for database queries. This agent bridges that gap by accepting natural language questions and returning actionable, dashboard-quality analytics.

**Technology Stack**:
- **Google ADK Pattern**: Tool-calling, memory management, multi-step planning
- **MongoDB**: Predefined aggregation pipelines for 5 analytics tools
- **Python**: Agent orchestration, validation, formatting
- **Short-Term Memory**: Context retention for conversational follow-ups

**Key Features**:
- 🎯 5 predefined analytics tools (summary, comparison, trend, top performers, rejections)
- 🧠 Memory system for follow-up queries
- ✅ Smart validation with helpful error messages
- 📊 Dashboard-quality output with visual indicators
- ⚡ 100% functional mock mode (no database/API required)

**ADK Concepts Demonstrated**:
1. **Tool-Calling**: Pattern matching with 40+ NL patterns, confidence scoring, dynamic tool selection
2. **Short-Term Memory**: Context storage (vendorId, dateRange, lastNWeeks) for conversational flow
3. **Multi-Step Planning**: Query parsing → Memory check → Validation → Execution → Formatting
4. **Error Handling**: Structured errors with actionable suggestions
5. **Decision Transparency**: Shows tool selection reasoning and confidence

This project showcases how ADK principles enable building production-ready agents that are reliable, maintainable, and user-friendly—perfect for real-world recruitment analytics.

---

## 🛠️ Technical Details

### 5 Analytics Tools

| Tool | Purpose | Parameters | MongoDB Aggregation |
|------|---------|------------|---------------------|
| `get_vendor_summary` | Performance metrics for one vendor | vendorId, dateRange | Group by status, calculate ratios |
| `compare_vendors` | Side-by-side comparison | vendorA, vendorB, dateRange | Parallel aggregations, comparison |
| `get_vendor_trend` | Weekly performance over time | vendorId, lastNWeeks | Group by week, time-series data |
| `vendor_top_performers` | Leaderboard of best vendors | limit, dateRange | Sort by join ratio, limit results |
| `vendor_failed_submissions` | Rejection reason analysis | dateRange | Group by rejection reason, count |

### Memory System

The agent maintains short-term memory to enable conversational interactions:

```python
# First query establishes context
"show vendor summary for VENDOR_1 in 2024"
# Memory stores: vendorId=VENDOR_1, dateRange={...}

# Follow-up uses memory
"now show me the trend for last 8 weeks"
# Agent automatically uses VENDOR_1 from memory!
```

### Validation

All inputs are validated before execution:
- **VendorId**: Format (VENDOR_X), memory fallback
- **DateRange**: Up to 1 year, logical checks
- **Limit**: Range 1-100
- **LastNWeeks**: Range 1-52

Errors return helpful messages:
```
❌ VendorId is required. Please specify a vendor or run a query with a vendor first.
```

---

## 🧪 Testing

### Mock Mode Tests
```bash
# Test all 5 tools
python3 backend/runner.py --mock --query "show vendor summary for VENDOR_1 in 2024"
python3 backend/runner.py --mock --query "compare VENDOR_1 and VENDOR_2"
python3 backend/runner.py --mock --query "show trend for VENDOR_1 last 8 weeks"
python3 backend/runner.py --mock --query "top 5 vendors in 2024"
python3 backend/runner.py --mock --query "why are candidates rejected"
```

### Real Database Tests
```bash
# Import data first
cd data && bash import_data.sh && cd ..

# Test with real data
python3 backend/runner.py --real --query "top 5 vendors in 2024"
python3 backend/runner.py --real --query "compare VENDOR_1 and VENDOR_3 in 2024"
```

---

## 📚 Additional Resources

- **IMPLEMENTATION_SUMMARY.md** - Detailed feature documentation
- **STATUS.md** - Current project status and testing results
- **COMPLETION_REPORT.md** - Final delivery report
- **examples/queries.md** - 10+ example queries with outputs
- **notebooks/kaggle_demo.ipynb** - Interactive demonstration

---

## 🚀 Future Enhancements

Planned improvements beyond the capstone:

1. **Real Gemini Integration** - Replace mock parser with actual LLM
2. **Client Agent** - Handle client-side queries
3. **Ops Agent** - Operational analytics
4. **Dynamic Aggregations** - LLM-generated MongoDB queries
5. **Web UI** - Interactive dashboard
6. **Export Capabilities** - CSV, PDF reports
7. **Real-Time Updates** - Live data streaming
8. **Multi-User Support** - Team collaboration

---

## 👤 Author

**Priyanshu**  
Google AI Intensive 5-Day Capstone Project  
November 2025

---

## 📝 License

This project is created for educational purposes as part of the Google AI Intensive program.

---

## 🙏 Acknowledgments

- **Google AI Intensive Program** - For the comprehensive 5-day training
- **Google ADK Team** - For the agent development framework concepts
- **MongoDB** - For the powerful aggregation pipeline capabilities

---

**Ready to analyze vendor performance with natural language? Start with:**

```bash
python3 backend/runner.py --mock --query "top vendors last month"
```

🎉 **Happy Analyzing!**
