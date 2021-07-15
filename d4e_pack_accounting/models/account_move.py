# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    internal_reference = fields.Char(string='Internal Reference')
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


    @api.onchange('invoice_line_ids')
    def _onchange_invoice_line_ids(self):
        new_lines = self.env['account.move.line']
        new_line1 = new_lines.new({

                'sequence': 10,
                'name': 'Sous-Total-manuel 1 : 00',
                'quantity': 1,
                'partner_id': 8,
                'amount_currency': 0,
                'currency_id': 1,
                'debit': 0,
                'credit': 0,
                'recompute_tax_line': True,
                'predict_from_name': False,
                'display_type': 'line_subtotal',
                'is_rounding_line': False,
                'exclude_from_invoice_tab': False

        })
        new_line2 = new_lines.new({

                'sequence': 10,
                'name': 'Sous-Total-manuel 2 : 00',
                'quantity': 1,
                'partner_id': 8,
                'amount_currency': 0,
                'currency_id': 1,
                'debit': 0,
                'credit': 0,
                'recompute_tax_line': True,
                'predict_from_name': False,
                'display_type': 'line_subtotal',
                'is_rounding_line': False,
                'exclude_from_invoice_tab': False

        })
        new_lines += new_line1
        new_lines += new_line2
        new_lines += self.invoice_line_ids
        self.invoice_line_ids = new_lines
        print("int_lines : ", self.invoice_line_ids)


    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        # if not self._context.get('request_from_action_subtotal'):
        #     for move in res:
        #         move.action_subtotal_create()
        #         move.add_subtotal_create()
        # res.write({'update_sequence' : 'test'})
        return res



    def write(self, vals):
        res = super(AccountMove, self).write(vals)
        # if not self._context.get('request_from_action_subtotal'):
        #     for move in self:
        #         move.action_subtotal()
        #         move.add_subtotal()
        return res



class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    new_line = fields.Boolean(default=False)
    display_type = fields.Selection(selection_add=[('line_sub_total', 'Subtotal'), ('line_title', 'Titre'), ('line_subtotal', 'Subtotal')])


    @api.model
    def default_get(self, fields):
        res = super(AccountMoveLine, self).default_get(fields)
        print("self._context : ", self._context.get('current_line_vals'))
        # 'default_display_type': 'line_subtotal'
        if self._context.get('default_display_type') == 'line_subtotal':
            sub_total = 0.0
            if self._context.get('current_line_vals'):

                for line in self._context.get('current_line_vals'):
                    if (len(line) > 2) and (not (type(line[2]) is bool)) and line[2].get('credit'):
                        sub_total += line[2]['credit']
            res.update({
                    'name': _('Sub-Total-manuel:      ')+str("%.2f" % sub_total) + ' ',
                # + line.currency_id.symbol

                })

        # active_ids = self.env.context.get('active_ids', [])
        # refuse_model = self.env.context.get('hr_expense_refuse_model')
        # if refuse_model == 'hr.expense':
        #     res.update({
        #         'hr_expense_ids': active_ids,
        #         'hr_expense_sheet_id': False,
        #     })
        # elif refuse_model == 'hr.expense.sheet':
        #     res.update({
        #         'hr_expense_sheet_id': active_ids[0] if active_ids else False,
        #         'hr_expense_ids': [],
        #     })
        return res

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

