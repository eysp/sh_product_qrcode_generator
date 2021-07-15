# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountReconcileModel(models.Model):
    _inherit = 'account.reconcile.model'

    match_text_location_note = fields.Boolean(
        default=True,
        help="Search in the Statement's Note to find the Invoice/Payment's reference",
    )
    match_text_location_reference = fields.Boolean(
        default=True,
        help="Search in the Statement's Reference to find the Invoice/Payment's reference",
    )


class AccountMove(models.Model):
    _inherit = 'account.move'

    internal_reference = fields.Char(string='Internal Reference')


class AccountChartTemplate(models.Model):

    _inherit = 'account.chart.template'


    def generate_account_reconcile_model(self, tax_template_ref, acc_template_ref, company):
        res = super().generate_account_reconcile_model(acc_template_ref, acc_template_ref, company)
        return res

    def generate_account_reconcile_model(self, tax_template_ref, acc_template_ref, company):
        """ This method creates account reconcile models

        :param tax_template_ref: Taxes templates reference for write taxes_id in account_account.
        :param acc_template_ref: dictionary with the mapping between the account templates and the real accounts.
        :param company_id: company to create models for
        :returns: return new_account_reconcile_model for reference purpose.
        :rtype: dict
        """
        self.ensure_one()
        account_reconcile_models = self.env['account.reconcile.model.template'].search([
            ('chart_template_id', '=', self.id)
        ])
        for account_reconcile_model in account_reconcile_models:
            vals = self._prepare_reconcile_model_vals(company, account_reconcile_model, acc_template_ref, tax_template_ref)
            self.create_record_with_xmlid(company, account_reconcile_model, 'account.reconcile.model', vals)
        # Create a default rule for the reconciliation widget matching invoices automatically.
        self.env['account.reconcile.model'].sudo().create({
            "name": _('Invoices Matching Rule'),
            "sequence": '1',
            "rule_type": 'invoice_matching',
            "auto_reconcile": False,
            "match_nature": 'both',
            "match_same_currency": True,
            "match_total_amount": True,
            "match_total_amount_param": 100,
            "match_partner": True,
            "company_id": company.id,
        })
        return True