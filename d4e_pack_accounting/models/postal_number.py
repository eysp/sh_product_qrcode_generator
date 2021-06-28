# -*- coding: utf-8 -*-

from odoo import fields, models

class PostalNumber(models.Model):
    _description = 'Postal Number'
    _name = 'postal.number'

    onrp = fields.Char(string='Identifiant')
    bfsnr = fields.Char(string='N° OFS')
    plz_typ = fields.Char(string='Type de NPA')
    kanton = fields.Char(string='Canton')
    gplz = fields.Char(string='NPA')
    ortbez18 = fields.Char(string='Localité')
    sprachcode = fields.Selection([('1', 'Allemand'), ('2', 'Français'), ('3', 'Italien')], string="Langue", default='1')




