# -*- coding: utf-8 -*-
from odoo import models
from odoo.tools import pdf


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _pdf_invoices_with_isr(self):
        pdf_docs = []
        actions = [
            self.env.ref('account.account_invoices'),
            self.env.ref('l10n_ch.l10n_ch_isr_report'),
        ]
        for invoice in self:
            pdf_data = actions[0].render_qweb_pdf(invoice.id)[0]
            pdf_docs.append(pdf_data)
            if invoice.l10n_ch_isr_valid:
                invoice.l10n_ch_isr_sent = True
                isr_data = actions[1].render_qweb_pdf(invoice.id)[0]
                pdf_docs.append(isr_data)
        pdf_merge = pdf.merge_pdf(pdf_docs)
        return pdf_merge
