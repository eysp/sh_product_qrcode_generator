# -*- coding: utf-8 -*-
import json

from odoo.osv import expression
from odoo import api, fields, models, _
import requests


class ResBank(models.Model):
    _inherit = "res.bank"

    clearing = fields.Char(string="Clearing")
    swissbank_id = fields.Char()

    def name_get(self):
        res = super(ResBank, self).name_get()
        result = []
        for bank in self:
            name = bank.name + (bank.clearing and (' - ' + bank.clearing) or '') + (bank.bic and (' - ' + bank.bic) or '')
            result.append((bank.id, name))
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', '|', ('bic', '=ilike', name + '%'), ('name', operator, name), ('clearing', '=ilike', name + '%')]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&'] + domain
        return self._search(domain + args, limit=limit, access_rights_uid=name_get_uid)

    @api.model
    def create_bank_with_api(self):
        url = "https://api.six-group.com/api/epcd/bankmaster/v2/public"
        reponse = requests.get(url).json()
        for rec in reponse['entries']:
            swissbank_id = str(rec.get('group') or '') + str(rec.get('iid') or '') + str(rec.get('branchId') or '') + str(rec.get('sicIid') or '') + str(rec.get('headOffice') or '')
            bank_vals = {
                'name': rec.get('bankOrInstitutionName') or '',
                'phone': rec.get('phone') or '',
                'zip': rec.get('zipCode') or '',
                'street': rec.get('domicileAddress') or '',
                'city': rec.get('place') or '',
                'bic': rec.get('bic') or '',
                'swissbank_id': swissbank_id,
            }
            bank = self.env["res.bank"].search([('swissbank_id', '=', bank_vals['swissbank_id'])])
            if bank:
                bank.write(bank_vals)
            else:
                self.env["res.bank"].create(bank_vals)
