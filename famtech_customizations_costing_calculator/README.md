# FamTech Sales Customizations - Costing Calculator Module

## Overview

This Odoo 18.0 custom module adds an embedded costing calculator to Sales Quotations, enabling sales staff to compute cost breakdowns, margins, and profitability before finalizing deals.

## Features

- **Real-time Cost Calculation**: Automatically computes selling price based on cost, markup, and discount
- **Margin Analysis**: Displays profit margins in both currency and percentage
- **Modal Calculator**: Clean, user-friendly interface accessible from quotation form
- **PDF Export**: Costing breakdown automatically included in quotation reports
- **Validation**: Built-in checks to prevent invalid percentage values

## Module Structure

```
famtech_customizations/
├── __init__.py                          # Module initialization
├── __manifest__.py                      # Module manifest and dependencies
├── models/
│   ├── __init__.py                      # Models initialization
│   └── sale_order.py                    # Extended Sale Order model with costing logic
├── views/
│   ├── sale_order_view.xml              # Main form view with calculator button
│   └── sale_order_costing_view.xml      # Calculator modal view
├── reports/
│   └── sale_order_report.xml            # Enhanced quotation report template
└── security/
    └── ir.model.access.csv              # Access rights configuration
```

## Installation Instructions

### 1. Copy Module to Addons Directory

```bash
# Copy the famtech_customizations folder to your Odoo addons directory
cp -r famtech_customizations /path/to/odoo/addons/
```

### 2. Update Addons Path (if needed)

Ensure your `odoo.conf` includes the addons path:

```ini
[options]
addons_path = /path/to/odoo/addons,/path/to/custom/addons
```

### 3. Restart Odoo Server

```bash
# Stop Odoo
sudo systemctl stop odoo

# Or if running manually:
pkill -f odoo-bin

# Start Odoo with update flag
./odoo-bin -c /path/to/odoo.conf --dev all

# Or with systemctl:
sudo systemctl start odoo
```

### 4. Update Apps List

1. Log into Odoo as Administrator
2. Go to **Apps** menu
3. Click **Update Apps List** (you may need to activate Developer Mode first)
4. Search for "FamTech Sales Customizations"
5. Click **Install**

### 5. Verify Installation

1. Go to **Sales → Orders → Quotations**
2. Open any quotation or create a new one
3. You should see the **"Costing Calculator"** button in the header
4. You should see a new **"Costing Summary"** tab

## How to Use

### Opening the Calculator

1. Navigate to a Sales Order/Quotation
2. Click the **"Costing Calculator"** button in the header
3. A modal window will open with input fields

### Entering Cost Data

In the calculator modal:

1. **Estimated Cost Price**: Enter your total cost (e.g., ₱5,000)
2. **Markup %**: Enter markup percentage (e.g., 20 for 20%)
3. **Discount %**: Enter discount percentage (e.g., 10 for 10%)

The computed results update automatically:
- **Computed Selling Price**: Final price after markup and discount
- **Margin Amount**: Profit in currency
- **Margin Percentage**: Profit as percentage of selling price

### Calculation Formula

```
Step 1: Base Price = Cost Price × (1 + Markup%/100)
Step 2: Selling Price = Base Price × (1 - Discount%/100)
Step 3: Margin = Selling Price - Cost Price
Step 4: Margin % = (Margin / Selling Price) × 100
```

### Viewing in Reports

1. After saving costing data, generate the quotation PDF
2. The costing breakdown appears in a dedicated section
3. Shows: Cost Price, Markup, Discount, Computed Price, and Margins

## Testing Scenarios

### Test Case 1: Basic Markup
- **Cost**: ₱5,000
- **Markup**: 20%
- **Discount**: 0%
- **Expected Result**: ₱6,000
- **Expected Margin**: ₱1,000 (16.67%)

