from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    first_name = fields.Char(
        string="First Name",
        compute="_compute_first_name",
        store=True
    )

    @api.depends('name')
    def _compute_first_name(self):
        for partner in self:
            if partner.name:
                partner.first_name = partner.name.split(' ')[0]
            else:
                partner.first_name = ''