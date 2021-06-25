# -*- coding: utf-8 -*-
{
    'name': "D4E Default data",
    'description': """
        D4E Default data
    """,
    'author': "D4E",
    'website': "https://www.d4e.cool",
    'category': 'Tools',
    'version': '14.0',

    # any module necessary for this one to work correctly
    'depends': ['account', 'base', 'contacts', 'l10n_ch'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/account_tax_data.xml',
        'data/account_data.xml',
        'views/account.xml',
        'views/res_partner.xml',
        'views/template.xml',
        'views/res_bank.xml',
        'views/postal_number.xml',
    ],
}