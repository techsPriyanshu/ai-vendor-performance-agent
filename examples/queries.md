# 📝 Example Queries for Vendor Analytics Agent

This file contains 15+ example queries demonstrating all features of the Vendor Analytics Agent.

---

## 🎯 Quick Start

All examples use mock mode (no database required). Simply copy and paste into your terminal!

---

## 1️⃣ Vendor Summary Queries

Get performance metrics for a specific vendor.

### Example 1.1: Basic Summary
```bash
python3 backend/runner.py --mock --query "show vendor summary for VENDOR_1 in 2024"
```

**Expected Output**: Dashboard showing shared profiles, interviews, onboarded candidates, join ratio, and average time to hire.

### Example 1.2: Alternative Phrasing
```bash
python3 backend/runner.py --mock --query "vendor performance for VENDOR_2"
```

### Example 1.3: Casual Phrasing
```bash
python3 backend/runner.py --mock --query "how is VENDOR_3 doing"
```

### Example 1.4: Formal Phrasing
```bash
python3 backend/runner.py --mock --query "get summary for vendor VENDOR_4"
```

---

## 2️⃣ Top Performers Queries

Find the best performing vendors based on join ratio.

### Example 2.1: Top 5 Vendors
```bash
python3 backend/runner.py --mock --query "top 5 vendors in 2024"
```

**Expected Output**: Leaderboard with medals (🥇🥈🥉), onboarded count, shared count, join ratio, and visual rating bars.

### Example 2.2: Top 3 Vendors
```bash
python3 backend/runner.py --mock --query "top 3 vendors"
```

### Example 2.3: Best Performers
```bash
python3 backend/runner.py --mock --query "best performing vendors"
```

### Example 2.4: Top Vendors Last Month
```bash
python3 backend/runner.py --mock --query "top vendors last month"
```

### Example 2.5: Leading Vendors
```bash
python3 backend/runner.py --mock --query "who are the leading vendors"
```

---

## 3️⃣ Vendor Comparison Queries

Compare two vendors side-by-side.

### Example 3.1: Basic Comparison
```bash
python3 backend/runner.py --mock --query "compare VENDOR_1 and VENDOR_2 in 2024"
```

**Expected Output**: Side-by-side metrics with winner indication (🏆) and final verdict.

### Example 3.2: VS Format
```bash
python3 backend/runner.py --mock --query "VENDOR_1 vs VENDOR_3"
```

### Example 3.3: Versus Format
```bash
python3 backend/runner.py --mock --query "VENDOR_2 versus VENDOR_4"
```

### Example 3.4: Which is Better
```bash
python3 backend/runner.py --mock --query "which is better VENDOR_1 or VENDOR_2"
```

### Example 3.5: Difference Between
```bash
python3 backend/runner.py --mock --query "difference between VENDOR_3 and VENDOR_5"
```

---

## 4️⃣ Performance Trend Queries

Analyze weekly performance trends over time.

### Example 4.1: 8-Week Trend
```bash
python3 backend/runner.py --mock --query "show trend for VENDOR_1 last 8 weeks"
```

**Expected Output**: Weekly breakdown with trend indicators (📈📉➡️) and period summary.

### Example 4.2: Vendor Trend
```bash
python3 backend/runner.py --mock --query "vendor trend for VENDOR_2"
```

### Example 4.3: Weekly Performance
```bash
python3 backend/runner.py --mock --query "weekly performance for VENDOR_3"
```

### Example 4.4: Historical Performance
```bash
python3 backend/runner.py --mock --query "historical performance for VENDOR_1"
```

### Example 4.5: Performance Over Time
```bash
python3 backend/runner.py --mock --query "performance trend for VENDOR_2 over last 6 weeks"
```

---

## 5️⃣ Rejection Analysis Queries

Understand why candidates are getting rejected.

### Example 5.1: Basic Rejection Query
```bash
python3 backend/runner.py --mock --query "why are candidates rejected in 2024"
```

**Expected Output**: Total rejections, top reasons with percentages and visual bars, actionable insights.

### Example 5.2: Failed Submissions
```bash
python3 backend/runner.py --mock --query "failed submissions"
```

### Example 5.3: Rejection Reasons
```bash
python3 backend/runner.py --mock --query "rejection reasons"
```

### Example 5.4: Why Rejected
```bash
python3 backend/runner.py --mock --query "why rejected"
```

### Example 5.5: Failure Analysis
```bash
python3 backend/runner.py --mock --query "what went wrong with candidates"
```

---

## 6️⃣ Follow-Up Queries (Memory Demonstration)

The agent remembers context from previous queries!

### Example 6.1: Summary Then Trend
```bash
# First query - establishes context
python3 backend/runner.py --mock --query "show vendor summary for VENDOR_1 in 2024"

# Follow-up - uses VENDOR_1 from memory
python3 backend/runner.py --mock --query "now show me trend for last 8 weeks"
```

**Note**: Memory only works within the same Python session. For CLI, use the programmatic API:

```python
from backend.agent import VendorAgent

agent = VendorAgent(mock_mode=True)

# First query
response1 = agent.process_query("show vendor summary for VENDOR_1 in 2024")
print(response1['formatted'])

# Follow-up uses memory
response2 = agent.process_query("now show trend")
print(response2['formatted'])
print(f"Memory used: {response2['memory_used']}")  # Shows ['vendorId']

agent.close()
```

