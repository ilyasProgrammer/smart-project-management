# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'
    problem_ids = fields.Many2many('kro.problem', ondelete="cascade",  string=u'Проблемы')


class Problem(models.Model):
    _name = 'kro.problem'
    _inherit = 'project.task'

    kro_project_id = fields.Many2one('kro.project', u'Проект', select=True)
    # date_deadline = fields.Date(u'Плановая дата решения', select=True, copy=False)
    fact_date = fields.Date(u'Фактическая дата', select=True)
    # user_id = fields.Many2one('res.users', 'Инициатор', select=True, track_visibility='onchange')
    priority = fields.Selection([('0', u'Низкий'), ('1', u'Средний'), ('2', u'Высокий')], u'Приоритет', select=True)
    user_aim_id = fields.Many2one('res.users', u'Ответственный за определение целей', select=True, track_visibility='onchange')
    user_admin_id = fields.Many2one('res.users', u'Администратор', select=True, track_visibility='onchange')
    description = fields.Html(u'Формулировка проблемы')
    effects = fields.Text(u'Последствия')
    causes = fields.Text(u'Причины')
    decision = fields.Text(u'Решение')
    reason_aside_problem = fields.Many2one('kro.problem', u'Причина откладывания - проблема', select=True)
    reason_aside_aim = fields.Many2one('kro.aim', u'Причина откладывания - цель', select=True)
    reason_aside_task = fields.Many2one('kro.task', u'Причина откладывания - задача', select=True)
    aim_ids = fields.One2many('kro.aim', 'problem_id', ondelete="cascade", string=u'Цели')
    state = fields.Selection([('draft', u'Черновик'),
                              ('approved', u'Утвержден'),
                              ('current', u'Текущий'),
                              ('canceled', u'Отменен'),
                              ], u'Статус', readonly=True, default='draft')

    @api.model
    def _store_history(self, ids):
        if 1:
            return False
        return True


class Aim(models.Model):
    _name = 'kro.aim'
    _inherit = 'project.task'

    priority = fields.Selection([('0', u'Низкий'), ('1', u'Средний'), ('2', u'Высокий')], u'Приоритет', select=True)
    problem_id = fields.Many2one('kro.problem', u'Проблема')
    # project_id = fields.Many2one(related='problem_id.project_id', readonly=True)
    # date_deadline = fields.Date(u'Срок планирования', select=True, copy=False)
    # name = fields.Char(u'Заголовок', track_visibility='onchange', size=128, select=True)
    user_plan_id = fields.Many2one('res.users', u'Ответственный за планирование', select=True, track_visibility='onchange')
    task_ids = fields.One2many('project.task', 'aim_id', ondelete="cascade", string=u'Задачи')
    state = fields.Selection([('draft', u'Черновик'),
                              ('approved', u'Утвержден'),
                              ('current', u'Текущий'),
                              ('canceled', u'Отменен'),
                              ], u'Статус', readonly=True, default='draft')

    @api.model
    def _store_history(self, ids):
        if 1:
            return False
        return True


class Task(models.Model):
    _inherit = 'project.task'

    aim_id = fields.Many2one('kro.aim')
    project_id = fields.Many2one(related='aim_id.project_id', readonly=True, string=u'Проект')
    problem_id = fields.Many2one(related='aim_id.problem_id', readonly=True, string=u'Проблема')
    priority = fields.Selection([('0', u'Низкий'), ('1', u'Средний'), ('2', u'Высокий')], u'Priority', select=True)
    user_plan_id = fields.Many2one('res.users', u'Ответственный за планирование', select=True, track_visibility='onchange')

    @api.model
    def _store_history(self, ids):
        if 1:
            return False
        return True
