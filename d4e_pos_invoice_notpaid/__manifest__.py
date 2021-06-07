# -*- coding: utf-8 -*-
{
    'name': "D4E Pos Invoice Not Paid",
    'summary': """Digital4Efficiency - Add a payment method that generate an unpaid posted invoice""",
    'description': """Add a payment method that generate an unpaid posted invoice.""",
    'category': 'Sales/Point Of Sale',
    'version': '14.0.1.0',
    'depends': [
        'web',
        'point_of_sale',
        'account_accountant',
        'l10n_generic_coa',
        'l10n_ch',
    ],
    'data': [
        'views/ir_actions_server.xml',
        'views/pos_payment_method_views.xml',
        'views/point_of_sale.xml',
    ],
    'qweb': [
        'static/src/xml/OrderReceipt.xml',
    ],
    'post_init_hook': 'create_payment_methode_unpaid_invoice',
}
