# -*- coding:utf-8 -*-

from odoo import api, fields, models

class FleetVehicleInsurance(models.Model):
    _name = 'fleet.vehicle.log.insurance'

    name = fields.Char('Name', required=True, translate=True)
