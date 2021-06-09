# -*- coding:utf-8 -*-

from odoo import api, fields, models


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    driving_license = fields.Binary(string='Driving license', readonly=False, help='Upload the file')
    last_expertise = fields.Date('Last Expertise Date', required=False, default=fields.Date.today, tracking=True)
    weight = fields.Float(string='Weight')
    key_code_1 = fields.Char('Key Code 1')
    key_code_2 = fields.Char('Key Code 2')
    radio_code = fields.Char('Radio Code')
    key_identification = fields.Char('Key Identification')
    policy_number = fields.Char('Policy N°')
    insurance_id = fields.Many2one('fleet.vehicle.log.insurance', 'Insurance', tracking=True)
    description = fields.Text('description', tracking=True, help='Write here any other information about this vehicle')



