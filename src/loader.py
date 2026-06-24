"""
Data Loader Module
Handles reading CSV files and converting them to appropriate data structures
"""

import csv
from typing import List, Dict


class DataLoader:
    """Load CSV files into Python data structures"""
    
    def __init__(self):
        """Initialize the DataLoader"""
        self.orders = []
        self.products = {}
        
    def load_orders(self, filepath: str) -> List[Dict]:
        """
        Load orders from CSV file
        
        Args:
            filepath (str): Path to raw_orders.csv
            
        Returns:
            List[Dict]: List of order dictionaries
        """
        try:
            orders = []
            with open(filepath, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                if csv_reader.fieldnames is None:
                    raise ValueError("CSV file is empty or has no headers")
                
                for row_num, row in enumerate(csv_reader, start=2):
                    try:
                        # Convert string fields to appropriate types
                        order = {
                            'order_id': row.get('order_id', '').strip(),
                            'customer_id': row.get('customer_id', '').strip(),
                            'customer_name': row.get('customer_name', '').strip(),
                            'city': row.get('city', '').strip(),
                            'product_id': row.get('product_id', '').strip(),
                            'quantity': row.get('quantity', '').strip(),
                            'unit_price': row.get('unit_price', '').strip(),
                            'order_status': row.get('order_status', '').strip(),
                            'payment_method': row.get('payment_method', '').strip(),
                            'order_date': row.get('order_date', '').strip(),
                            'row_number': row_num
                        }
                        orders.append(order)
                    except Exception as e:
                        print(f"Warning: Error processing row {row_num}: {str(e)}")
                        continue
            
            self.orders = orders
            print(f"✓ Successfully loaded {len(orders)} orders from {filepath}")
            return orders
            
        except FileNotFoundError:
            print(f"✗ Error: File not found - {filepath}")
            raise
        except Exception as e:
            print(f"✗ Error loading orders: {str(e)}")
            raise
    
    def load_product_master(self, filepath: str) -> Dict:
        """
        Load product master data from CSV file
        
        Args:
            filepath (str): Path to product_master.csv
            
        Returns:
            Dict: Dictionary with product_id as key and product details as value
        """
        try:
            products = {}
            with open(filepath, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                if csv_reader.fieldnames is None:
                    raise ValueError("CSV file is empty or has no headers")
                
                for row in csv_reader:
                    product_id = row.get('product_id', '').strip()
                    if product_id:
                        products[product_id] = {
                            'product_id': product_id,
                            'product_name': row.get('product_name', '').strip(),
                            'category': row.get('category', '').strip(),
                            'standard_price': float(row.get('standard_price', '0'))
                        }
            
            self.products = products
            print(f"✓ Successfully loaded {len(products)} products from {filepath}")
            return products
            
        except FileNotFoundError:
            print(f"✗ Error: File not found - {filepath}")
            raise
        except ValueError as e:
            print(f"✗ Error parsing product prices: {str(e)}")
            raise
        except Exception as e:
            print(f"✗ Error loading products: {str(e)}")
            raise
    
    def get_orders(self) -> List[Dict]:
        """Get loaded orders"""
        return self.orders
    
    def get_products(self) -> Dict:
        """Get loaded products"""
        return self.products
