# Python Data Processing Pipeline - Capstone Project Part 2

## Assignment Information
- **Assignment Title:** Data Processing Without Pandas
- **Student Name:** Satyam Jaiswal
- **Student ID:** rotman_ds_2601001
- **Project Part:** 2 (Python Data Processing Without Pandas)

---

## 📋 Project Overview

This project implements a comprehensive Python data processing pipeline for cleaning and analyzing a business order dataset. The pipeline reads raw CSV files, validates and cleans the data, identifies and rejects invalid records, and generates a detailed business summary report.

**Key Constraint:** The entire pipeline is built using **pure Python** without pandas library, using only the built-in `csv` module, lists, dictionaries, functions, and proper exception handling.

---

## 📂 Project Structure

```
satyamjaiswal_rotman_ds_2601001_part2_python_data_processing/
│
├── README.md                          # This file
├── main.py                            # Pipeline orchestrator
│
├── src/                               # Source modules
│   ├── __init__.py                    # Package initializer
│   ├── loader.py                      # Data loading module
│   ├── cleaner.py                     # Data cleaning & validation
│   ├── analyzer.py                    # Data analysis & insights
│   └── reporter.py                    # Report generation
│
├── data/                              # Input data directory
│   ├── raw_orders.csv                 # Raw order records (60+ rows)
│   └── product_master.csv             # Product reference data (10+ products)
│
├── outputs/                           # Generated output files
│   ├── cleaned_orders.csv             # Validated and cleaned order records
│   ├── rejected_records.csv           # Records rejected with reasons
│   ├── summary_report.txt             # Business summary report
│   └── screenshots/                   # Execution screenshots
│
└── tests/                             # Test documentation
    └── test_cases.md                  # 16 comprehensive test cases
```

---

## 📊 Dataset Description

### Raw Orders CSV (`data/raw_orders.csv`)
- **Records:** 60 rows of order data
- **Purpose:** Raw, unvalidated order information from the business
- **Columns:**
  - `order_id`: Unique order identifier
  - `customer_id`: Customer identifier
  - `customer_name`: Name of the customer
  - `city`: City where the customer is located
  - `product_id`: Product purchased (must exist in product master)
  - `quantity`: Number of units ordered
  - `unit_price`: Price per unit
  - `order_status`: Status of the order
  - `payment_method`: Method used for payment
  - `order_date`: Date of order (YYYY-MM-DD format)

### Product Master CSV (`data/product_master.csv`)
- **Records:** 12 products
- **Purpose:** Reference data for product validation
- **Columns:**
  - `product_id`: Unique product identifier
  - `product_name`: Name of the product
  - `category`: Product category (Electronics, Furniture, Accessories)
  - `standard_price`: Standard price for the product

---

## 🔴 Intentionally Added Data Quality Issues

The raw dataset includes **12+ intentional data quality issues** to simulate real-world challenges:

| # | Issue Type | Count | Example | Location |
|---|-----------|-------|---------|----------|
| 1 | **Duplicate Order IDs** | 3 | ORD001 appears 3 times | Rows 1, 11, 46 |
| 2 | **Missing Customer Names** | 3 | Empty customer_name field | Rows 12, 28, 49 |
| 3 | **Missing City Values** | 4 | Empty city field | Rows 13, 15, 24, 42 |
| 4 | **Inconsistent City Spellings** | Multiple | "delhi", "Delhi", "DELHI", "NEW DELHI", "new delhi" | Throughout |
| 5 | **Extra Spaces** | Multiple | " Alice Williams " | Rows 4, 8, etc. |
| 6 | **Incorrect Casing** | Multiple | "JAMES miller", "ROBERT TAYLOR" | Throughout |
| 7 | **Quantity as Zero** | 2 | quantity = 0 | Rows 14, 29 |
| 8 | **Negative Quantity** | 2 | quantity = -2, -1 | Rows 15, 50 |
| 9 | **Unit Price Mismatch** | 2 | 90999 vs 89999 standard | Rows 18, 37 |
| 10 | **Invalid Order Status** | 3 | "InProcess", "OnHold", "UnknownStatus" | Rows 20, 40, 52 |
| 11 | **Invalid Payment Method** | 3 | "InvalidMethod", "InvalidPayment", "WalletPay" | Rows 17, 33, 59 |
| 12 | **Invalid Date Format** | 1 | "02/11/2024" instead of YYYY-MM-DD | Row 28 |

