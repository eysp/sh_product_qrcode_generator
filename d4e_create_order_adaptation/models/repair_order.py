# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Repair(models.Model):
    _inherit = 'repair.order'

    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle', tracking=True, domain="['|', ('driver_id', '=', False), ('driver_id', '=', partner_id)]")
    mileage = fields.Float(string='Mileage')
    product_id = fields.Many2one(
        'product.product', string='Product to Repair',
        domain="[('type', 'in', ['product', 'consu']), '|', ('company_id', '=', company_id), ('company_id', '=', False)]",
        readonly=True, required=False, states={'draft': [('readonly', False)]}, check_company=True)
    product_uom = fields.Many2one(
        'uom.uom', 'Product Unit of Measure',
        readonly=True, required=False, states={'draft': [('readonly', False)]}, domain="[('category_id', '=', product_uom_category_id)]")
    location_id = fields.Many2one(
        'stock.location', 'Location',
        index=True, readonly=True, required=False, check_company=True,
        help="This is the location where the product to repair is located.",
        states={'draft': [('readonly', False)], 'confirmed': [('readonly', True)]})

    @api.onchange('vehicle_id')
    def on_change_client(self):
        self.partner_id = self.vehicle_id.driver_id
        self.mileage = self.vehicle_id.odometer



