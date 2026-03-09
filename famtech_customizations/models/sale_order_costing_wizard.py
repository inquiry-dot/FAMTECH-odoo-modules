from odoo import models, fields, api

class SaleOrderCostingWizard(models.TransientModel):
    _name = 'sale.order.costing.wizard'
    _description = 'Sale Order Costing Calculator Wizard'

    cost_price = fields.Float("Estimated Cost Price")
    markup_percent = fields.Float("Markup %")
    discount_percent = fields.Float("Discount %")
    computed_price = fields.Float("Computed Selling Price", compute="_compute_computed_price")

    @api.depends('cost_price', 'markup_percent', 'discount_percent')
    def _compute_computed_price(self):
        for rec in self:
            base = rec.cost_price * (1 + rec.markup_percent / 100)
            rec.computed_price = base * (1 - rec.discount_percent / 100)

    def apply_to_order(self):
        """Apply the values back to the current sale order"""
        active_id = self.env.context.get('active_id')
        if active_id:
            order = self.env['sale.order'].browse(active_id)
            order.write({
                'cost_price': self.cost_price,
                'markup_percent': self.markup_percent,
                'discount_percent': self.discount_percent,
            })