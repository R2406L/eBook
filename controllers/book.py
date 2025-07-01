# -*- coding: utf-8 -*-

import json
import datetime, base64, logging
from odoo import fields, http, SUPERUSER_ID, _
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.http import request, Controller
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
_logger = logging.getLogger(__name__)

MODEL = 'ebook.book'

class EBookWebsite(Controller):

    @http.route('/ebook/public', type='http', auth="public", website=False, methods=['GET'])
    def ebook_public(self, **kwargs):
        tags = kwargs.get("tags")
        domain = [("public_tags_ids.name", "in", tags.split(','))] if len(tags) > 0 else []
        books = request.env[MODEL].sudo().search([('is_public', '=', True)] + domain)
        resp = []
        for b in books:
            resp.append({
                "id": b.id,
                "name": b.name,
                "short_description": b.short_description,
                "tags": [(a.id, a.name) for a in b.public_tags_ids],
                "downloads": b.downloads
            })
        return json.dumps(resp)

    @http.route('/ebook/tags', type='http', auth="public", website=False, methods=['GET'])
    def ebook_tags(self, **kwargs):
        tags = request.env['ebook.public_tags'].sudo().search([])
        return json.dumps([t.name for t in tags])

    @http.route('/ebook/preview/<int:id>', type='http', auth="public", website=False, methods=['GET'])
    def ebook_preview(self, id, **kwargs):
        book = request.env[MODEL].sudo().search([('is_public', '=', True), ("id", "=", id)], limit=1)
        data = base64.b64decode(book.image)
        headers = [('Content-Type', 'image/jpeg'),('Content-Length', len(data))]
        return request.make_response(data, headers=headers)

    @http.route('/ebook/download/<int:id>', type='http', auth="public", website=False, methods=['GET'])
    def ebook_download(self, id, **kwargs):
        book = request.env[MODEL].sudo().search([('is_public', '=', True), ("id", "=", id)], limit=1)
        book.downloads += 1
        data = base64.b64decode(book.attachment_id)
        headers = [('Content-Type', 'application/pdf'),('Content-Length', len(data))]
        return request.make_response(data, headers=headers)

class EBookPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        Book = request.env[MODEL]
        books_count = Book.sudo().search_count(self._prepare_approval_domain())
        values['books_count'] = books_count if books_count else '0'
        return values

    def _prepare_approval_domain(self):
        return []

    def _prepare_approval_portal_rendering_values(
        self, page=1, date_begin=None, date_end=None, sortby=None, quotation_page=False, **kwargs
    ):
        Book = request.env[MODEL]

        if not sortby:
            sortby = 'date'

        domain = self._prepare_approval_domain()
        values = self._prepare_portal_layout_values()

        pager_values = portal_pager(
            url="/my/ebooks",
            total=Book.search_count(domain),
            page=page,
            step=self._items_per_page,
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
        )
        books = Book.search(domain, order=sortby, limit=self._items_per_page, offset=pager_values['offset'])

        values.update({
            'date': date_begin,
            'approvals': books.sudo(),
            'page_name': 'ebooks',
            'pager': pager_values,
            'default_url': "/my/ebooks"
        })
        return values

    @http.route(['/my/ebooks'], type='http', auth="user", website=True)
    def portal_my_ebooks(self, **kwargs):
        books = request.env[MODEL].sudo().search([])
        values = self._prepare_approval_portal_rendering_values(quotation_page=False, **kwargs)
        values.update({
            "books": books
        })
        return request.render("ebooks.portal_my_ebooks", values)


    @http.route(['/my/ebooks/<int:id>'], type='http', auth="public", website=True)
    def portal_my_ebooks_page(self, id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            book = self._document_check_access(MODEL, id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my/ebooks')

        values = self._prepare_portal_layout_values()
        values = self._get_page_view_values(approval, access_token, values, False, False)
        values.update({
            "book": book,
            "page_name": "ebooks",
            "default_url": "/my/ebooks"
        })

        return request.render("ebooks.portal_ebooks_template", values)

