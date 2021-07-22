# -*- coding:utf-8 -*-

from odoo import api, fields, models
from odoo.osv import expression


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

    def name_get(self):
        res = super(FleetVehicle, self).name_get()
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if operator == 'ilike' and not (name or '').strip():
            domain = []
        else:
            connector = '&' if operator in expression.NEGATIVE_TERM_OPERATORS else '|'
            domain = [connector, ('license_plate', operator, name),
                      '|', ('model_id.name', operator, name),
                      ('model_id.brand_id.name', operator, name)]
        return self._search(domain, limit=limit, access_rights_uid=name_get_uid)
