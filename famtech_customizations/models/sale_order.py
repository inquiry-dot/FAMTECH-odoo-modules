def action_open_costing_calculator(self):
    return {
        'type': 'ir.actions.act_window',
        'name': 'Costing Calculator',
        'res_model': 'sale.order.costing.wizard',
        'view_mode': 'form',
        'target': 'new',
        'context': {'default_cost_price': self.cost_price,
                    'default_markup_percent': self.markup_percent,
                    'default_discount_percent': self.discount_percent,
                    'active_id': self.id},
    }