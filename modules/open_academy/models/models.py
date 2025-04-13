# -*- coding: utf-8 -*-

from odoo import models, fields


class Course(models.Model):
    _name = "open_academy.course"
    _description = "open_academy.course"
    title = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")
    responsible_user = fields.Many2one(
        comodel_name="res.users",
        string="Responsible User",
        ondelete="restrict",
        required=True,
    )
    session_ids = fields.One2many(
        comodel_name="open_academy.session",
        inverse_name="course_id",
        string="Sessions",
    )


class Session(models.Model):
    _name = "open_academy.session"
    _description = "open_academy.session"
    name = fields.Char(string="Session Name", required=True)
    start_date = fields.Datetime(string="Start Date", required=True)
    duration = fields.Float(string="Duration (hours)", required=True)
    seats = fields.Integer(string="Number of Seats")
    instructor = fields.Many2one(
        comodel_name="res.partner",
        string="Instructor",
        ondelete="restrict",
        required=True,
    )
    course_id = fields.Many2one(
        comodel_name="open_academy.course",
        string="Course",
        ondelete="cascade",
        required=True,
    )
    attendees_ids = fields.Many2many(
        comodel_name="res.partner",
        string="Attendees",
        relation="session_attendees_rel",
        column1="session_id",
        column2="partner_id",
    )
