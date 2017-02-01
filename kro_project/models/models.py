# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Project(models.Model):

    _inherit = 'project.project'
    problem_ids = fields.Many2many('kro.problem', string=u'Проблемы')


class Problem(models.Model):

    _name = 'kro.problem'
    _inherit = 'project.task'

    name = fields.Char(u'Заголовок', track_visibility='onchange', size=128, required=True, select=True)
    project_id = fields.Many2one('project.project', 'Проект', ondelete='set null', select=True, track_visibility='onchange', change_default=True)
    user_id = fields.Many2one('res.users', 'Инициатор', select=True, track_visibility='onchange')
    user_aim_id = fields.Many2one('res.users', 'Ответственный за определение целей', select=True, track_visibility='onchange')
    user_plan_id = fields.Many2one('res.users', 'Ответственный за планирование', select=True, track_visibility='onchange')
    user_admin_id = fields.Many2one('res.users', 'Администратор', select=True, track_visibility='onchange')
    description = fields.Html('Формулировка проблемы')
    symptoms = fields.Text('Как проявляется (проявится)')
    effects = fields.Text('Последствия')
    causes = fields.Text('Причины')
    decision = fields.Text('Решение')


    aim_ids = fields.Many2many('kro.aim', string=u'Цели')
    state = fields.Selection([('draft', 'Черновик'),
                              ('approved', 'Утвержден'),
                              ('current', 'Текущий'),
                              ('canceled', 'Отменен'),
                              ], 'Статус', readonly=True, default='draft')


class Aim(models.Model):

    _name = 'kro.aim'
    _inherit = 'project.task'

    name = fields.Char(u'Заголовок', track_visibility='onchange', size=128, required=True, select=True)
    task_ids = fields.Many2many('project.task', string=u'Цели')
    state = fields.Selection([('draft', 'Черновик'),
                              ('approved', 'Утвержден'),
                              ('current', 'Текущий'),
                              ('canceled', 'Отменен'),
                              ], 'Статус', readonly=True, default='draft')


# class Task(models.Model):
#
#     _inherit = 'project.task'