### Example 6.2: Comparison Then Individual Summary
```python
from backend.agent import VendorAgent

agent = VendorAgent(mock_mode=True)

# Compare two vendors
agent.process_query("compare VENDOR_1 and VENDOR_2 in 2024")

# Follow-up about first vendor
response = agent.process_query("show me more details")
# Agent remembers VENDOR_1 from comparison

agent.close()
```

---

## 7️⃣ Debug Mode Queries

See detailed information about agent decisions.

### Example 7.1: Debug Mode
```bash
python3 backend/runner.py --mock --debug --query "top 5 vendors in 2024"
```

**Output Includes**:
- Decision process (tool selected, confidence, pattern matched)
- Parameters used
- Formatted result
- Raw JSON result
- Memory state
- Mock mode indicator

### Example 7.2: Debug with Comparison
```bash
python3 backend/runner.py --mock --debug --query "compare VENDOR_1 and VENDOR_2"
```

---

## 8️⃣ Real Database Queries

Use these after importing sample data.

### Setup Real Database
```bash
# Start MongoDB
brew services start mongodb-community  # macOS
# OR
sudo systemctl start mongod            # Linux

# Import data
cd data
bash import_data.sh
cd ..
```

### Example 8.1: Real Data - Top Performers
```bash
python3 backend/runner.py --real --query "top 5 vendors in 2024"
```

### Example 8.2: Real Data - Comparison
```bash
python3 backend/runner.py --real --query "compare VENDOR_1 and VENDOR_3 in 2024"
```

### Example 8.3: Real Data - Rejection Analysis
```bash
python3 backend/runner.py --real --query "why are candidates rejected in 2024"
```

---

## 9️⃣ JSON Output Queries

Get raw JSON for programmatic use.

### Example 9.1: JSON Only
```bash
python3 backend/runner.py --mock --json-only --query "top 3 vendors in 2024"
```

**Output**: Complete JSON response with query, tool, params, result, formatted output, decision, and memory_used.

---

## 🔟 Error Handling Examples

See how the agent handles invalid inputs.

### Example 10.1: Missing VendorId
```bash
python3 backend/runner.py --mock --query "show trend"
```

**Expected**: Helpful error message suggesting to specify a vendor or run a query with a vendor first.

### Example 10.2: Invalid VendorId Format
```bash
python3 backend/runner.py --mock --query "show summary for ABC123"
```

**Expected**: Error explaining expected format (VENDOR_X).

### Example 10.3: Invalid Date Range
```bash
python3 backend/runner.py --mock --query "show vendors from 2020 to 2025"
```

**Expected**: Error explaining date range limit (up to 1 year).

---

## 📊 Complete Testing Workflow

Test all features in sequence:

```bash
# 1. Vendor Summary
python3 backend/runner.py --mock --query "show vendor summary for VENDOR_1 in 2024"

# 2. Top Performers
python3 backend/runner.py --mock --query "top 5 vendors in 2024"

# 3. Vendor Comparison
python3 backend/runner.py --mock --query "compare VENDOR_1 and VENDOR_2 in 2024"

# 4. Performance Trend
python3 backend/runner.py --mock --query "show trend for VENDOR_1 last 8 weeks"

# 5. Rejection Analysis
python3 backend/runner.py --mock --query "why are candidates rejected in 2024"

# 6. Debug Mode
python3 backend/runner.py --mock --debug --query "top 3 vendors in 2024"
```

---

## 🎯 Query Pattern Reference

The agent recognizes 40+ patterns. Here are the main categories:

### Vendor Summary Patterns
- "show vendor summary"
- "vendor summary for"
- "get summary for vendor"
- "vendor performance for"
- "how is vendor"
- "vendor stats"
- "vendor metrics"

### Comparison Patterns
- "compare vendor"
- "vendor comparison"
- "vs vendor"
- "versus vendor"
- "difference between"
- "which is better"

### Trend Patterns
- "vendor trend"
- "trend for vendor"
- "weekly trend"
- "show me trend"
- "performance trend"
- "historical performance"

### Top Performers Patterns
- "top vendor"
- "top performing vendor"
- "best vendor"
- "top 3 vendor"
- "top 5 vendor"
- "highest performing"
- "leading vendor"

### Rejection Patterns
- "failed submission"
- "rejection"
- "why are candidates rejected"
- "rejection reason"
- "failure reason"
- "what went wrong"

---

## 💡 Tips for Best Results

1. **Be Specific**: Include vendor IDs and date ranges when possible
2. **Use Memory**: Run related queries in the same session for context
3. **Try Variations**: The agent understands many phrasings
4. **Check Debug**: Use `--debug` to understand agent decisions
5. **Test Mock First**: Verify queries work in mock mode before using real data

---

## 🚀 Next Steps

- Try the Jupyter notebook: `jupyter notebook notebooks/kaggle_demo.ipynb`
- Read the full README: `README.md`
- Check implementation details: `IMPLEMENTATION_SUMMARY.md`

---

**Happy Querying! 🎉**
