"""
Main Pipeline Orchestrator
Data Processing Pipeline for Business Order Dataset
Author: Satyam Jaiswal
Student ID: rotman_ds_2601001
"""

import os
import sys
from src.loader import DataLoader
from src.cleaner import DataCleaner
from src.analyzer import DataAnalyzer
from src.reporter import ReportGenerator


def create_directories():
    """Create necessary output directories if they don't exist"""
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('outputs/screenshots', exist_ok=True)
    print("✓ Directories ready")


def main():
    """Execute the complete data processing pipeline"""
    
    print("\n" + "="*80)
    print("DATA PROCESSING PIPELINE - CAPSTONE PROJECT PART 2")
    print("="*80)
    print(f"Author: Satyam Jaiswal")
    print(f"Student ID: rotman_ds_2601001")
    print("="*80 + "\n")
    
    try:
        # Step 0: Create directories
        print("STEP 0: Creating output directories...")
        create_directories()
        
        # Step 1: Load Data
        print("\nSTEP 1: Loading raw data...")
        loader = DataLoader()
        
        orders = loader.load_orders('data/raw_orders.csv')
        products = loader.load_product_master('data/product_master.csv')
        
        # Step 2: Clean and Validate Data
        print("\nSTEP 2: Cleaning and validating orders...")
        cleaner = DataCleaner()
        cleaned_orders, rejected_orders = cleaner.clean_orders(orders, products)
        
        # Step 3: Save Cleaned and Rejected Data
        print("\nSTEP 3: Saving cleaned and rejected records...")
        cleaner.save_cleaned_orders(cleaned_orders, 'outputs/cleaned_orders.csv')
        cleaner.save_rejected_orders(rejected_orders, 'outputs/rejected_records.csv')
        
        # Step 4: Analyze Data
        print("\nSTEP 4: Analyzing cleaned data...")
        analyzer = DataAnalyzer()
        analysis = analyzer.analyze(cleaned_orders, rejected_orders, products)
        
        # Step 5: Generate Report
        print("\nSTEP 5: Generating business summary report...")
        reporter = ReportGenerator()
        report_content = reporter.generate_summary_report(
            analysis,
            'outputs/summary_report.txt'
        )
        
        # Display summary
        print("\n" + "="*80)
        print("PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\nPIPELINE STATISTICS:")
        print(f"  Total Raw Records: {analysis['total_raw_records']}")
        print(f"  Total Cleaned Records: {analysis['total_cleaned_records']}")
        print(f"  Total Rejected Records: {analysis['total_rejected_records']}")
        print(f"  Data Quality Rate: {(analysis['total_cleaned_records']/analysis['total_raw_records']*100) if analysis['total_raw_records'] > 0 else 0:.2f}%")
        print(f"\nREVENUE METRICS:")
        print(f"  Total Revenue: ₹{analysis['total_revenue']:,.2f}")
        
        if analysis['top_3_customers']:
            print(f"\nTOP 3 CUSTOMERS:")
            for idx, customer in enumerate(analysis['top_3_customers'], 1):
                print(f"  {idx}. {customer['customer_name']}: ₹{customer['total_spend']:,.2f}")
        
        print(f"\nOUTPUT FILES GENERATED:")
        print(f"  ✓ outputs/cleaned_orders.csv")
        print(f"  ✓ outputs/rejected_records.csv")
        print(f"  ✓ outputs/summary_report.txt")
        print(f"  ✓ outputs/screenshots/ (add screenshots here)")
        
        print("\n" + "="*80 + "\n")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"\n✗ ERROR: File not found - {str(e)}")
        print("Please ensure raw_orders.csv and product_master.csv exist in the data/ directory")
        return 1
    
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
