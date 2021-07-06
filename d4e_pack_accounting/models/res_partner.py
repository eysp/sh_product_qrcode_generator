# -*- coding:utf-8 -*-

from odoo.osv import expression
from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'


    def compute_customer_no(self):
        num = self.env['res.partner'].search([])
        maxi = num.mapped('customer_no')
        if not maxi:
            return 1
        return max(maxi) + 1

    customer_no = fields.Integer(string="Customer no.", default=compute_customer_no)
    phone_2 = fields.Char(string="Phone 2")
    city = fields.Many2one('postal.number', string='City', ondelete='restrict')

    @api.onchange('zip')
    def on_change_zip(self):
        if self.zip:
            return {'domain': {'city': [('gplz', '=', self.zip)]}}
        else:
            self.city = {}
            return {'domain': {'city': []}}


    @api.onchange('city')
    def on_change_city(self):
        if self.city:
            self.zip = self.city.gplz

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = ['|', '|', ('city', '=ilike', name + '%'), ('zip', '=ilike', name + '%'), ('name', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)