# -*- coding: utf-8 -*-

from odoo import fields, models, api
from PIL import Image
from odoo.tools import config
import os, logging, fitz, io, base64, subprocess, time

_logger = logging.getLogger(__name__)

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
    attachment_id = fields.Binary(string='File')
    image = fields.Binary('Illustration')
    description = fields.Text('Short description')
    pages = fields.Integer('Page count')
    year = fields.Char('Year of publish',size=4)
    isbn = fields.Char('ISBN')

    @api.depends('local_name','original_name')
    def _get_name(self):
        for s in self:
            if (s.original_name):
                s.name = "%s (%s)" % (s.local_name,s.original_name)
            else:
                s.name = s.local_name

    def get_preview(self):
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        filename = str(int(time.time()))
        dst_file = "%s/temp/thumb_%s.jpg" % (path, filename)
        src_file = "%s/temp/orig_%s.pdf" % (path, filename)

        file_content = base64.b64decode(self.attachment_id)
        with open(src_file, "wb+") as f:
            f.write(file_content)
            f.close()

        params = 'convert %s[0] -density 300 -resize 500x500^ %s' % (src_file, dst_file)
        subprocess.call(params, shell=True)
        if os.path.isfile(dst_file):
            with open(dst_file, "rb") as image_file:
                self.image = base64.b64encode(image_file.read())
            os.unlink(dst_file)
        os.unlink(src_file)
