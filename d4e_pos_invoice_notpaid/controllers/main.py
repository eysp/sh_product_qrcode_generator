# -*- coding: utf-8 -*-
from odoo import models, http


class AccountMoveController(http.Controller):

    @http.route('/report/isr/<active_ids>', auth='user')
    def report_isr(self, active_ids):
        active_ids = [int(active_id) for active_id in active_ids.split(',')]
        pdf_merge = http.request.env['account.move'].browse(active_ids)._pdf_invoices_with_isr()
        pdf_http_headers = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf_merge))]
        return http.request.make_response(pdf_merge, headers=pdf_http_headers)
