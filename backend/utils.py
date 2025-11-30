"""
Utility functions including simple memory store
Enhanced memory system with tracking and retrieval
"""
from typing import Dict, Any, Optional


class SimpleMemory:
    """
    Simple in-memory store for context retention
    Enhanced with memory management and tracking
    """
    
    def __init__(self):
        self.store = {}
        self.history = []  # Track memory updates
    
    def set_memory(self, key: str, value: Any):
        """
        Store a value with history tracking
        
        Args:
            key: Memory key
            value: Value to store
        """
        self.store[key] = value
        self.history.append({"key": key, "value": value})
        
        # Keep history limited to last 10 entries
        if len(self.history) > 10:
            self.history = self.history[-10:]
    
    def get_memory(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a value from memory
        
        Args:
            key: Memory key
            default: Default value if key not found
            
        Returns:
            Stored value or default
        """
        return self.store.get(key, default)
    
    def clear_memory(self):
        """Clear all stored values and history"""
        self.store = {}
        self.history = []
    
    # Legacy methods for backward compatibility
    def set(self, key: str, value: Any):
        """Store a value (legacy method)"""
        self.set_memory(key, value)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value (legacy method)"""
        return self.get_memory(key, default)
    
    def clear(self):
        """Clear all stored values (legacy method)"""
        self.clear_memory()
    
    # Specific memory accessors
    def get_last_vendor_id(self) -> Optional[str]:
        """Get last used vendor ID"""
        return self.get_memory("vendorId")
    
    def set_last_vendor_id(self, vendor_id: str):
        """Store last used vendor ID"""
        self.set_memory("vendorId", vendor_id)
    
    def get_last_date_range(self) -> Optional[Dict]:
        """Get last used date range"""
        return self.get_memory("dateRange")
    
    def set_last_date_range(self, date_range: Dict):
        """Store last used date range"""
        self.set_memory("dateRange", date_range)
    
    def get_last_n_weeks(self) -> Optional[int]:
        """Get last used lastNWeeks value"""
        return self.get_memory("lastNWeeks")
    
    def set_last_n_weeks(self, weeks: int):
        """Store last used lastNWeeks value"""
        self.set_memory("lastNWeeks", weeks)
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """
        Get a summary of current memory state
        
        Returns:
            Dictionary with current memory values
        """
        return {
            "vendorId": self.get_last_vendor_id(),
            "dateRange": self.get_last_date_range(),
            "lastNWeeks": self.get_last_n_weeks(),
            "history_count": len(self.history)
        }


def format_vendor_summary(data: Dict) -> str:
    """
    Format vendor summary for dashboard-quality output
    Enhanced with visual formatting and performance indicators
    """
    if not data:
        return "📊 No data available for this vendor."
    
    vendor_id = data.get('vendorId', 'Unknown')
    shared = data.get('shared', 0)
    interviewed = data.get('interviewed', 0)
    onboarded = data.get('onboarded', 0)
    join_ratio = data.get('joinRatio', 0)
    avg_time = data.get('avgTimeToOnboarding', 0)
    
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"📊 VENDOR PERFORMANCE DASHBOARD - {vendor_id}")
    output.append(f"{'='*60}")
    output.append(f"\n📈 Candidate Flow:")
    output.append(f"   • Profiles Shared:     {shared:>4}")
    output.append(f"   • Interviews Conducted: {interviewed:>4}")
    output.append(f"   • Successfully Onboarded: {onboarded:>4}")
    output.append(f"\n🎯 Key Metrics:")
    output.append(f"   • Join Ratio:          {join_ratio:>6.1%}  {'🟢' if join_ratio >= 0.5 else '🟡' if join_ratio >= 0.3 else '🔴'}")
    output.append(f"   • Avg Time to Hire:    {avg_time:>6.1f} days")
    
    # Add performance assessment
    if join_ratio >= 0.6:
        assessment = "Excellent performance! 🌟"
    elif join_ratio >= 0.4:
        assessment = "Good performance 👍"
    elif join_ratio >= 0.2:
        assessment = "Moderate performance ⚠️"
    else:
        assessment = "Needs improvement 📉"
    
    output.append(f"\n💡 Assessment: {assessment}")
    output.append(f"{'='*60}")
    
    return "\n".join(output)


def format_comparison(data: Dict) -> str:
    """
    Format vendor comparison for dashboard-quality output
    Enhanced with side-by-side comparison and winner indication
    """
    if not data:
        return "🔄 No comparison data available."
    
    vendor_a = data.get("vendorA", {})
    vendor_b = data.get("vendorB", {})
    
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"🔄 VENDOR COMPARISON DASHBOARD")
    output.append(f"{'='*60}")
    output.append(f"\n{vendor_a.get('vendorId', 'Vendor A'):^28} vs {vendor_b.get('vendorId', 'Vendor B'):^28}")
    output.append(f"{'-'*60}")
    
    # Metrics comparison
    metrics = [
        ("Profiles Shared", "shared"),
        ("Interviews", "interviewed"),
        ("Onboarded", "onboarded"),
        ("Join Ratio", "joinRatio")
    ]
    
    for label, key in metrics:
        val_a = vendor_a.get(key, 0)
        val_b = vendor_b.get(key, 0)
        
        if key == "joinRatio":
            output.append(f"{label:>20}: {val_a:>6.1%}  {'🏆' if val_a > val_b else '  '}  |  {val_b:>6.1%}  {'🏆' if val_b > val_a else '  '}")
        else:
            output.append(f"{label:>20}: {val_a:>6}  {'🏆' if val_a > val_b else '  '}  |  {val_b:>6}  {'🏆' if val_b > val_a else '  '}")
    
    # Determine winner
    ratio_a = vendor_a.get('joinRatio', 0)
    ratio_b = vendor_b.get('joinRatio', 0)
    
    output.append(f"\n{'-'*60}")
    if ratio_a > ratio_b:
        output.append(f"💡 Winner: {vendor_a.get('vendorId')} with {ratio_a:.1%} join ratio")
    elif ratio_b > ratio_a:
        output.append(f"💡 Winner: {vendor_b.get('vendorId')} with {ratio_b:.1%} join ratio")
    else:
        output.append(f"💡 Both vendors have equal performance")
    
    output.append(f"{'='*60}")
    
    return "\n".join(output)


