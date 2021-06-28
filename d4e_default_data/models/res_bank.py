# -*- coding: utf-8 -*-
from odoo.osv import expression
from odoo import api, fields, models, _


class ResBank(models.Model):
    _inherit = "res.bank"

    clearing = fields.Char(string="Clearing")

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
