from odoo import http
from odoo.http import request

class PaymentReturn(http.Controller):
    @http.route('/payment/famtech/return', type='http', auth='public', website=True)
    def famtech_return(self, **post):
        ref = post.get('reference')
        tx = request.env['payment.transaction'].sudo().search([('acquirer_reference','=',ref)], limit=1)
        if tx and tx.state == 'done':
            # Choose appointment type id programmatically or embed in order metadata
            return request.redirect('/calendar/booking?appointment_type=3')
        return request.redirect('/shop/confirmation')