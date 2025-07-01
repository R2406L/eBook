# -*- coding: utf-8 -*-

from odoo import fields, models, api
from PIL import Image
from odoo.tools import config
import os, logging, fitz, io, base64, subprocess, time

_logger = logging.getLogger(__name__)

class BookManagement(models.Transientmodel):
    _name = 'ebook.management'
    _description = 'Book management model definition'

    backup_file = fields.Binary('Backup file')