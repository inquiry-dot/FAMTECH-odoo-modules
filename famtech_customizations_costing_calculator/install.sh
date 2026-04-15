#!/bin/bash

###############################################################################
# FamTech Sales Customizations - Installation Script
# 
# This script helps automate the installation of the costing calculator module
# for Odoo 18.0
#
# Usage: ./install.sh [odoo-addons-path]
# Example: ./install.sh /opt/odoo/addons
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo "=============================================="
    echo "$1"
    echo "=============================================="
    echo ""
}

# Check if running as root (optional, depends on your setup)
check_permissions() {
    if [ "$EUID" -eq 0 ]; then
        print_warning "Running as root. Make sure file permissions are set correctly."
    fi
}

# Validate Odoo addons path
validate_addons_path() {
    local addons_path=$1
    
    if [ -z "$addons_path" ]; then
        print_error "Addons path not provided!"
        echo "Usage: $0 <odoo-addons-path>"
        echo "Example: $0 /opt/odoo/addons"
        exit 1
    fi
    
    if [ ! -d "$addons_path" ]; then
        print_error "Addons path does not exist: $addons_path"
        exit 1
    fi
    
    print_info "Using addons path: $addons_path"
}

# Copy module files
copy_module() {
    local addons_path=$1
    local module_name="famtech_customizations"
    local target_path="$addons_path/$module_name"
    
    print_header "Copying Module Files"
    
    # Check if module already exists
    if [ -d "$target_path" ]; then
        print_warning "Module already exists at $target_path"
        read -p "Overwrite? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Installation cancelled."
            exit 0
        fi
        print_info "Removing existing module..."
        rm -rf "$target_path"
    fi
    
    # Copy module
    print_info "Copying module to $target_path..."
    cp -r "$module_name" "$target_path"
    
    if [ $? -eq 0 ]; then
        print_info "Module files copied successfully!"
    else
        print_error "Failed to copy module files."
        exit 1
    fi
}

# Set proper permissions
set_permissions() {
    local target_path=$1
    
    print_header "Setting Permissions"
    
    print_info "Setting file permissions..."
    find "$target_path" -type f -exec chmod 644 {} \;
    find "$target_path" -type d -exec chmod 755 {} \;
    
    print_info "Permissions set successfully!"
}

# Validate module structure
validate_module() {
    local target_path=$1
    
    print_header "Validating Module Structure"
    
    local required_files=(
        "__init__.py"
        "__manifest__.py"
        "models/__init__.py"
        "models/sale_order.py"
        "views/sale_order_view.xml"
        "views/sale_order_costing_view.xml"
        "reports/sale_order_report.xml"
        "security/ir.model.access.csv"
    )
    
    local all_valid=true
    
    for file in "${required_files[@]}"; do
        if [ -f "$target_path/$file" ]; then
            print_info "✓ $file"
        else
            print_error "✗ $file (MISSING)"
            all_valid=false
        fi
    done
    
    if [ "$all_valid" = true ]; then
        print_info "All required files are present!"
    else
        print_error "Some required files are missing!"
        exit 1
    fi
}

# Print next steps
print_next_steps() {
    print_header "Installation Complete!"
    
    echo "Next steps:"
    echo ""
    echo "1. Restart Odoo server:"
    echo "   sudo systemctl restart odoo"
    echo "   OR"
    echo "   pkill -f odoo-bin && ./odoo-bin -c odoo.conf"
    echo ""
    echo "2. Update Apps List:"
    echo "   - Log into Odoo as Administrator"
    echo "   - Go to Apps menu"
    echo "   - Click 'Update Apps List'"
    echo "   - Search for 'FamTech Sales Customizations'"
    echo "   - Click 'Install'"
    echo ""
    echo "3. Test the module:"
    echo "   - Go to Sales → Quotations"
    echo "   - Open or create a quotation"
    echo "   - Click 'Costing Calculator' button"
    echo ""
    echo "4. Refer to README.md for detailed usage instructions"
    echo ""
    print_info "Installation script completed successfully!"
}

# Main installation flow
main() {
    print_header "FamTech Sales Customizations - Installation"
    
    # Get addons path from argument or prompt
    local addons_path=$1
    
    if [ -z "$addons_path" ]; then
        read -p "Enter Odoo addons path (e.g., /opt/odoo/addons): " addons_path
    fi
    
    # Run installation steps
    check_permissions
    validate_addons_path "$addons_path"
    copy_module "$addons_path"
    set_permissions "$addons_path/famtech_customizations"
    validate_module "$addons_path/famtech_customizations"
    print_next_steps
}

# Run main function
main "$@"
