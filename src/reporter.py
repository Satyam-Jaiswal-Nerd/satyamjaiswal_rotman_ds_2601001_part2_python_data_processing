"""
Report Generator Module
Generates formatted business summary reports
"""

from typing import Dict, List
from datetime import datetime


class ReportGenerator:
    """Generate comprehensive business reports"""
    
    def __init__(self):
        """Initialize the ReportGenerator"""
        self.report_content = []
    
    def generate_summary_report(
        self,
        analysis: Dict,
        output_filepath: str
    ) -> str:
        """
        Generate comprehensive business summary report
        
        Args:
            analysis (Dict): Analysis results from DataAnalyzer
            output_filepath (str): Path to save the report
            
        Returns:
            str: Report content
        """
        self.report_content = []
        
        # Header
        self._add_section("BUSINESS SUMMARY REPORT")
        self._add_line(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._add_line("Prepared by: Satyam Jaiswal (ID: rotman_ds_2601001)")
        
        # Executive Summary
        self._add_section("1. EXECUTIVE SUMMARY")
        self._add_line(f"Total Raw Records Processed: {analysis['total_raw_records']}")
        self._add_line(f"Valid Records (Cleaned): {analysis['total_cleaned_records']}")
        self._add_line(f"Rejected Records: {analysis['total_rejected_records']}")
        
        quality_pct = (
            (analysis['total_cleaned_records'] / analysis['total_raw_records'] * 100)
            if analysis['total_raw_records'] > 0
            else 0
        )
        self._add_line(f"Data Quality Rate: {quality_pct:.2f}%")
        self._add_blank_line()
        
        # Revenue Analysis
        self._add_section("2. REVENUE ANALYSIS")
        self._add_line(f"Total Revenue (Completed Orders): ₹{analysis['total_revenue']:,.2f}")
        
        if analysis['revenue_by_category']:
            self._add_line("\nRevenue Breakdown by Category:")
            for category, revenue in analysis['revenue_by_category'].items():
                pct = (revenue / analysis['total_revenue'] * 100) if analysis['total_revenue'] > 0 else 0
                self._add_line(f"  • {category}: ₹{revenue:,.2f} ({pct:.1f}%)")
        
        if analysis['revenue_by_city']:
            self._add_line("\nRevenue Breakdown by City:")
            for city, revenue in list(analysis['revenue_by_city'].items())[:10]:
                pct = (revenue / analysis['total_revenue'] * 100) if analysis['total_revenue'] > 0 else 0
                self._add_line(f"  • {city}: ₹{revenue:,.2f} ({pct:.1f}%)")
        self._add_blank_line()
        
        # Payment Method Analysis
        self._add_section("3. PAYMENT METHOD ANALYSIS")
        if analysis['orders_by_payment_method']:
            for method, count in analysis['orders_by_payment_method'].items():
                pct = (count / analysis['total_cleaned_records'] * 100) if analysis['total_cleaned_records'] > 0 else 0
                self._add_line(f"  • {method}: {count} orders ({pct:.1f}%)")
        self._add_blank_line()
        
        # Top Customers
        self._add_section("4. TOP CUSTOMERS")
        if analysis['top_3_customers']:
            for idx, customer in enumerate(analysis['top_3_customers'], 1):
                self._add_line(
                    f"  {idx}. {customer['customer_name']}: "
                    f"₹{customer['total_spend']:,.2f} ({customer['order_count']} orders)"
                )
        self._add_blank_line()
        
        # Product Analysis
        self._add_section("5. PRODUCT ANALYSIS")
        highest_qty = analysis['product_highest_quantity']
        self._add_line(
            f"Product with Highest Quantity Sold: {highest_qty['product_name']} "
            f"({highest_qty['total_quantity']} units)"
        )
        
        highest_category = analysis['category_highest_revenue']
        self._add_line(
            f"Category with Highest Revenue: {highest_category['category']} "
            f"(₹{highest_category['revenue']:,.2f})"
        )
        self._add_blank_line()
        
        # Data Quality Issues
        self._add_section("6. DATA QUALITY ISSUES - REJECTION ANALYSIS")
        if analysis['rejection_reasons_count']:
            self._add_line("Rejection Reasons Count:")
            for reason, count in analysis['rejection_reasons_count'].items():
                pct = (count / analysis['total_rejected_records'] * 100) if analysis['total_rejected_records'] > 0 else 0
                self._add_line(f"  • {reason}: {count} occurrences ({pct:.1f}%)")
        else:
            self._add_line("No rejection reasons recorded.")
        self._add_blank_line()
        
        # Business Insights
        self._add_section("7. KEY BUSINESS INSIGHTS")
        if analysis['business_insights']:
            for idx, insight in enumerate(analysis['business_insights'], 1):
                self._add_line(f"  Insight {idx}:")
                # Wrap long text
                words = insight.split()
                current_line = ""
                for word in words:
                    if len(current_line) + len(word) + 1 > 95:
                        if current_line:
                            self._add_line(f"    {current_line}")
                        current_line = word
                    else:
                        current_line += (" " + word if current_line else word)
                if current_line:
                    self._add_line(f"    {current_line}")
                self._add_blank_line()
        self._add_blank_line()
        
        # Footer
        self._add_section("8. RECOMMENDATIONS")
        self._add_line("  1. Implement data validation at the point of data entry to reduce rejection rate.")
        self._add_line("  2. Focus marketing efforts on high-revenue categories to maximize profitability.")
        self._add_line("  3. Ensure payment gateway availability for most-used payment methods.")
        self._add_line("  4. Monitor data quality metrics regularly and set improvement targets.")
        self._add_blank_line()
        
        # Save report
        self._save_report(output_filepath)
        
        return '\n'.join(self.report_content)
    
    def _add_section(self, title: str) -> None:
        """Add a section header"""
        self.report_content.append("")
        self.report_content.append("=" * 80)
        self.report_content.append(title)
        self.report_content.append("=" * 80)
    
    def _add_line(self, content: str) -> None:
        """Add a line of content"""
        self.report_content.append(content)
    
    def _add_blank_line(self) -> None:
        """Add a blank line"""
        self.report_content.append("")
    
    def _save_report(self, filepath: str) -> None:
        """
        Save report to file
        
        Args:
            filepath (str): Path to save the report
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write('\n'.join(self.report_content))
            print(f"✓ Summary report saved to {filepath}")
        except Exception as e:
            print(f"✗ Error saving report: {str(e)}")
            raise
