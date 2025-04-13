# -*- coding: utf-8 -*-
# from odoo import http


# class Open-academy(http.Controller):
#     @http.route('/open-academy/open-academy/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/open-academy/open-academy/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('open-academy.listing', {
#             'root': '/open-academy/open-academy',
#             'objects': http.request.env['open-academy.open-academy'].search([]),
#         })

#     @http.route('/open-academy/open-academy/objects/<model("open-academy.open-academy"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('open-academy.object', {
#             'object': obj
#         })
