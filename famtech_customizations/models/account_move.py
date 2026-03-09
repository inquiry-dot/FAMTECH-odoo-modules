from odoo import models, fields, api
from datetime import date, timedelta

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _cron_send_invoice_reminders(self):
        """
        Executed daily via cron to send automated reminders for:
        - 3 days before due date (Gentle)
        - 1 day overdue (Overdue with callback)
        """
        today = date.today()
        
        # logic for 3 days before due date
        reminder_date = today + timedelta(days=3)
        upcoming_invoices = self.search([
            ('state', '=', 'posted'),
            ('payment_state', 'not in', ('paid', 'in_payment')),
            ('move_type', '=', 'out_invoice'),
            ('invoice_date_due', '=', reminder_date)
        ])
        template_gentle = self.env.ref('famtech_customizations.email_template_invoice_reminder_gentle', raise_if_not_found=False)
        if template_gentle:
            for inv in upcoming_invoices:
                inv.message_post_with_source(template_gentle)

        # logic for 1 day overdue
        overdue_date = today - timedelta(days=1)
        overdue_invoices = self.search([
            ('state', '=', 'posted'),
            ('payment_state', 'not in', ('paid', 'in_payment')),
            ('move_type', '=', 'out_invoice'),
            ('invoice_date_due', '=', overdue_date)
        ])
        template_overdue = self.env.ref('famtech_customizations.email_template_invoice_reminder_overdue', raise_if_not_found=False)
        if template_overdue:
            for inv in overdue_invoices:
                inv.message_post_with_source(template_overdue)
