# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Repair(models.Model):
    _inherit = 'repair.order'

    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle', tracking=True, domain="['|', ('driver_id', '=', False), ('driver_id', '=', partner_id)]")
    mileage = fields.Float(string='Mileage')

    @api.onchange('vehicle_id')
    def on_change_client(self):
        self.partner_id = self.vehicle_id.driver_id
        self.mileage = self.vehicle_id.odometer



