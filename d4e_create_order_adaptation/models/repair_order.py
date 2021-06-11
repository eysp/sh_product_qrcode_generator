# -*- coding: utf-8 -*-

from odoo import api, fields, models


class Repair(models.Model):
    _inherit = 'repair.order'

    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle', tracking=True, domain="['|', ('driver_id', '=', False), ('driver_id', '=', partner_id)]")
    mileage = fields.Float(string='Mileage')
    product_id = fields.Many2one(
        'product.product', string='Product to Repair',
        domain="['|', ('company_id', '=', company_id), ('company_id', '=', False)]",
        default=lambda self: self.env.ref('d4e_create_order_adaptation.consumable_product', raise_if_not_found=False),
        readonly=True, required=False, states={'draft': [('readonly', False)]}, check_company=True)


    @api.onchange('vehicle_id')
    def on_change_client(self):
        self.partner_id = self.vehicle_id.driver_id
        self.mileage = self.vehicle_id.odometer

    def _create_invoices(self, group=False):
        res = super(Repair, self)._create_invoices(group=group)
        for repair_id in res:
            repair = self.env['repair.order'].browse(repair_id)
            invoice = self.env['account.move'].browse(res[repair_id])
            invoice['vehicle_id'] = repair['vehicle_id']
            invoice['invoice_mileage'] = repair['mileage']
        return res

    def write(self, vals):
        res = super(Repair, self).write(vals)
        if 'mileage' in vals:
            self.vehicle_id.odometer = self.mileage
        return res

    @api.model
    def create(self, vals):
        res = super(Repair, self).create(vals)
        if ('mileage' in vals) and (res.vehicle_id):
            res.vehicle_id.write({'odometer': res.mileage})
        return res
