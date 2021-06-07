# -*- coding: utf-8 -*-
from . import controllers
from . import models
from odoo import api, SUPERUSER_ID, _


def create_payment_methode_unpaid_invoice(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    companies = env['res.company'].search([])
    for company in companies:
        if company.chart_template_id:
            cash_journal = env['account.journal'].search([('company_id', '=', company.id), ('type', '=', 'cash')], limit=1)
            pos_receivable_account = company.account_default_pos_receivable_account_id
            payment_methods = env['pos.payment.method']
            if cash_journal and (not env['pos.payment.method'].search([('name', '=', 'Unpaid invoice'),('unpaid_invoice', '=', True)])):
                payment_methods = payment_methods.create({
                    'name': _('Unpaid invoice'),
                    'receivable_account_id': pos_receivable_account.id,
                    'is_cash_count': True,
                    'unpaid_invoice': True,
                    'cash_journal_id': cash_journal.id,
                    'company_id': company.id,
                })
                existing_pos_config = env['pos.config'].search([('company_id', '=', company.id)])
                existing_pos_config.write({'payment_method_ids': [(4, payment_methods.id)]})