---

## 🧹 Cleaning Rules Applied

### Task 1: Data Loading
- Load raw orders CSV using Python's `csv` module
- Load product master CSV for reference
- Store data in Python lists and dictionaries
- NO hardcoding of data in Python files

### Task 2: Data Cleaning & Standardization

1. **Text Normalization**
   - Trim leading/trailing whitespace from all text fields
   - Remove extra spaces within text
   - Apply title casing to customer names (e.g., "john smith" → "John Smith")

2. **City Standardization**
   - Normalize city variations to standard format
   - Mapping examples:
     - "delhi", "DELHI", "new delhi", "NEW DELHI" → "Delhi"
     - "bangalore", "BENGALURU" → "Bangalore"
     - "kolkata", "KOLKATA" → "Kolkata"
     - "mumbai", "MUMBAI" → "Mumbai"
     - "pune", "PUNE" → "Pune"
     - "hyderabad", "HYDERABAD" → "Hyderabad"

3. **Customer Name Standardization**
   - Remove extra spaces
   - Apply title case formatting

4. **Order Status Standardization**
   - Valid statuses: `Completed`, `Pending`, `Cancelled`
   - Any other status triggers rejection

5. **Payment Method Validation**
   - Valid methods: `Credit Card`, `Debit Card`, `UPI`, `NetBanking`
   - Any other method triggers rejection

6. **Quantity Validation**
   - Must be integer
   - Must be greater than 0
   - Invalid values trigger rejection

7. **Price Validation**
   - Must be numeric (integer or float)
   - Unit price must match product master standard price
   - Mismatch triggers rejection

8. **Date Validation**
   - Must follow YYYY-MM-DD format
   - Invalid dates trigger rejection

9. **Total Amount Calculation**
   - For valid records: `total_amount = quantity × unit_price`
   - Rounded to 2 decimal places

10. **Product Enrichment**
    - Join with product master to add:
      - `product_name`
      - `category`
    - Product ID must exist in master data

---

## ❌ Rejection Rules Applied

Records are rejected if they have ANY of the following issues:

| Rejection Reason | Trigger Condition |
|------------------|-------------------|
| Duplicate order ID | Order ID already processed |
| Missing customer name | Empty or whitespace-only name |
| Missing city | Empty or whitespace-only city |
| Invalid quantity | Zero, negative, or non-numeric |
| Product ID not found | Product doesn't exist in master |
| Invalid order status | Not in [Completed, Pending, Cancelled] |
| Invalid payment method | Not in [Credit Card, Debit Card, UPI, NetBanking] |
| Unit price mismatch | Doesn't match product master price |
| Invalid date format | Not in YYYY-MM-DD format |

**Multiple Issues:** If a record has multiple issues, ALL reasons are documented in the rejection reason field, separated by " | ".

---

## 📤 Output Files Generated

### 1. `outputs/cleaned_orders.csv`
- **Purpose:** Contains only valid, cleaned records ready for business use
- **Records:** Only records that passed all validations
- **Columns:**
  ```
  order_id, customer_id, customer_name, city, product_id, product_name, 
  category, quantity, unit_price, total_amount, order_status, payment_method, order_date
  ```
- **Quality:** 100% data integrity

### 2. `outputs/rejected_records.csv`
- **Purpose:** Contains all rejected records with detailed rejection reasons
- **Records:** Records that failed one or more validation rules
- **Columns:**
  ```
  order_id, customer_id, customer_name, city, product_id, quantity, 
  unit_price, order_status, payment_method, order_date, rejection_reasons
  ```
