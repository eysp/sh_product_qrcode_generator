# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    unpaid_invoice = fields.Boolean(string='Unpaid Invoice')
