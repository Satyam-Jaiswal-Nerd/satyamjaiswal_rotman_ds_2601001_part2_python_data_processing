"""
Data Cleaner Module
Handles data validation, cleaning, and rejection of invalid records
"""

import csv
from typing import List, Dict, Tuple
from datetime import datetime


class DataCleaner:
    """Clean and validate order data"""
    
    def __init__(self):
        """Initialize the DataCleaner"""
        self.valid_order_statuses = ['Completed', 'Pending', 'Cancelled']
        self.valid_payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'NetBanking']
        self.seen_order_ids = set()
        
    def clean_orders(
        self,
        orders: List[Dict],
        products: Dict
    ) -> Tuple[List[Dict], List[Dict]]:
        """
        Clean and validate all orders
        
        Args:
            orders (List[Dict]): Raw orders data
            products (Dict): Product master data
            
        Returns:
            Tuple: (cleaned_orders, rejected_orders)
        """
        cleaned_orders = []
        rejected_orders = []
        self.seen_order_ids = set()
        
        print("\n" + "="*60)
        print("CLEANING AND VALIDATING ORDERS")
        print("="*60)
        
        for order in orders:
            rejection_reasons = []
            cleaned_order = order.copy()
            
            # Check for duplicate order ID
            if order['order_id'] in self.seen_order_ids:
                rejection_reasons.append("Duplicate order ID")
            else:
                self.seen_order_ids.add(order['order_id'])
            
            # Validate and clean customer name
            if not order['customer_name'] or order['customer_name'].strip() == '':
                rejection_reasons.append("Missing customer name")
            else:
                cleaned_order['customer_name'] = self._standardize_text(
                    order['customer_name']
                )
            
            # Validate and clean city
            if not order['city'] or order['city'].strip() == '':
                rejection_reasons.append("Missing city")
            else:
                cleaned_order['city'] = self._standardize_city(order['city'])
            
            # Validate product ID
            if order['product_id'] not in products:
                rejection_reasons.append("Product ID not found in master")
            
            # Validate quantity
            try:
                quantity = int(order['quantity'])
                if quantity <= 0:
                    rejection_reasons.append("Invalid quantity (must be positive)")
                else:
                    cleaned_order['quantity'] = quantity
            except (ValueError, TypeError):
                rejection_reasons.append("Invalid quantity format")
            
            # Validate and clean unit price
            try:
                unit_price = float(order['unit_price'])
                if order['product_id'] in products:
                    standard_price = products[order['product_id']]['standard_price']
                    if unit_price != standard_price:
                        rejection_reasons.append(
                            f"Unit price mismatch (expected {standard_price}, got {unit_price})"
                        )
                cleaned_order['unit_price'] = unit_price
            except (ValueError, TypeError):
                rejection_reasons.append("Invalid unit price format")
            
            # Validate order status
            if order['order_status'] not in self.valid_order_statuses:
                rejection_reasons.append(
                    f"Invalid order status: {order['order_status']}"
                )
            
            # Validate payment method
            if order['payment_method'] not in self.valid_payment_methods:
                rejection_reasons.append(
                    f"Invalid payment method: {order['payment_method']}"
                )
            
            # Validate and parse order date
            is_valid_date = self._validate_date(order['order_date'])
            if not is_valid_date:
                rejection_reasons.append(
                    f"Invalid date format: {order['order_date']} (expected YYYY-MM-DD)"
                )
            
            # Decide whether to accept or reject
            if rejection_reasons:
                cleaned_order['rejection_reasons'] = ' | '.join(rejection_reasons)
                rejected_orders.append(cleaned_order)
            else:
                # Add calculated fields for valid orders
                try:
                    quantity = int(cleaned_order.get('quantity', 0))
                    unit_price = float(cleaned_order.get('unit_price', 0))
                    cleaned_order['total_amount'] = quantity * unit_price
                    
                    # Add product details
                    if cleaned_order['product_id'] in products:
                        product = products[cleaned_order['product_id']]
                        cleaned_order['product_name'] = product['product_name']
                        cleaned_order['category'] = product['category']
                except (ValueError, TypeError):
                    cleaned_order['total_amount'] = 0
                
                cleaned_orders.append(cleaned_order)
        
        print(f"✓ Valid records: {len(cleaned_orders)}")
        print(f"✗ Rejected records: {len(rejected_orders)}")
        
        return cleaned_orders, rejected_orders
    
    def _standardize_text(self, text: str) -> str:
        """
        Standardize text: trim spaces and fix casing
        
        Args:
            text (str): Raw text
            
        Returns:
            str: Standardized text
        """
        if not text:
            return ''
        # Remove extra spaces and title case
        return ' '.join(text.strip().split()).title()
    
    def _standardize_city(self, city: str) -> str:
        """
        Standardize city names with common variations
        
        Args:
            city (str): Raw city name
            
        Returns:
            str: Standardized city name
        """
        if not city:
            return ''
        
        city_mapping = {
            'delhi': 'Delhi',
            'new delhi': 'Delhi',
            'NEW DELHI': 'Delhi',
            'DELHI': 'Delhi',
            'new_delhi': 'Delhi',
            'mumbai': 'Mumbai',
            'MUMBAI': 'Mumbai',
            'bangalore': 'Bangalore',
            'BANGALORE': 'Bangalore',
            'bengaluru': 'Bangalore',
            'BENGALURU': 'Bangalore',
            'kolkata': 'Kolkata',
            'KOLKATA': 'Kolkata',
            'pune': 'Pune',
            'PUNE': 'Pune',
            'hyderabad': 'Hyderabad',
            'HYDERABAD': 'Hyderabad',
        }
        
        normalized = ' '.join(city.strip().split()).lower()
        return city_mapping.get(normalized, normalized.title())
    
    def _validate_date(self, date_str: str) -> bool:
        """
        Validate date format (YYYY-MM-DD)
        
        Args:
            date_str (str): Date string to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not date_str or date_str.strip() == '':
            return False
        
        try:
            datetime.strptime(date_str.strip(), '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def save_cleaned_orders(
        self,
        cleaned_orders: List[Dict],
        filepath: str
    ) -> None:
        """
        Save cleaned orders to CSV file
        
        Args:
            cleaned_orders (List[Dict]): Cleaned order records
            filepath (str): Output filepath
        """
        if not cleaned_orders:
            print(f"✓ No valid records to save")
            return
        
        try:
            fieldnames = [
                'order_id', 'customer_id', 'customer_name', 'city',
                'product_id', 'product_name', 'category',
                'quantity', 'unit_price', 'total_amount',
                'order_status', 'payment_method', 'order_date'
            ]
            
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for order in cleaned_orders:
                    row = {field: order.get(field, '') for field in fieldnames}
                    writer.writerow(row)
            
            print(f"✓ Saved {len(cleaned_orders)} cleaned orders to {filepath}")
            
        except Exception as e:
            print(f"✗ Error saving cleaned orders: {str(e)}")
            raise
    
    def save_rejected_orders(
        self,
        rejected_orders: List[Dict],
        filepath: str
    ) -> None:
        """
        Save rejected orders with rejection reasons
        
        Args:
            rejected_orders (List[Dict]): Rejected order records
            filepath (str): Output filepath
        """
        if not rejected_orders:
            print(f"✓ No rejected records to save")
            return
        
        try:
            fieldnames = [
                'order_id', 'customer_id', 'customer_name', 'city',
                'product_id', 'quantity', 'unit_price',
                'order_status', 'payment_method', 'order_date',
                'rejection_reasons'
            ]
            
            with open(filepath, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for order in rejected_orders:
                    row = {field: order.get(field, '') for field in fieldnames}
                    writer.writerow(row)
            
            print(f"✓ Saved {len(rejected_orders)} rejected orders to {filepath}")
            
        except Exception as e:
            print(f"✗ Error saving rejected orders: {str(e)}")
            raise
