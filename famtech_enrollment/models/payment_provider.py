from odoo import models, fields

class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('cash_manual', 'Cash Manual')])