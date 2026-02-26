from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    no_send_to_customer = fields.Boolean(
        string="Do Not Send to Customer",
        default=False,
        help="Enable this to prevent auto-emailing invoice to customer."
    )