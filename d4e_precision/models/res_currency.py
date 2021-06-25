# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.addons import decimal_precision as dp


class Currency(models.Model):
    _inherit = 'res.currency'

    rounding = fields.Float(string='Rounding Factor',
                            digits=dp.get_precision('Currency Rounding'),
                            default=0.01)
    rate = fields.Float(compute='_compute_current_rate',
                        string='Current Rate',
                        digits=dp.get_precision('Currency Rate'),
                        help='The rate of the currency to the currency of rate 1.')
