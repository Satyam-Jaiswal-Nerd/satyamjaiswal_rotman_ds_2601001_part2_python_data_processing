# Test Cases for Data Processing Pipeline

## Test Case 1: Valid Record Processing
**Objective:** Ensure valid records are correctly processed and moved to cleaned output

**Input Condition:**
- Order: `ORD001, CUST001, John Smith, Delhi, P001, 1, 89999, Completed, Credit Card, 2024-01-15`
- Product P001 exists with standard_price: 89999

**Expected Output:**
- Record should be in `cleaned_orders.csv`
- No rejection reason
- Calculated total_amount: 89999 (1 × 89999)
- Product details (product_name, category) should be added

**Reason:** Validates that all data fields are correct and pass validation rules

---

## Test Case 2: Duplicate Order ID
**Objective:** Detect and reject duplicate order IDs

**Input Condition:**
- First occurrence: `ORD001, CUST001, John Smith, Delhi, P001, 1, 89999, Completed, Credit Card, 2024-01-15`
- Second occurrence: `ORD001, CUST011, Henry Martin, New Delhi, P011, 1, 4999, Completed, Debit Card, 2024-01-25`

**Expected Output:**
- First record: Cleaned (if all other fields valid)
- Second record: Rejected with reason "Duplicate order ID"
- Rejection record in `rejected_records.csv`

**Reason:** Ensures duplicate detection logic works correctly

---

## Test Case 3: Missing Customer Name
**Objective:** Detect and reject records with missing customer names

**Input Condition:**
- Order: `ORD012, CUST012, , Mumbai, P012, 2, 1999, Completed, UPI, 2024-01-26`
- Empty customer_name field

**Expected Output:**
- Record rejected with reason "Missing customer name"
- Saved in `rejected_records.csv`

**Reason:** Validates missing data detection

---

## Test Case 4: Missing City
**Objective:** Detect and reject records with missing city

**Input Condition:**
- Order: `ORD013, CUST013, Victoria Johnson, , P001, 1, 89999, Completed, Credit Card, 2024-01-27`
- Empty city field

**Expected Output:**
- Record rejected with reason "Missing city"
- Saved in `rejected_records.csv`

**Reason:** Validates location data validation

---

## Test Case 5: Invalid Quantity - Zero
**Objective:** Detect and reject orders with zero quantity

**Input Condition:**
- Order: `ORD014, CUST014, frank walker, Bangalore, P002, 0, 2499, Completed, Debit Card, 2024-01-28`
- Quantity: 0

**Expected Output:**
- Record rejected with reason "Invalid quantity (must be positive)"
- Saved in `rejected_records.csv`

**Reason:** Validates business rule that quantity must be positive

---

## Test Case 6: Invalid Quantity - Negative
**Objective:** Detect and reject orders with negative quantity

**Input Condition:**
- Order: `ORD016, CUST016, LUCAS WHITE, Delhi, P004, -2, 15999, Pending, Credit Card, 2024-01-30`
- Quantity: -2

**Expected Output:**
- Record rejected with reason "Invalid quantity (must be positive)"
- Saved in `rejected_records.csv`

**Reason:** Validates negative value rejection

---

## Test Case 7: Invalid Product ID
**Objective:** Detect and reject records with non-existent product IDs

**Input Condition:**
- Order: `ORD100, CUST100, Test Customer, Mumbai, P999, 1, 5000, Completed, UPI, 2024-03-15`
- Product P999 does not exist in product_master.csv

**Expected Output:**
- Record rejected with reason "Product ID not found in master"
- Saved in `rejected_records.csv`

**Reason:** Validates referential integrity with product master

---

## Test Case 8: Invalid Payment Method
**Objective:** Detect and reject invalid payment methods

**Input Condition:**
- Order: `ORD017, CUST017, amelia hall, Kolkata, P005, 1, 24999, Completed, InvalidMethod, 2024-01-31`
- Payment method: "InvalidMethod" (not in valid list)

**Expected Output:**
- Record rejected with reason "Invalid payment method: InvalidMethod"
- Saved in `rejected_records.csv`

**Reason:** Validates payment method is from approved list

---

## Test Case 9: Invalid Order Status
**Objective:** Detect and reject invalid order statuses

