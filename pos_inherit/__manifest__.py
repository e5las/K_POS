# -*- coding: utf-8 -*-
{
    'name': "POS of Pharmacy",

    'summary': """
        POS FOR Pharmacy""",

    'description': """
        POS FOR Pharmacy
    """,

    'author': "Eng.Ekhlas Mohamed Abdallah",
    'website': "https://www.linkedin.com/in/eng-ekhlas-mohamed-software-engineer-48ab6596",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','om_account_accountant','currency_rate_inverted',
    'point_of_sale','pos_discount','product_return_pos','pos_scan_camera','pos_ui_design',
    'sr_print_pos_session','nuro_pos_receipt','l10n_generic_coa','pos_traceability_validation','product_multi_uom_pos',
    'purchase','product_expiry','stock_picking_auto_create_lot','pos_disable_discount',
    'muk_web_theme'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/sale_view_wizard.xml',
        'views/pos_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': ['static/src/xml/pos.xml'],

}