- **Key Feature:** `rejection_reasons` column explains why each record was rejected

### 3. `outputs/summary_report.txt`
- **Purpose:** Executive business summary and analysis
- **Contents:**
  1. **Executive Summary**
     - Total records processed
     - Records cleaned vs. rejected
     - Data quality percentage
  
  2. **Revenue Analysis**
     - Total revenue from completed orders
     - Revenue breakdown by product category
     - Revenue breakdown by city
  
  3. **Payment Method Analysis**
     - Distribution of orders by payment method
     - Percentages for each method
  
  4. **Top Customers**
     - Top 3 customers by total spending
     - Customer names, total spend, order count
  
  5. **Product Analysis**
     - Product with highest quantity sold
     - Category with highest revenue
  
  6. **Data Quality Analysis**
     - Count of rejection reasons
     - Percentage breakdown
  
  7. **Key Business Insights**
     - Data quality observations
     - Payment method preferences
     - Revenue concentration analysis
  
  8. **Recommendations**
     - Actionable insights for business improvement

### 4. `outputs/screenshots/`
- **Purpose:** Visual evidence of pipeline execution
- **Contents:** Screenshots of:
  - Pipeline execution console output
  - Sample of cleaned_orders.csv
  - Sample of rejected_records.csv
  - Final summary_report.txt output

---

## 🚀 How to Run the Project

### Prerequisites
- Python 3.7 or higher
- No external libraries required (pure Python)

### Execution Steps

1. **Navigate to project directory:**
   ```bash
   cd satyamjaiswal_rotman_ds_2601001_part2_python_data_processing
   ```

2. **Run the pipeline:**
   ```bash
   python main.py
   ```

3. **Check outputs:**
   - `outputs/cleaned_orders.csv` - Valid records
   - `outputs/rejected_records.csv` - Rejected records with reasons
   - `outputs/summary_report.txt` - Business summary report

### Expected Console Output
```
================================================================================
DATA PROCESSING PIPELINE - CAPSTONE PROJECT PART 2
================================================================================
Author: Satyam Jaiswal
Student ID: rotman_ds_2601001
================================================================================

STEP 0: Creating output directories...
✓ Directories ready

STEP 1: Loading raw data...
✓ Successfully loaded 60 orders from data/raw_orders.csv
✓ Successfully loaded 12 products from data/product_master.csv

STEP 2: Cleaning and validating orders...
============================================================
CLEANING AND VALIDATING ORDERS
============================================================
✓ Valid records: XX
✗ Rejected records: XX

STEP 3: Saving cleaned and rejected records...
✓ Saved XX cleaned orders to outputs/cleaned_orders.csv
✓ Saved XX rejected orders to outputs/rejected_records.csv

STEP 4: Analyzing cleaned data...

STEP 5: Generating business summary report...
✓ Summary report saved to outputs/summary_report.txt

================================================================================
PIPELINE EXECUTION COMPLETED SUCCESSFULLY
================================================================================
```

---

## 🔬 Testing

### Test Coverage
The project includes **16 comprehensive test cases** in `tests/test_cases.md`:

1. Valid record processing
2. Duplicate order ID detection
3. Missing customer name detection
4. Missing city detection
5. Zero quantity rejection
6. Negative quantity rejection
7. Invalid product ID handling
8. Invalid payment method handling
9. Invalid order status handling
10. Unit price mismatch detection
11. Invalid date format detection
12. Revenue calculation accuracy
13. Text standardization
14. Multiple rejection reasons
15. Rejection reason aggregation
16. Business insights generation

### Running Tests
Tests are documented in `tests/test_cases.md` with:
- Input conditions
- Expected outputs
- Reasoning for each test case

Manual testing can be performed by:
1. Running the main pipeline
2. Comparing outputs with expected results in test_cases.md
3. Verifying calculations in summary_report.txt

---

## 📈 Key Features

