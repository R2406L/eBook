# -*- coding: utf-8 -*-

from odoo import fields, models, api
import os

class Book(models.Model):
    _name = 'ebook.book'
    _inherit = 'mail.thread'
    _description = 'Book model definition'

    id = fields.Integer('ID')
    name = fields.Char('Name', compute='_get_name', store=True)
    local_name = fields.Char('Local name', size=256)
    original_name = fields.Char('Original name', size=256)
    country_id = fields.Many2one('res.country',string='Country')
    author_ids = fields.Many2many('res.partner',string='Authors')
    category_ids = fields.Many2many('ebook.category',string='Categories')
    files = fields.Many2many('ir.attachment',string='Files')
    image = fields.Binary('Illustration')
    description = fields.Text('Short description')
    pages = fields.Integer('Page count')
    year = fields.Char('Year of publish',size=4)
    formats = fields.Char('File formats', compute='_get_formats')
    isbn = fields.Char('ISBN')

    @api.depends('local_name','original_name')
    def _get_name(self):
        for s in self:
            if (s.original_name):
                s.name = "%s (%s)" % (s.local_name,s.original_name)
            else:
                s.name = s.local_name

    @api.depends('files')
    def _get_formats(self):
        for s in self:
            fs = []
            for f in s.files:
                file_extension = os.path.splitext(f.name)[1]
                fs.append(file_extension)
            s.formats = ','.join(fs)
