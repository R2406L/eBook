# -*- coding: utf-8 -*-
{
    'name': "eBook storage service",
    'description': "Light electronic book storage service",
    'author': "R2406",
    'website': "https://svgun.ru/odoo",
    'category': 'Services',
    'version': '0.0.3',
    'license': 'GPL-3',

    'depends': ['contacts'],

    'auto_install': False,
    'installable': True,
    'application': True,

    'assets': {
        'web.assets_frontend': [
            'ebook/static/src/snippets/s_ebook_public/000.xml',
            'ebook/static/src/snippets/s_ebook_public/001.xml',
            'ebook/static/src/snippets/s_ebook_public/000.js',
            'ebook/static/src/snippets/s_ebook_public/000.scss',
            'ebook/static/src/snippets/s_ebook_public/001.scss',
        ],
	},

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',

        'views/book.xml',
        'views/category.xml',
        'views/tags.xml',
        'views/public_tags.xml',
        'views/_menu.xml',

        'views/snippets/books.xml',

        'views/portal/ebook_list.xml',
        'views/portal/ebook_menu.xml',
    ],
}
