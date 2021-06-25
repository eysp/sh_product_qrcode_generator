# -*- coding:utf-8 -*-

from odoo.osv import expression
from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_no = fields.Integer(string="Customer no.", default=0)

    @api.onchange('zip')
    def on_change_zip(self):
        post = self.env['postal.number'].search([('POSTLEITZAHL', '=', self.zip)])
        self.city = post[0].ORTBEZ27

    @api.onchange('city')
    def on_change_city(self):
        post = self.env['postal.number'].search([('ORTBEZ27', '=', self.city)])
        self.zip = post[0].POSTLEITZAHL

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = ['|', '|', ('city', '=ilike', name + '%'), ('zip', '=ilike', name + '%'), ('name', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)