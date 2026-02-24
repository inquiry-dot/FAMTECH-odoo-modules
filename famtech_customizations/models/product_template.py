from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    brochure_url = fields.Char(string="Brochure URL")