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

    aim_ids = fields.One2many('kro.aim', 'problem_id', string=u'Цели')
    state = fields.Selection([('draft', 'Черновик'),
                              ('approved', 'Утвержден'),
                              ('current', 'Текущий'),
                              ('canceled', 'Отменен'),
                              ], 'Статус', readonly=True, default='draft')


class Aim(models.Model):

    _name = 'kro.aim'
    _inherit = 'project.task'

    priority = fields.Selection([('0', 'Низкий'), ('1', 'Средний'), ('2', 'Высокий')], 'Priority', select=True)
    problem_id = fields.Many2one('kro.problem', string='Проблема')
    project_id = fields.Many2one(related='problem_id.project_id', readonly=True)
    date_deadline = fields.Date('Срок планирования', select=True, copy=False)
    name = fields.Char(u'Заголовок', track_visibility='onchange', size=128, required=True, select=True)
    user_plan_id = fields.Many2one('res.users', 'Ответственный за планирование', select=True, track_visibility='onchange')
    task_ids = fields.One2many('project.task', 'aim_id', string=u'Задачи')
    state = fields.Selection([('draft', 'Черновик'),
                              ('approved', 'Утвержден'),
                              ('current', 'Текущий'),
                              ('canceled', 'Отменен'),
                              ], 'Статус', readonly=True, default='draft')


class Task(models.Model):

    _inherit = 'project.task'

    aim_id = fields.Many2one('kro.aim')
    project_id = fields.Many2one(related='aim_id.project_id', readonly=True, string='Проект')
    problem_id = fields.Many2one(related='aim_id.problem_id', readonly=True, string='Проблема')
    priority = fields.Selection([('0', 'Низкий'), ('1', 'Средний'), ('2', 'Высокий')], 'Priority', select=True)
    user_plan_id = fields.Many2one('res.users', 'Ответственный за планирование', select=True, track_visibility='onchange')