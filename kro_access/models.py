# -*- coding: utf-8 -*-

from openerp import models, fields, api


class FieldsAccess(models.Model):
    _name = 'kro.access'
    w_approved_by_executor = fields.Boolean(compute='compute_fields')
    w_approved_by_predicator = fields.Boolean(compute='compute_fields')
    w_approved_by_approver = fields.Boolean(compute='compute_fields')

    @api.model
    def compute_fields(self):
        self.w_approved_by_executor = False
        self.w_approved_by_predicator = False
        self.w_approved_by_approver = False
