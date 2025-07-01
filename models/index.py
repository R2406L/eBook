# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Category(models.Model):
    _name = 'ebook.category'
    _description = 'Book category model definition'

    id = fields.Integer('ID')
    name = fields.Char('Name')

class Tags(models.Model):
    _name = 'ebook.tags'
    _description = 'Book tags model definition'

    id = fields.Integer('ID')
    name = fields.Char('Name')

class PublicTags(models.Model):
    _name = 'ebook.public_tags'
    _description = 'Book public tags model definition'

    id = fields.Integer('ID')
    name = fields.Char('Name')