# -*- coding: utf-8 -*-
{
    'name': "Create Order Adaptation",
    'description': """
        Adaptation of the order creation file in the Repairs module
    """,
    'author': "D4E",
    'website': "https://www.d4e.cool",
    'category': 'Tools',
    'version': '13.0',

    # any module necessary for this one to work correctly
    'depends': ['repair', 'fleet'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/product.xml',
        'views/repair_views.xml',
        'views/account_move.xml',
        'reports/report_repair_order.xml',
        'reports/report_invoice.xml',
    ],
}