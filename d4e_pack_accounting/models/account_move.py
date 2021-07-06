# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    update_sequence = fields.Char(string='Update sequence')

    def action_subtotal(self):
        for l in self.invoice_line_ids:
            if l.new_line:
                res = l.unlink()
        subtotal = 0
        section_1 = False
        section_2 = False
        seq = 0
        invoice_line_ids = self.env["account.move.line"].search([
            ('move_id', '=', self.id),
            ('exclude_from_invoice_tab', '=', False), ('display_type', '!=', 'line_subtotal')], order="sequence")
        for line in invoice_line_ids:
            if line.display_type == 'line_section':
                section_1 = True
            if line.display_type == 'line_section' and subtotal:
                section_2 = True
            if not line.display_type and section_1:
                subtotal += line.price_subtotal
            if section_2 and subtotal != 0:
                line_vals_list = {
                  'sequence': line.sequence - 1,
                  'name': _('Sub-Total:    ') + str("%.2f" % subtotal)+' '+line.currency_id.symbol,
                  'currency_id': line.currency_id.symbol,
                  'quantity': 1,
                  'currency_id': 5,
                  'tax_exigible': True,
                  'display_type': 'line_sub_total',
                  'new_line': True,
                  'move_id': self.id
                }
                new_line = self.env['account.move.line'].create(line_vals_list)
                subtotal = 0
                section_2 = False
            seq = line.sequence
        if subtotal != 0:
            line_vals_list = {
              'sequence': seq,
              'name': _('Sub-Total:      ')+str("%.2f" % subtotal)+' '+line.currency_id.symbol,
              'currency_id': line.currency_id.symbol,
              'quantity': 1,
              'currency_id': 5,
              'tax_exigible': True,
              'display_type': 'line_sub_total',
              'new_line': True,
              'move_id': self.id
            }
            new_line = self.env['account.move.line'].with_context(request_from_action_subtotal=True).create(line_vals_list)

    def add_subtotal(self):
        subtotal = 0
        seq = 0
        invoice_line_ids = self.env["account.move.line"].search([
            ('move_id', '=', self.id),
            ('exclude_from_invoice_tab', '=', False)], order="sequence")
        for line in invoice_line_ids:
            if not line.display_type:
                subtotal += line.price_subtotal
            if line.display_type == 'line_subtotal':
                seq = line.sequence
                line_vals_list = {
                    'sequence': seq,
                    'name': _('Sub-Total-manuel:      ')+str("%.2f" % subtotal) + ' ' + line.currency_id.symbol,
                    'currency_id': line.currency_id.symbol,
                    'quantity': 1,
                    'currency_id': 5,
                    'tax_exigible': True,
                    'display_type': 'line_subtotal',
                    'new_line': False,
                    'move_id': self.id
                }
                new_line = line.write(
                    line_vals_list)
                subtotal = 0

    def action_subtotal_create(self):
        for l in self.invoice_line_ids:
            if l.new_line:
                res = l.unlink()
        subtotal = 0
        section_1 = False
        section_2 = False
        seq = 0
        invoice_line_ids = self.env["account.move.line"].search([
            ('move_id', '=', self.id),
            ('exclude_from_invoice_tab', '=', False)])
        line_index = 1
        for line in invoice_line_ids:
            line.sequence = line_index
            line_index += 1
            if line.display_type == 'line_section':
                section_1 = True
            if line.display_type == 'line_section' and subtotal:
                section_2 = True
            if not line.display_type and section_1:
                subtotal += line.price_subtotal
            if section_2 and subtotal != 0:
                increment_sequence_invoice_line_ids = self.env["account.move.line"].search([
                    ('move_id', '=', self.id),
                    ('sequence', '>=', line.sequence),
                    ('exclude_from_invoice_tab', '=', False)], order="sequence DESC")
                for element in increment_sequence_invoice_line_ids:
                    element.sequence = element.sequence + 2
                line_vals_list = {
                  'sequence': line_index,
                  'name': _('Sub-Total:    ') + str("%.2f" % subtotal)+' '+line.currency_id.symbol,
                  'currency_id': line.currency_id.symbol,
                  'quantity': 1,
                  'currency_id': 5,
                  'tax_exigible': True,
                  'display_type': 'line_sub_total',
                  'new_line': True,
                  'move_id': self.id
                }

                new_line = self.env['account.move.line'].create(line_vals_list)
                line_index += line.sequence
                subtotal = 0
                section_2 = False
            seq = line.sequence
        if subtotal != 0:
            line_vals_list = {
              'sequence': seq,
              'name': _('Sub-Total:      ')+str("%.2f" % subtotal)+' '+line.currency_id.symbol,
              'currency_id': line.currency_id.symbol,
              'quantity': 1,
              'currency_id': 5,
              'tax_exigible': True,
              'display_type': 'line_sub_total',
              'new_line': True,
              'move_id': self.id
            }
            new_line = self.env['account.move.line'].with_context(request_from_action_subtotal=True).create(line_vals_list)


    def add_subtotal_create(self):
        subtotal = 0
        seq = 0
        invoice_line_ids = self.env["account.move.line"].search([
            ('move_id', '=', self.id),
            ('exclude_from_invoice_tab', '=', False)])
        line_index = 1
        for line in invoice_line_ids:
            line_index += 1
            line.sequence = line_index
            if not line.display_type:
                subtotal += line.price_subtotal
            if line.display_type == 'line_subtotal':
                seq = line.sequence
                line_vals_list = {
                    'sequence': seq,
                    'name': _('Sub-Total-manuel:      ')+str("%.2f" % subtotal) + ' ' + line.currency_id.symbol,
                    'currency_id': line.currency_id.symbol,
                    'quantity': 1,
                    'currency_id': 5,
                    'tax_exigible': True,
                    'display_type': 'line_subtotal',
                    'new_line': False,
                    'move_id': self.id
                }
                new_line = line.write(
                    line_vals_list)
                subtotal = 0
    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        if not self._context.get('request_from_action_subtotal'):
            for move in res:
                move.action_subtotal_create()
                move.add_subtotal_create()
        res.write({'update_sequence' : 'test'})
        return res



    def write(self, vals):
        res = super(AccountMove, self).write(vals)
        if not self._context.get('request_from_action_subtotal'):
            for move in self:
                move.action_subtotal()
                move.add_subtotal()
        return res

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    new_line = fields.Boolean(default=False)
    display_type = fields.Selection(selection_add=[('line_sub_total', 'Subtotal'), ('line_title', 'Titre'), ('line_subtotal', 'Subtotal')])


    _sql_constraints = [
        (
            'check_credit_debit',
            'CHECK(credit + debit>=0 AND credit * debit=0)',
            'Wrong credit or debit value in accounting entry !'
        ),
        (
            'check_accountable_required_fields',
             "CHECK(COALESCE(display_type IN ('line_section', 'line_note', 'line_sub_total, 'line_subtotal, 'line_title'), 'f') OR account_id IS NOT NULL)",
             "Missing required account on accountable invoice line."
        ),
        (
            'check_non_accountable_fields_null',
             "CHECK(display_type NOT IN ('line_section', 'line_note', 'line_sub_total', 'line_subtotal', 'line_title') OR (amount_currency = 0 AND debit = 0 AND credit = 0 AND account_id IS NULL))",
             "Forbidden unit price, account and quantity on non-accountable invoice line"
        ),
        (
            'check_amount_currency_balance_sign',
            '''CHECK(
                (
                    (currency_id != company_currency_id)
                    AND
                    (
                        (debit - credit <= 0 AND amount_currency <= 0)
                        OR
                        (debit - credit >= 0 AND amount_currency >= 0)
                    )
                )
                OR
                (
                    currency_id = company_currency_id
                    AND
                    ROUND(debit - credit - amount_currency, 2) = 0
                )
            )''',
            "The amount expressed in the secondary currency must be positive when account is debited and negative when "
            "account is credited. If the currency is the same as the one from the company, this amount must strictly "
            "be equal to the balance."
        ),
    ]

