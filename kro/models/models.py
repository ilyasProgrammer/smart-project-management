# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'
    problem_ids = fields.Many2many('kro.problem', ondelete="cascade",  string=u'Проблемы')


class Problem(models.Model):
    _name = 'kro.problem'
    _inherit = 'project.task'

    kro_project_id = fields.Many2one('project.project', u'Проект', select=True)
    date_deadline = fields.Date(u'Плановая дата решения', select=True, copy=False)
    fact_date = fields.Date(u'Фактическая дата', select=True)
    # user_id = fields.Many2one('res.users', 'Инициатор', select=True, track_visibility='onchange')
    priority = fields.Selection([('0', u'Низкий'), ('1', u'Средний'), ('2', u'Высокий')], u'Приоритет', select=True)
    user_aim_id = fields.Many2one('res.users', u'Ответственный за определение целей', select=True, track_visibility='onchange', ondelete='set null')
    # user_admin_id = fields.Many2one('res.users', u'Администратор', select=True, track_visibility='onchange')
    addressee_id = fields.Many2one('res.users', u'Адресат', select=True, track_visibility='onchange', ondelete='set null')
    description = fields.Html(u'Формулировка проблемы')
    effects = fields.Text(u'Последствия')
    causes = fields.Text(u'Причины')
    decision = fields.Text(u'Решение')
    reason_aside_problem = fields.Many2one('kro.problem', u'Причина откладывания - проблема', select=True, ondelete='set null')
    reason_aside_aim = fields.Many2one('kro.aim', u'Причина откладывания - цель', select=True, ondelete='set null')
    reason_aside_task = fields.Many2one('project.task', u'Причина откладывания - задача', select=True, ondelete='set null')
    aim_ids = fields.One2many('kro.aim', 'problem_id', ondelete="cascade", string=u'Цели')
    # stage_id = fields.Many2one('project.task.type', u'Статус', track_visibility='onchange', select=True, domain="[('project_ids', '=', project_id)]", copy=False),
    state = fields.Selection([('plan', u'Планирование'),
                              ('moved', u'Передана'),
                              ('process', u'Обрабатывается'),
                              ('taken', u'Принята'),
                              ('suspended', u'Отложена'),
                              ('canceled', u'Отклонена'),
                              ('closed', u'Закрыта'),
                              ], u'Статус',  default='plan')

    @api.model
    def _store_history(self, ids):
        if 1:
            return False
        return True


