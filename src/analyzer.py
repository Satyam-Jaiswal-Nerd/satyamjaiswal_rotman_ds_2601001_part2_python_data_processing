"""
Data Analyzer Module
Handles analysis of cleaned data to generate business insights
"""

from typing import List, Dict


class DataAnalyzer:
    """Analyze cleaned order data for business insights"""
    
    def __init__(self):
        """Initialize the DataAnalyzer"""
        self.clean_orders = []
        self.rejected_orders = []
        self.products = {}
        
    def analyze(
        self,
        clean_orders: List[Dict],
        rejected_orders: List[Dict],
        products: Dict
    ) -> Dict:
        """
        Perform comprehensive analysis on cleaned data
        
        Args:
            clean_orders (List[Dict]): Cleaned orders
            rejected_orders (List[Dict]): Rejected orders
            products (Dict): Product master data
            
        Returns:
            Dict: Analysis results
        """
        self.clean_orders = clean_orders
        self.rejected_orders = rejected_orders
        self.products = products
        
        analysis = {
            'total_raw_records': len(clean_orders) + len(rejected_orders),
            'total_cleaned_records': len(clean_orders),
            'total_rejected_records': len(rejected_orders),
            'total_revenue': self._calculate_total_revenue(),
            'revenue_by_category': self._analyze_revenue_by_category(),
            'revenue_by_city': self._analyze_revenue_by_city(),
            'orders_by_payment_method': self._analyze_payment_methods(),
            'top_3_customers': self._get_top_customers(),
            'product_highest_quantity': self._get_highest_quantity_product(),
            'category_highest_revenue': self._get_highest_revenue_category(),
            'rejection_reasons_count': self._count_rejection_reasons(),
            'business_insights': self._generate_insights()
        }
        
        return analysis
    
    def _calculate_total_revenue(self) -> float:
        """Calculate total revenue from completed orders"""
        total = 0.0
        for order in self.clean_orders:
            if order.get('order_status') == 'Completed':
                try:
                    total += float(order.get('total_amount', 0))
                except (ValueError, TypeError):
                    pass
        return round(total, 2)
    
    def _analyze_revenue_by_category(self) -> Dict:
        """Analyze revenue distribution by product category"""
        category_revenue = {}
        
        for order in self.clean_orders:
            if order.get('order_status') == 'Completed':
                category = order.get('category', 'Unknown')
                try:
                    amount = float(order.get('total_amount', 0))
                    category_revenue[category] = category_revenue.get(category, 0) + amount
                except (ValueError, TypeError):
                    pass
        
        # Sort by revenue descending
        sorted_revenue = sorted(
            category_revenue.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return dict(sorted_revenue)
    
    def _analyze_revenue_by_city(self) -> Dict:
        """Analyze revenue distribution by city"""
        city_revenue = {}
        
        for order in self.clean_orders:
            if order.get('order_status') == 'Completed':
                city = order.get('city', 'Unknown')
                try:
                    amount = float(order.get('total_amount', 0))
                    city_revenue[city] = city_revenue.get(city, 0) + amount
                except (ValueError, TypeError):
                    pass
        
        # Sort by revenue descending
        sorted_revenue = sorted(
            city_revenue.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return dict(sorted_revenue)
    
    def _analyze_payment_methods(self) -> Dict:
        """Analyze order distribution by payment method"""
        payment_count = {}
        
        for order in self.clean_orders:
            method = order.get('payment_method', 'Unknown')
            payment_count[method] = payment_count.get(method, 0) + 1
        
        # Sort by count descending
        sorted_count = sorted(
            payment_count.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return dict(sorted_count)
    
    def _get_top_customers(self) -> List[Dict]:
        """Get top 3 customers by total spend"""
        customer_spend = {}
        
        for order in self.clean_orders:
            if order.get('order_status') == 'Completed':
                customer_id = order.get('customer_id', 'Unknown')
                customer_name = order.get('customer_name', 'Unknown')
                try:
                    amount = float(order.get('total_amount', 0))
                    if customer_id not in customer_spend:
                        customer_spend[customer_id] = {
                            'customer_name': customer_name,
                            'total_spend': 0,
                            'order_count': 0
                        }
                    customer_spend[customer_id]['total_spend'] += amount
                    customer_spend[customer_id]['order_count'] += 1
                except (ValueError, TypeError):
                    pass
        
        # Sort by spend descending and get top 3
        sorted_customers = sorted(
            customer_spend.values(),
            key=lambda x: x['total_spend'],
            reverse=True
        )[:3]
        
        return sorted_customers
    
    def _get_highest_quantity_product(self) -> Dict:
        """Get product with highest quantity sold"""
        product_quantity = {}
        
        for order in self.clean_orders:
            if order.get('order_status') == 'Completed':
                product_id = order.get('product_id', 'Unknown')
                product_name = order.get('product_name', 'Unknown')
                try:
                    quantity = int(order.get('quantity', 0))
                    if product_id not in product_quantity:
                        product_quantity[product_id] = {
                            'product_name': product_name,
                            'total_quantity': 0
                        }
                    product_quantity[product_id]['total_quantity'] += quantity
                except (ValueError, TypeError):
                    pass
        
        if product_quantity:
            highest = max(
                product_quantity.values(),
                key=lambda x: x['total_quantity']
            )
            return highest
        
        return {'product_name': 'N/A', 'total_quantity': 0}
    
    def _get_highest_revenue_category(self) -> Dict:
        """Get category with highest revenue"""
        category_revenue = self._analyze_revenue_by_category()
        
        if category_revenue:
            highest_category = list(category_revenue.keys())[0]
            highest_revenue = category_revenue[highest_category]
            return {
                'category': highest_category,
                'revenue': round(highest_revenue, 2)
            }
        
        return {'category': 'N/A', 'revenue': 0}
    
    def _count_rejection_reasons(self) -> Dict:
        """Count occurrences of each rejection reason"""
        reason_count = {}
        
        for order in self.rejected_orders:
            reasons_str = order.get('rejection_reasons', '')
            if reasons_str:
                # Split multiple reasons
                reasons = [r.strip() for r in reasons_str.split('|')]
                for reason in reasons:
                    reason_count[reason] = reason_count.get(reason, 0) + 1
        
        # Sort by count descending
        sorted_reasons = sorted(
            reason_count.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return dict(sorted_reasons)
    
    def _generate_insights(self) -> List[str]:
        """Generate business insights from the data"""
        insights = []
        
        # Insight 1: Data quality
        rejection_rate = (
            (len(self.rejected_orders) / (len(self.clean_orders) + len(self.rejected_orders)) * 100)
            if (len(self.clean_orders) + len(self.rejected_orders)) > 0
            else 0
        )
        insights.append(
            f"Data Quality Alert: {rejection_rate:.2f}% of raw orders were rejected due to "
            f"data quality issues. Focus on data validation at point of entry."
        )
        
        # Insight 2: Payment method preference
        payment_methods = self._analyze_payment_methods()
        if payment_methods:
            preferred_method = list(payment_methods.keys())[0]
            count = payment_methods[preferred_method]
            pct = (count / len(self.clean_orders) * 100) if self.clean_orders else 0
            insights.append(
                f"Payment Preference: {preferred_method} is the most popular payment method, "
                f"used in {pct:.1f}% of all orders. Ensure robust infrastructure for this channel."
            )
        
        # Insight 3: Revenue concentration
        category_revenue = self._analyze_revenue_by_category()
        if category_revenue:
            total_revenue = self._calculate_total_revenue()
            if total_revenue > 0:
                top_category = list(category_revenue.keys())[0]
                top_revenue = category_revenue[top_category]
                pct = (top_revenue / total_revenue * 100)
                insights.append(
                    f"Revenue Concentration: The '{top_category}' category drives {pct:.1f}% of total revenue. "
                    f"Consider expanding this product line to maximize profitability."
                )
        
        return insights
    
    def get_analysis_summary(self) -> str:
        """Get a text summary of the analysis"""
        analysis = self.analyze(self.clean_orders, self.rejected_orders, self.products)
        
        summary = []
        summary.append("ANALYSIS SUMMARY")
        summary.append(f"Total Raw Records: {analysis['total_raw_records']}")
        summary.append(f"Total Cleaned Records: {analysis['total_cleaned_records']}")
        summary.append(f"Total Rejected Records: {analysis['total_rejected_records']}")
        summary.append(f"Total Revenue (Completed Orders): ₹{analysis['total_revenue']:,.2f}")
        
        return '\n'.join(summary)
