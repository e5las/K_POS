# -*- coding: utf-8 -*-
{
    'name': "Nutikad Theme",

    'summary': """
        Nutikad / Theme for odoo 13""",

    'description': """
       Odoo 13.0 Theme
    """,

    'author': "NUTIKAD",
    'website': "http://www.nutikad.com",

    
    'category': 'Theme',
    'version': '1.0',

    'depends': ['base', 'web', 'calendar', 'contacts'],

    'data': [
        'views/webclient_templates.xml',
        'views/login_layout.xml',
        'views/assets.xml',
        'views/menus.xml',
    ],
    'qweb': [
        'static/src/xml/base.xml',
    ],
    'images': [
        'static/description/1.png',
        'static/description/2.png',
        'static/description/3.png',
        'static/description/4.png',
    ],
    'license': 'LGPL-3',
    'auto_install': False,
    'installable': True,
    'application':True,
}
