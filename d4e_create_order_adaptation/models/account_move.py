# -*- coding: utf-8 -*-

from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = 'account.move'

    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle', tracking=True)
    invoice_mileage = fields.Float(string='Mileage')

    def write(self, vals):
        res = super(AccountMove, self).write(vals)
        if 'invoice_mileage' in vals:
            self.vehicle_id.odometer = self.invoice_mileage
        return res
