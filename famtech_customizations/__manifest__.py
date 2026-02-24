{
    'name': 'FAMTECH Customizations',
    'version': '1.0',
    'summary': 'Custom modules for FAMTECH',
    'depends': ['mail', 'sale_management', 'account', 'stock'],
    'data': [
        'data/mail_templates_firstname.xml',
        "views/quotation_report.xml",
        "views/invoice_report.xml",
        "views/payment_receipt_report.xml",
        "views/delivery_report.xml",
    ],
    'installable': True,
    'application': False,
}