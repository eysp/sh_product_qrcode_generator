# -*- coding:utf-8 -*-

from odoo import api, fields, models


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'


    def _compute_count_repair(self):
        repair = self.env['repair.order']
        for record in self:
            record.repair_count = repair.search_count([('vehicle_id', '=', record.id)])


    driving_license = fields.Binary(string='Driving license', readonly=False, help='Upload the file')
    last_expertise = fields.Date('Last Expertise Date', required=False, default=fields.Date.today, tracking=True)
    weight = fields.Float(string='Weight')
    key_code_1 = fields.Char('Key Code 1')
    key_code_2 = fields.Char('Key Code 2')
    radio_code = fields.Char('Radio Code')
    key_identification = fields.Char('Key Identification')
    policy_number = fields.Char('Policy N°')
    insurance_id = fields.Many2one('fleet.vehicle.log.insurance', 'Insurance', tracking=True)
    repair_count = fields.Integer(compute="_compute_count_repair", string='Repairs Count')

    def return_repair_to_open(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Repairs',
            'view_mode': 'tree',
            'res_model': 'repair.order',
            'domain': [('vehicle_id', '=', self.id)],
        }





