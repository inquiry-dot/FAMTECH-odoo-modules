from odoo import http
from odoo.http import request

class FamtechPaymentController(http.Controller):
    @http.route(['/shop/payment/transaction/feedback'], type='http', auth='public', methods=['GET','POST'], website=True)
    def payment_feedback(self, **post):
        # This is example; use the acquirer's feedback route or payment.transaction entries
        order = request.website.sale_get_order()
        if order:
            # example set custom field from payment provider
            order.sudo().write({'x_payment_method': post.get('acquirer') or 'online'})
        return request.redirect('/shop/confirmation')