### Test Case 2: Markup with Discount
- **Cost**: ₱10,000
- **Markup**: 30%
- **Discount**: 10%
- **Expected Result**: ₱11,700
- **Expected Margin**: ₱1,700 (14.53%)

### Test Case 3: High Markup, High Discount
- **Cost**: ₱8,000
- **Markup**: 50%
- **Discount**: 25%
- **Expected Result**: ₱9,000
- **Expected Margin**: ₱1,000 (11.11%)

### Test Case 4: Zero Markup
- **Cost**: ₱3,000
- **Markup**: 0%
- **Discount**: 5%
- **Expected Result**: ₱2,850
- **Expected Margin**: -₱150 (-5.26%)

## Validation Rules

- Markup percentage cannot be negative
- Discount percentage must be between 0 and 100
- Cost price should be non-negative
- Invalid values will show error messages

## Git Workflow

### Initial Setup

```bash
# Navigate to your Odoo addons directory
cd /path/to/odoo/addons

# Initialize git repository (if not already done)
git init

# Create feature branch
git checkout -b feature/quotation-costing-calculator
```

### Stage and Commit Changes

```bash
# Add all module files
git add famtech_customizations/__init__.py
git add famtech_customizations/__manifest__.py
git add famtech_customizations/models/__init__.py
git add famtech_customizations/models/sale_order.py
git add famtech_customizations/views/sale_order_view.xml
git add famtech_customizations/views/sale_order_costing_view.xml
git add famtech_customizations/reports/sale_order_report.xml
git add famtech_customizations/security/ir.model.access.csv

# Or add everything at once:
git add famtech_customizations/

# Commit with descriptive message
git commit -m "Add costing calculator feature to Sales Quotations

- Extended sale.order model with cost, markup, discount fields
- Added computed price and margin calculations
- Created calculator modal view with real-time updates
- Enhanced quotation reports with costing breakdown
- Implemented validation for percentage inputs
- Added comprehensive documentation"
```

### Push to Repository

```bash
# Push to remote repository
git push origin feature/quotation-costing-calculator
```

### Create Merge/Pull Request

1. Go to your Git repository (GitHub, GitLab, Bitbucket, etc.)
2. Create a new Pull Request/Merge Request
3. Set source: `feature/quotation-costing-calculator`
4. Set target: `main` or `develop`
5. Add description and screenshots
6. Request review from team lead

## Troubleshooting

### Module Not Appearing in Apps List

- Ensure module is in correct addons path
- Check `odoo.conf` addons_path configuration
- Update Apps List with Developer Mode enabled
- Check Odoo logs for import errors

### Calculator Button Not Visible

- Verify module is installed and upgraded
- Check user has Sales / User permissions
- Refresh browser cache (Ctrl+F5)
- Check if quotation is in 'cancelled' state (button is hidden)

### Computed Price Not Updating

- Ensure all fields are saved
- Check browser console for JavaScript errors
- Try reopening the quotation
- Upgrade the module: `Apps → FamTech Sales → Upgrade`

### Report Not Showing Costing Data

- Verify cost_price > 0
- Check report template inheritance
- Regenerate the PDF report
- Check if report XML is properly loaded

## Upgrade Instructions

If you modify the module after installation:

```bash
# From Odoo shell or command line:
./odoo-bin -c odoo.conf -u famtech_customizations -d your_database_name

# Or from the UI:
# Apps → FamTech Sales Customizations → Upgrade
```

## Dependencies

- `sale`: Core Sales module
- `sale_management`: Sales Management features

## Compatibility

- Odoo Version: 18.0
- Python: 3.10+
- Tested on: Ubuntu 22.04, Odoo 18.0 Community/Enterprise

## Support

For issues or questions:
- Check Odoo logs: `/var/log/odoo/odoo-server.log`
- Enable Developer Mode for detailed error messages
- Reference: https://www.odoo.com/documentation/18.0/developer.html

## License

LGPL-3

## Author

FamTech Development Team
