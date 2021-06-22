# -*- coding:utf-8 -*-

from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_no = fields.Integer(string="Customer no.", default=1)

    def increment(self):
        self.customer_no = self.customer_no + 1
