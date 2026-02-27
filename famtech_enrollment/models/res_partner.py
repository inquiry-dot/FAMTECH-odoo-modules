from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'
    x_famtech_points = fields.Integer(string='FAMTECH Points', default=0)
    x_last_points_earned = fields.Integer(string='Last Points Earned', default=0)