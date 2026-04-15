# Architecture Documentation

## Module Structure Overview

```
famtech_customizations/
│
├── Core Files
│   ├── __init__.py                  → Module entry point
│   └── __manifest__.py              → Module metadata, dependencies, data files
│
├── models/                          → Business Logic Layer
│   ├── __init__.py                  → Models initialization
│   └── sale_order.py                → Extended Sale Order model
│       ├── Fields:
│       │   ├── cost_price           (Float)
│       │   ├── markup_percent       (Float)
│       │   ├── discount_percent     (Float)
│       │   ├── computed_price       (Float, Computed)
│       │   ├── margin_amount        (Float, Computed)
│       │   └── margin_percent       (Float, Computed)
│       ├── Methods:
│       │   ├── _compute_computed_price()      → Calculate selling price
│       │   ├── _compute_margin_metrics()      → Calculate margins
│       │   ├── _check_percentages()           → Validate inputs
│       │   └── action_open_costing_calculator() → Open modal
│
├── views/                           → User Interface Layer
│   ├── sale_order_view.xml         → Main form enhancement
│   │   ├── Adds button to header
│   │   └── Adds "Costing Summary" tab
│   └── sale_order_costing_view.xml → Calculator modal
│       ├── Input fields for cost, markup, discount
│       ├── Display computed results
│       └── Help text and examples
│
├── reports/                         → Reporting Layer
│   └── sale_order_report.xml       → PDF template extension
│       └── Adds costing breakdown section
│
├── security/                        → Access Control
│   └── ir.model.access.csv         → User permissions
│
└── Documentation
    ├── README.md                    → Full documentation
    ├── QUICKSTART.md                → Quick start guide
    ├── TESTING_CHECKLIST.md         → Test cases
    ├── CHANGELOG.md                 → Version history
    └── install.sh                   → Automated installer
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERACTION                        │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  1. Click "Costing Calculator" Button                       │
│     (sale_order_view.xml)                                   │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  2. Trigger action_open_costing_calculator()                │
│     (sale_order.py)                                         │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Open Modal Calculator                                   │
│     (sale_order_costing_view.xml)                           │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  4. User Enters Values:                                     │
│     - Cost Price: 10,000                                    │
│     - Markup: 30%                                           │
│     - Discount: 10%                                         │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  5. Real-time Computation (@api.depends)                    │
│     ┌─────────────────────────────────────────────┐        │
│     │  _compute_computed_price():                 │        │
│     │  base = 10,000 × (1 + 30/100) = 13,000     │        │
│     │  final = 13,000 × (1 - 10/100) = 11,700    │        │
│     └─────────────────────────────────────────────┘        │
│     ┌─────────────────────────────────────────────┐        │
│     │  _compute_margin_metrics():                 │        │
│     │  margin = 11,700 - 10,000 = 1,700          │        │
│     │  margin% = (1,700/11,700) × 100 = 14.53%   │        │
│     └─────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  6. Display Results in Modal                                │
│     - Computed Price: ₱11,700                               │
│     - Margin: ₱1,700 (14.53%)                               │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  7. User Clicks "Save & Close"                              │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  8. Data Persisted to Database                              │
│     (sale_order table)                                      │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  9. Generate PDF Report                                     │
│     (sale_order_report.xml)                                 │
│     → Includes costing breakdown section                    │
└─────────────────────────────────────────────────────────────┘
```

## Calculation Logic

### Step-by-Step Calculation

```python
# Given inputs:
cost_price = 10,000
markup_percent = 30
discount_percent = 10

# Step 1: Calculate base price with markup
base_price = cost_price × (1 + (markup_percent / 100))
base_price = 10,000 × (1 + (30 / 100))
base_price = 10,000 × 1.30
base_price = 13,000

# Step 2: Apply discount to get final price
computed_price = base_price × (1 - (discount_percent / 100))
computed_price = 13,000 × (1 - (10 / 100))
computed_price = 13,000 × 0.90
computed_price = 11,700

# Step 3: Calculate margin metrics
margin_amount = computed_price - cost_price
margin_amount = 11,700 - 10,000
margin_amount = 1,700

margin_percent = (margin_amount / computed_price) × 100
margin_percent = (1,700 / 11,700) × 100
margin_percent = 14.53%
```

## Database Schema

### Extended Fields in sale_order Table

| Field Name        | Type    | Stored | Computed | Description                    |
|-------------------|---------|--------|----------|--------------------------------|
| cost_price        | Float   | Yes    | No       | Estimated cost price           |
| markup_percent    | Float   | Yes    | No       | Markup percentage              |
| discount_percent  | Float   | Yes    | No       | Discount percentage            |
| computed_price    | Float   | Yes    | Yes      | Final calculated selling price |
| margin_amount     | Float   | Yes    | Yes      | Profit margin in currency      |
| margin_percent    | Float   | Yes    | Yes      | Profit margin percentage       |

### Computed Field Dependencies

```
cost_price ─┐
            ├─→ computed_price ─┐
markup_percent ─┘                 ├─→ margin_amount
                                  │
discount_percent ──────────────┘  └─→ margin_percent
```

## View Inheritance Structure

```
sale.view_order_form (Base Odoo View)
    │
    ├── Header
    │   └── [NEW] Costing Calculator Button
    │
    └── Notebook
        └── [NEW] Costing Summary Tab
            ├── Cost Breakdown Group
            └── Computed Results Group

sale.order (Base Model) → [NEW] view_order_costing_form (Modal)
    └── Calculator Interface
        ├── Input Group
        └── Results Group
```

## Report Template Structure

```
sale.report_saleorder_document (Base Template)
    │
    ├── Order Lines
    ├── Totals
    ├── Terms & Conditions
    │
    └── [NEW] Costing Breakdown Section
        ├── Cost Information Table
        ├── Results Table
        └── Disclaimer Text
```

## Security Model

| Model      | Group                        | Read | Write | Create | Delete |
|------------|------------------------------|------|-------|--------|--------|
| sale.order | sales_team.group_sale_salesman | ✓    | ✓     | ✓      | ✓      |
| sale.order | sales_team.group_sale_manager  | ✓    | ✓     | ✓      | ✓      |

## API Dependencies

### Python Dependencies
- `odoo.models` - Base model classes
- `odoo.fields` - Field types
- `odoo.api` - Decorators (depends, constrains)
- `odoo.exceptions` - ValidationError

### Odoo Module Dependencies
- `sale` - Core Sales module
- `sale_management` - Sales Management features

### XML Namespaces
- Standard Odoo XML structure
- QWeb templating for reports

## Performance Considerations

### Computed Fields
- All computed fields are **stored** (store=True)
- Reduces database queries on each read
- Automatic recalculation on dependency change

### View Loading
- Minimal view inheritance overhead
- Modal loads on-demand (not preloaded)

### Report Generation
- Conditional rendering (only when cost_price > 0)
- No additional queries needed (uses existing fields)

## Extension Points

Future enhancements can build on:

1. **Model Methods**: Add new calculation methods
2. **View Extensions**: Add more UI elements
3. **Report Sections**: Additional costing details
4. **Wizards**: Batch operations on multiple orders
5. **Scheduled Actions**: Automated costing updates
6. **Custom Controllers**: Web API endpoints

## Integration Points

Can integrate with:

- Purchase module (automatic cost updates)
- Product module (default cost values)
- Accounting module (profit tracking)
- Inventory module (actual cost comparison)
- CRM module (costing in opportunities)
