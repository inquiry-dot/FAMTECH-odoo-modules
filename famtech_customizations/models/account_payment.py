from odoo import models

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def action_post(self):
        res = super(AccountPayment, self).action_post()
        
        for payment in self:
            for invoice in payment.reconciled_invoice_ids:
                
                # Skip if flagged
                if invoice.no_send_to_customer:
                    continue

                # Ensure invoice is posted
                if invoice.state != 'posted':
                    continue

                # Send Invoice (Custom Attached Template)
                template_invoice = self.env.ref(
                    'famtech_customizations.email_template_custom_invoice',
                    raise_if_not_found=False
                )
                if template_invoice:
                    template_invoice.send_mail(invoice.id, force_send=True)

                # Send Collection Receipt (Attached BIR Template)
                template_receipt = self.env.ref(
                    'famtech_customizations.email_template_collection_receipt',
                    raise_if_not_found=False
                )
                if template_receipt:
                    template_receipt.send_mail(invoice.id, force_send=True)

        return res