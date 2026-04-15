# Quick Start Guide

## Installation (5 minutes)

### Option 1: Automated Installation
```bash
cd /path/to/downloaded/files
chmod +x install.sh
./install.sh /opt/odoo/addons
```

### Option 2: Manual Installation
```bash
# Copy module to Odoo addons directory
cp -r famtech_customizations /opt/odoo/addons/

# Restart Odoo
sudo systemctl restart odoo
```

## Activate Module (2 minutes)

1. Open Odoo in browser
2. Go to **Apps** menu
3. Click **Update Apps List** (enable Developer Mode if needed)
4. Search: "FamTech"
5. Click **Install**

## First Use (1 minute)

1. Navigate to **Sales → Quotations**
2. Open any quotation or create new one
3. Click **"Costing Calculator"** button in header
4. Enter:
   - Cost: 5000
   - Markup: 20
   - Discount: 0
5. See computed price: 6000
6. Click **Save & Close**
7. Generate PDF → see costing breakdown

## That's it! 🎉

For detailed information, see:
- `README.md` - Full documentation
- `TESTING_CHECKLIST.md` - Testing guide
- `CHANGELOG.md` - Version history

## Common Issues

**Module not appearing?**
- Check addons path in odoo.conf
- Restart Odoo server
- Enable Developer Mode

**Button not visible?**
- Verify module is installed
- Check user permissions (needs Sales/User role)
- Hard refresh browser (Ctrl+F5)

**Calculations wrong?**
- Formula: Base = Cost × (1 + Markup/100)
- Then: Final = Base × (1 - Discount/100)
- Verify your input values

## Support

Check the detailed README.md for troubleshooting, or:
- Review Odoo logs: `/var/log/odoo/odoo-server.log`
- Enable Developer Mode for detailed errors
- Reference: https://www.odoo.com/documentation/18.0/developer.html