**Input Condition:**
- Order: `ORD052, CUST052, AMELIA RODRIGUEZ, Kolkata, P004, 1, 15999, UnknownStatus, Debit Card, 2024-03-06`
- Order status: "UnknownStatus" (not in valid list)

**Expected Output:**
- Record rejected with reason "Invalid order status: UnknownStatus"
- Saved in `rejected_records.csv`

**Reason:** Validates order status is from approved list

---

## Test Case 10: Unit Price Mismatch
**Objective:** Detect and reject records where unit price doesn't match product master

**Input Condition:**
- Order: `ORD027, CUST027, ethan carter, Delhi, P003, 1, 600, Completed, UPI, 2024-02-10`
- Product P003 standard_price: 599
- Order unit_price: 600 (mismatch)

**Expected Output:**
- Record rejected with reason "Unit price mismatch (expected 599, got 600)"
- Saved in `rejected_records.csv`

**Reason:** Validates price integrity with product master

---

## Test Case 11: Invalid Date Format
**Objective:** Detect and reject invalid date formats

**Input Condition:**
- Order: `ORD028, CUST028, Test Customer, Delhi, P004, 1, 15999, Completed, Credit Card, 02/11/2024`
- Date format: "02/11/2024" (not YYYY-MM-DD)

**Expected Output:**
- Record rejected with reason "Invalid date format: 02/11/2024 (expected YYYY-MM-DD)"
- Saved in `rejected_records.csv`

**Reason:** Validates date format compliance

---

## Test Case 12: Revenue Calculation
**Objective:** Verify correct calculation of total_amount

**Input Condition:**
- Valid order with quantity: 5, unit_price: 599
- Calculation: 5 × 599 = 2995

**Expected Output:**
- Cleaned record includes total_amount: 2995
- Verified in cleaned_orders.csv
- Record included in revenue summation in summary_report.txt

**Reason:** Validates mathematical accuracy of financial calculations

---

## Test Case 13: Text Standardization
**Objective:** Verify proper text cleaning and standardization

**Input Condition:**
- Order with customer_name: " Alice Williams " (extra spaces)
- Order with city: "new delhi" (lowercase)
- Order with customer_name: "JAMES miller" (mixed case)

**Expected Output:**
- Cleaned customer_name: "Alice Williams" (spaces trimmed, proper case)
- Cleaned city: "Delhi" (standardized to proper format)
- Cleaned customer_name: "James Miller" (proper case applied)

**Reason:** Validates text normalization logic

---

## Test Case 14: Multiple Rejection Reasons
**Objective:** Verify that multiple issues in a single record are all captured

**Input Condition:**
- Order: `ORD099, CUST099, , , P999, -5, 99999, InvalidStatus, InvalidPayment, invalid-date`
- Missing customer_name AND missing city AND invalid product AND negative quantity AND invalid status AND invalid payment AND invalid date

**Expected Output:**
- Record rejected with ALL reasons listed
- Rejection reason field contains all issues separated by " | "
- Example: "Missing customer name | Missing city | Product ID not found | Invalid quantity | Invalid order status | Invalid payment method | Invalid date format"

**Reason:** Validates comprehensive error reporting

---

## Test Case 15: Rejection Reason Aggregation Report
**Objective:** Verify rejection reasons are properly aggregated in summary report

**Input Condition:**
- Multiple rejected records with various rejection reasons
- Example: 5 records with "Duplicate order ID", 3 records with "Missing customer name", 2 with "Invalid quantity"

**Expected Output:**
- Summary report includes section "DATA QUALITY ISSUES - REJECTION ANALYSIS"
- Shows count of each rejection reason
- Calculates percentage: 5 duplicates out of 10 rejected = 50%
- Output format: "Duplicate order ID: 5 occurrences (50%)"

**Reason:** Validates reporting and aggregation of data quality metrics

---

## Test Case 16: Business Insights Generation
**Objective:** Verify that business insights are generated correctly

**Input Condition:**
- Pipeline processes full dataset with mix of valid and rejected records
- Multiple categories and cities with varying revenue

**Expected Output:**
- Summary report includes section "KEY BUSINESS INSIGHTS"
- At least 3 insights generated:
  1. Data quality insight about rejection rate
  2. Payment method preference insight
  3. Revenue concentration insight
- Insights use actual data with calculated percentages and amounts

**Reason:** Validates business analysis and reporting capability
