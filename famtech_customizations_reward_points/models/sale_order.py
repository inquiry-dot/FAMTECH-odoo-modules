from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    points_to_earn = fields.Integer(
        string="Points to Earn",
        compute="_compute_points_to_earn",
        store=True
    )

    @api.depends('amount_total')
    def _compute_points_to_earn(self):
        for order in self:
            rate = 100  # 1 point per 100 pesos
            order.points_to_earn = int(order.amount_total // rate)