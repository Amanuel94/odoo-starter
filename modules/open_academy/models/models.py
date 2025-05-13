# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import ValidationError


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


class CustomPartner(models.Model):
    _name = "open_academy.partner"
    _inherits = {"res.partner": "partner_id"}

    instructor = fields.Boolean(string="Instructor", default=False)
    category = fields.Selection(
        selection=[
            ("none", "None"),
            ("t1", "Teacher/Level 1"),
            ("t2", "Teacher/Level 2"),
        ],
        string="Category",
        required=True,
    )
    session_ids = fields.Many2many(
        comodel_name="open_academy.session",
        string="Sessions",
        relation="session_instructor_rel",
        column1="partner_id",
        column2="session_id",
    )


class Session(models.Model):
    _name = "open_academy.session"
    _description = "open_academy.session"
    name = fields.Char(string="Session Name", required=True)
    start_date = fields.Datetime(
        string="Start Date",
        default=fields.Date.context_today,
    )
    active = fields.Boolean(string="Active", default=lambda self: True)
    duration = fields.Float(string="Duration (hours)", required=True)
    seats = fields.Integer(string="Number of Seats")

    percentage_seats2 = fields.Float(
        string="Percentage of Seats Taken", compute="_compute_percentage_seats2"
    )

    instructor = fields.Many2one(
        comodel_name="open_academy.partner",
        string="Instructor",
        ondelete="restrict",
        required=True,
        domain="['|', ('instructor', '=', True), ('category', '!=', 'none')]",
    )

    course_id = fields.Many2one(
        comodel_name="open_academy.course",
        string="Course",
        ondelete="cascade",
        required=True,
    )
    attendees_ids = fields.Many2many(
        comodel_name="open_academy.partner",
        string="Attendees",
        relation="session_attendees_rel",
        column1="session_id",
        column2="partner_id",
    )

    @api.depends("attendees_ids", "seats")
    def _compute_percentage_seats2(self):
        for record in self:
            record.percentage_seats2 = (
                (len(record.attendees_ids) / record.seats) if record.seats > 0 else 0
            ) * 100

    @api.onchange("seats")
    def _onchange_seats(self):
        if self.seats < 0:
            return {
                "warning": {
                    "title": "Invalid value",
                    "message": "The number of seats must be positive.",
                }
            }
        if self.seats < len(self.attendees_ids):
            return {
                "warning": {
                    "title": "Too many attendees",
                    "message": "There are more attendees than seats.",
                }
            }

    @api.onchange("attendees_ids")
    def _onchange_attendees_ids(self):
        if len(self.attendees_ids) > self.seats:
            return {
                "warning": {
                    "title": "Too many attendees",
                    "message": "There are more attendees than seats.",
                }
            }
        if len(self.attendees_ids) == self.seats:
            return {
                "warning": {
                    "title": "Seats full",
                    "message": "All seats are taken.",
                }
            }

    @api.constrains("attendees_ids", "instructor")
    def _check_instructor_not_attendee(self):
        for record in self:
            if record.instructor in record.attendees_ids:
                raise ValidationError(
                    "The instructor cannot be an attendee of the session."
                )
