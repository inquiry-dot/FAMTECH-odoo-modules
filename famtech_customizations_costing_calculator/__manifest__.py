# -*- coding: utf-8 -*-
{
    'name': 'FamTech Sales Costing Calculator',
    'version': '18.0.1.0.6',
    'category': 'Sales',
    'summary': 'Custom costing calculator and enhancements for Sales module',
    'description': """
        FamTech Sales Customizations
        ==============================
        * Embedded costing calculator in quotations
        * Real-time margin and profitability calculations
        * Cost breakdown in quotation reports
    """,
    'author': 'FamTech',
    'website': 'https://www.famtech.com',
    'depends': [
        'sale',
        'sale_management',
    ],
    'data': [
        'views/sale_order_view.xml',
        'views/sale_order_costing_view.xml',
        'reports/sale_order_report.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