### Data Processing
✅ CSV reading and writing without pandas  
✅ Duplicate detection and removal  
✅ Text standardization and normalization  
✅ Data validation with comprehensive rules  
✅ Price and inventory verification  
✅ Date format validation  
✅ Exception handling for data errors  

### Code Quality
✅ Modular architecture (loader, cleaner, analyzer, reporter)  
✅ Clear variable naming  
✅ Comprehensive comments and docstrings  
✅ Error handling with meaningful messages  
✅ Proper use of Python data structures  
✅ Functions for code reusability  

### Reporting
✅ Cleaned data CSV output  
✅ Rejection records with detailed reasons  
✅ Executive summary report  
✅ Business insights and recommendations  
✅ Revenue analysis by category and city  
✅ Customer analytics  

---

## 💡 Business Insights Generated

The pipeline automatically generates 3+ business insights:

1. **Data Quality Alert**
   - Calculates percentage of rejected records
   - Highlights need for data validation at point of entry
   
2. **Payment Method Analysis**
   - Identifies most popular payment method
   - Highlights need for robust infrastructure for preferred channels
   
3. **Revenue Concentration**
   - Identifies top-performing product categories
   - Suggests expansion opportunities for high-revenue products

---

## 📝 Technical Specifications

### Language & Libraries
- **Language:** Python 3.7+
- **Libraries:** Only built-in modules (csv, datetime, typing)
- **No external dependencies:** ✅ No pandas, numpy, or other libraries

### Data Structures Used
- `list`: For storing multiple records
- `dict`: For storing record data with field names
- `set`: For tracking duplicate order IDs
- String methods for text processing

### Key Functions
- `load_orders()` - CSV reading
- `load_product_master()` - Reference data loading
- `clean_orders()` - Validation and cleaning
- `save_cleaned_orders()` - CSV writing
- `save_rejected_orders()` - Rejection records output
- `analyze()` - Data analysis
- `generate_summary_report()` - Report generation

---

## 🎯 Assumptions Made

1. **Date Format:** All valid dates follow YYYY-MM-DD format
2. **Price Precision:** Prices are compared exactly with product master (no tolerance for rounding differences)
3. **City Standardization:** Only mapping the specified city names; unmapped cities are converted to title case
4. **Duplicate Detection:** Based on order_id only (same order_id = duplicate, regardless of other fields)
5. **Quantity Validation:** Strict rule - must be positive integer > 0
6. **Revenue Calculation:** Only "Completed" orders are included in revenue calculations
7. **File Encoding:** All CSV files use UTF-8 encoding
8. **Field Trimming:** All text fields are trimmed of leading/trailing whitespace
9. **Case Insensitivity:** City names and payment methods are case-insensitive for matching

---

## ✅ Final Checklist

- [x] Repository name exactly: `satyamjaiswal_rotman_ds_2601001_part2_python_data_processing`
- [x] Folder structure exactly as specified
- [x] Raw data created with 60+ rows and 12+ quality issues
- [x] Product master created with 10+ products
- [x] Pandas NOT used anywhere
- [x] Pure Python with csv module
- [x] Modular code in src/ folder
- [x] main.py orchestrates the pipeline
- [x] loader.py handles data input
- [x] cleaner.py handles validation and cleaning
- [x] analyzer.py generates insights
- [x] reporter.py creates summary report
- [x] cleaned_orders.csv generated
- [x] rejected_records.csv generated with rejection reasons
- [x] summary_report.txt generated
- [x] README.md comprehensive and complete
- [x] test_cases.md with 16+ test cases
- [x] All requirements met
- [x] Screenshots to be added to outputs/screenshots/

---

## 📞 Contact & Support

**Author:** Satyam Jaiswal  
**Student ID:** rotman_ds_2601001  

For questions or issues, please refer to the test cases and documentation within each module.

---

## 📄 License

This project is created for educational purposes as part of the Capstone assignment.

---

**Last Updated:** June 2026 