class Aim(models.Model):
    _name = 'kro.aim'
    _inherit = 'project.task'

    priority = fields.Selection([('0', u'Низкий'), ('1', u'Средний'), ('2', u'Высокий')], u'Приоритет', select=True)
    problem_id = fields.Many2one('kro.problem', u'Проблема', ondelete='set null')
    # project_id = fields.Many2one(related='problem_id.project_id', readonly=True)
    # date_deadline = fields.Date(u'Срок планирования', select=True, copy=False)
    # name = fields.Char(u'Заголовок', track_visibility='onchange', size=128, select=True)
    user_id = fields.Many2one('res.users', u'Ответственный за планирование', select=True, track_visibility='onchange')
    job_ids = fields.Many2many('kro.job',   ondelete="cascade", string=u'Задачи')
    task_ids = fields.Many2many('project.task',  ondelete="cascade", string=u'Задания')
    task_count = fields.Integer(compute='_task_count')
    state = fields.Selection([('plan', u'Планирование'),
                              ('defined', u'Определена'),
                              ('corrections', u'Коррекция'),
                              ('finished', u'Завершена'),
                              ], u'Статус', readonly=True, default='plan')

    @api.model
    def action_tasks(self, active_id):
        search_view = self.env['ir.model.data'].get_object_reference('kro', 'act_task_all')
        view_id = self.env['ir.model.data'].get_object_reference('kro', 'kro_task_search_form')
        aim = self.env['kro.aim'].browse(active_id)
        job_tasks_ids = []
        for r in aim.job_ids:
            for t in r.task_ids:
                job_tasks_ids.append(t.id)
        value = {
            'domain': [('id', 'in', [rec.id for rec in aim.task_ids]+job_tasks_ids)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'project.task',
            'res_id': False,
            'view_id': False,
            'context': {},
            'type': 'ir.actions.act_window',
            # 'target': 'inlineview',
            'search_view_id': search_view and search_view[1] or False
        }
        return value

    @api.one
    def _task_count(self):
        job_tasks_ids = []
        for r in self.job_ids:
            for t in r.task_ids:
                job_tasks_ids.append(t.id)
        self.task_count = len(self.task_ids.ids+job_tasks_ids)

    @api.model
    def _store_history(self, ids):
        if 1:
            return False
        return True


class Job(models.Model):
    _name = 'kro.job'
    _inherit = 'project.task'
    _description = u'Задача'

    priority = fields.Selection([('0', u'Низкий'), ('1', u'Средний'), ('2', u'Высокий')], u'Приоритет', select=True)
    problem_id = fields.Many2one('kro.problem', u'Проблема', ondelete='set null')
    user_id = fields.Many2one('res.users', u'Ответственный за планирование', select=True, track_visibility='onchange')
    task_ids = fields.Many2many('project.task', ondelete="cascade", string=u'Задания')
    task_count = fields.Integer(compute='_task_count')
    state = fields.Selection([('plan', u'Планирование'),
                              ('defined', u'Определена'),
                              ('corrections', u'Отложена'),
                              ('corrections', u'Коррекция'),
                              ('finished', u'Завершена'),
                              ], u'Статус', readonly=True, default='plan')

    @api.model
    def _store_history(self, ids):
        if 1:
            return False
        return True



class Task(models.Model):
    _inherit = 'project.task'
    _description = u'Задание'

    # aim_id = fields.Many2one('kro.aim')
    # project_id = fields.Many2one(related='aim_id.project_id', readonly=True, string=u'Проект')
    # problem_id = fields.Many2one(related='aim_id.problem_id', readonly=True, string=u'Проблема')
    priority = fields.Selection([('0', u'Низкий'), ('1', u'Средний'), ('2', u'Высокий')], u'Priority', select=True)
    user_plan_id = fields.Many2one('res.users', u'Ответственный за планирование', select=True, track_visibility='onchange')
    state = fields.Selection([('plan', u'Планирование'),
                              ('moved', u'Согласование'),
                              ('process', u'Назначено'),
                              ('taken', u'Выполнение'),
                              ('suspended', u'Утверждение'),
                              ('canceled', u'Утверждено'),
                              ('closed', u'Подтверждение'),
                              ('closed', u'Подтверждено'),
                              ('closed', u'Завершено'),
                              ('closed', u'Коррекция'),
                              ], u'Статус',  default='plan')


class Event(models.Model):
    _inherit = 'calendar.event'

    approver_id = fields.Many2one('res.users', u'Утверждающий', select=True, track_visibility='onchange', ondelete='set null')
    user_plan_id = fields.Many2one('res.users', u'Ответственный за планирование', select=True, track_visibility='onchange', ondelete='set null')
    project_id = fields.Many2one('project.project', u'Связанный проект', select=True, ondelete='set null')
    problem_id = fields.Many2one('kro.problem', u'Связанная проблема', select=True, ondelete='set null')
    aim_id = fields.Many2one('kro.aim', u'Связанная цель', select=True, ondelete='set null')
    task_id = fields.Many2one('project.task', u'Связанная задача', select=True, ondelete='set null')
    points = fields.Text(u'Цели')
    expectations = fields.Text(u'Требуемые результаты')
    state = fields.Selection([('plan', u'Планирование'),
                              ('agreement', u'Согласование'),
                              ('set', u'Назначена'),
                              ('agreed', u'Утверждение'),
                              ('done', u'Проведена'),
                              ('approved', u'Утверждена'),
                              ('closed', u'Завершена'),
                              ], u'Статус',  default='plan')