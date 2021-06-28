# -*- coding: utf-8 -*-

from odoo import fields, models

class PostalNumber(models.Model):
    _description = 'Postal Number'
    _name = 'postal.number'

    REC_ART = fields.Char()
    ONRP = fields.Char()
    BFSNR = fields.Char()
    PLZ_TYP = fields.Char()
    POSTLEITZAHL = fields.Char()
    PLZ_ZZ = fields.Char()
    GPLZ = fields.Char()
    ORTBEZ18 = fields.Char()
    ORTBEZ27 = fields.Char()
    KANTON = fields.Char()
    SPRACHCODE = fields.Char()
    SPRACHCODE_ABW = fields.Char()
    BRIEFZ_DURCH = fields.Char()
    GILT_AB_DAT = fields.Char()
    PLZ_BRIEFZUST = fields.Char()
    PLZ_COFF = fields.Char()
    Geo_Shape = fields.Text()
    Geokoordinaten_1 = fields.Text()
    Geokoordinaten_2 = fields.Text()


