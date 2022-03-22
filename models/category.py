# -*- coding: utf-8 -*-

from odoo import fields, models, api

class Category(models.Model):
    _name = 'ebook.category'
    _description = 'Book category model definition'

    id = fields.Integer('ID')
    name = fields.Char('Name')

