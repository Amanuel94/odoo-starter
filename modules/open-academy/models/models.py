# -*- coding: utf-8 -*-

from odoo import models, fields


class Course(models.Model):
    _name = "open_academy.course"
    _description = "open_academy.course"
    title = fields.Char(string="title", required=True)
    description = fields.Text(string="description")
