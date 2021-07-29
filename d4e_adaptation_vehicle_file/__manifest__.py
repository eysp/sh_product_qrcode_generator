# -*- coding: utf-8 -*-
{
    'name': "Vehicle file adaptation",
    'description': """
        Adaptation of the vehicle file in the Fleet module
    """,
    'author': "D4E",
    'website': "https://www.d4e.cool",
    'category': 'Tools',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['fleet', 'hr_fleet'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_views.xml',
        'views/fleet_insurance_view.xml',
    ],

}