def format_trend(data: list) -> str:
    """
    Format weekly trend data for dashboard-quality output
    Enhanced with visual trend indicators and summary
    """
    if not data:
        return "📈 No trend data available for the specified period."
    
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"📈 WEEKLY PERFORMANCE TREND")
    output.append(f"{'='*60}")
    output.append(f"\n{'Week':>8} | {'Shared':>7} | {'Interviewed':>11} | {'Onboarded':>9} | Trend")
    output.append(f"{'-'*60}")
    
    prev_onboarded = None
    for week in data:
        week_num = week.get('week', '?')
        year = week.get('year', '?')
        shared = week.get('shared', 0)
        interviewed = week.get('interviewed', 0)
        onboarded = week.get('onboarded', 0)
        
        # Trend indicator
        if prev_onboarded is not None:
            if onboarded > prev_onboarded:
                trend = "📈 Up"
            elif onboarded < prev_onboarded:
                trend = "📉 Down"
            else:
                trend = "➡️  Flat"
        else:
            trend = "—"
        
        output.append(f"W{week_num:>2}/{year} | {shared:>7} | {interviewed:>11} | {onboarded:>9} | {trend}")
        prev_onboarded = onboarded
    
    # Summary
    total_shared = sum(w.get('shared', 0) for w in data)
    total_onboarded = sum(w.get('onboarded', 0) for w in data)
    avg_ratio = total_onboarded / total_shared if total_shared > 0 else 0
    
    output.append(f"{'-'*60}")
    output.append(f"\n📊 Period Summary:")
    output.append(f"   • Total Shared: {total_shared}")
    output.append(f"   • Total Onboarded: {total_onboarded}")
    output.append(f"   • Average Join Ratio: {avg_ratio:.1%}")
    output.append(f"{'='*60}")
    
    return "\n".join(output)


def format_top_performers(data: list) -> str:
    """
    Format top performers list for dashboard-quality output
    Enhanced with ranking medals and performance bars
    """
    if not data:
        return "🏆 No performers data available."
    
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"🏆 TOP PERFORMING VENDORS LEADERBOARD")
    output.append(f"{'='*60}")
    output.append(f"\n{'Rank':>4} | {'Vendor':>12} | {'Onboarded':>9} | {'Shared':>6} | {'Join %':>7} | Rating")
    output.append(f"{'-'*60}")
    
    medals = ["🥇", "🥈", "🥉"]
    
    for i, vendor in enumerate(data, 1):
        vendor_id = vendor.get('vendorId', 'Unknown')
        onboarded = vendor.get('onboarded', 0)
        shared = vendor.get('shared', 0)
        join_ratio = vendor.get('joinRatio', 0)
        
        # Medal for top 3
        medal = medals[i-1] if i <= 3 else "  "
        
        # Performance bar
        bar_length = int(join_ratio * 10)
        bar = "█" * bar_length + "░" * (10 - bar_length)
        
        output.append(f"{medal} #{i:>2} | {vendor_id:>12} | {onboarded:>9} | {shared:>6} | {join_ratio:>6.1%} | {bar}")
    
    output.append(f"{'='*60}")
    
    return "\n".join(output)


def format_failed_submissions(data: Dict) -> str:
    """
    Format failed submissions report for dashboard-quality output
    Enhanced with visual breakdown and actionable insights
    """
    if not data:
        return "❌ No failure data available."
    
    total = data.get('totalRejections', 0)
    top_reasons = data.get('topReasons', [])
    
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"❌ REJECTION ANALYSIS DASHBOARD")
    output.append(f"{'='*60}")
    output.append(f"\n📊 Total Rejections: {total}")
    
    if top_reasons:
        output.append(f"\n🔍 Top Rejection Reasons:")
        output.append(f"{'-'*60}")
        
        for i, reason in enumerate(top_reasons, 1):
            reason_text = reason.get('reason', 'Unknown')
            count = reason.get('count', 0)
            percentage = (count / total * 100) if total > 0 else 0
            
            # Visual bar
            bar_length = int(percentage / 10)
            bar = "█" * bar_length + "░" * (10 - bar_length)
            
            output.append(f"{i}. {reason_text:30} {count:>3} ({percentage:>5.1f}%) {bar}")
        
        output.append(f"\n💡 Actionable Insights:")
        if top_reasons:
            top_reason = top_reasons[0].get('reason', 'Unknown')
            output.append(f"   • Primary issue: {top_reason}")
            output.append(f"   • Focus on improving candidate screening for this area")
    
    output.append(f"{'='*60}")
    
    return "\n".join(output)
