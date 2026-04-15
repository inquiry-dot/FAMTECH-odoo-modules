# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Costing Calculator Fields
    cost_price = fields.Float(
        string="Estimated Cost Price",
        help="Total estimated cost for this quotation",
        digits='Product Price',
    )
    markup_percent = fields.Float(
        string="Markup %",
        help="Markup percentage to apply on cost price",
        default=0.0,
    )
    discount_percent = fields.Float(
        string="Discount %",
        help="Discount percentage to apply on marked-up price",
        default=0.0,
    )
    computed_price = fields.Float(
        string="Computed Selling Price",
        compute="_compute_computed_price",
        store=True,
        digits='Product Price',
        help="Automatically calculated selling price based on cost, markup, and discount",
    )
    margin_amount = fields.Float(
        string="Margin Amount",
        compute="_compute_margin_metrics",
        store=True,
        digits='Product Price',
        help="Profit margin in currency",
    )
    margin_percent = fields.Float(
        string="Margin %",
        compute="_compute_margin_metrics",
        store=True,
        digits='Product Price',
        help="Profit margin percentage",
    )

    @api.depends('cost_price', 'markup_percent', 'discount_percent')
    def _compute_computed_price(self):
        """Calculate the final selling price based on cost, markup, and discount."""
        for order in self:
            if order.cost_price >= 0:
                # Apply markup to cost price
                base_price = order.cost_price * (1 + (order.markup_percent / 100.0))
                # Apply discount to marked-up price
                discounted = base_price * (1 - (order.discount_percent / 100.0))
                order.computed_price = discounted
            else:
                order.computed_price = 0.0

    @api.depends('cost_price', 'computed_price')
    def _compute_margin_metrics(self):
        """Calculate margin amount and percentage."""
        for order in self:
            if order.computed_price > 0 and order.cost_price >= 0:
                order.margin_amount = order.computed_price - order.cost_price
                order.margin_percent = (order.margin_amount / order.computed_price) * 100.0
            else:
                order.margin_amount = 0.0
                order.margin_percent = 0.0

    @api.constrains('markup_percent', 'discount_percent')
    def _check_percentages(self):
        """Validate that percentages are within reasonable ranges."""
        for order in self:
            if order.markup_percent < 0:
                raise ValidationError("Markup percentage cannot be negative.")
            if order.discount_percent < 0 or order.discount_percent > 100:
                raise ValidationError("Discount percentage must be between 0 and 100.")

    def action_open_costing_calculator(self):
        """Open the costing calculator modal."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quotation Costing Calculator',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
            'views': [(self.env.ref('famtech_customizations_costing_calculator.view_order_costing_form').id, 'form')],
            'context': dict(self.env.context, form_view_initial_mode='edit'),
        }

    def action_save_costing(self):
        """Save costing data and close modal."""
        self.ensure_one()
        # The values are automatically saved by the ORM when the form is submitted
        # Just return an action to close the modal
        return {'type': 'ir.actions.act_window_close'}

    def action_apply_computed_price(self):
        """Apply the computed price to order lines proportionally."""
        self.ensure_one()
        if not self.order_line:
            raise ValidationError("Cannot apply computed price to an order with no lines.")
        
        # This is a helper action that could distribute the computed price
        # across order lines if needed
        return True
