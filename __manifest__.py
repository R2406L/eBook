# -*- coding: utf-8 -*-
{
    'name': "eBook storage service",
    'description': "Light electronic book storage service",
    'author': "R2406",
    'website': "https://svgun.ru/odoo",
    'category': 'Services',
    'version': '0.0.2',
    'license': 'GPL-3',

    'depends': ['contacts'],

    'auto_install': False,
    'installable': True,
    'application': True,

    'data': [
	'security/groups.xml',
	'security/ir.model.access.csv',

	'views/book.xml',
	'views/category.xml',
	'views/_menu.xml',
    ],
}
