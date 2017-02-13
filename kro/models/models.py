# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Project(models.Model):
    _inherit = 'project.project'
    problem_ids = fields.One2many('kro.problem', 'kro_project_id', ondelete="cascade",  string=u'Проблемы')
    use_tasks = fields.Boolean(default=False)


class Problem(models.Model):
    _name = 'kro.problem'
    _inherit = 'project.task'

    kro_project_id = fields.Many2one('project.project', u'Проект', readonly=True)
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
    reason_correction = fields.Text(u'Причина коррекции')
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
    date_start = fields.Datetime(u'Дата начала')
    date_end = fields.Datetime(u'Дата завершения')
    problem_id = fields.Many2one('kro.problem', u'Проблема', ondelete='set null', readonly=True)
    project_id = fields.Many2one(related='problem_id.kro_project_id', readonly=True, string=u'Проект')
    priority = fields.Selection([('0', u'Низкий'), ('1', u'Средний'), ('2', u'Высокий')], u'Приоритет', select=True)
    reason_aside_problem = fields.Many2one('kro.problem', u'Причина откладывания - проблема', select=True, ondelete='set null')
    reason_aside_aim = fields.Many2one('kro.aim', u'Причина откладывания - цель', select=True, ondelete='set null')
    reason_aside_task = fields.Many2one('project.task', u'Причина откладывания - задача', select=True, ondelete='set null')
    reason_correction = fields.Text(u'Причина коррекции')
    user_id = fields.Many2one('res.users', u'Ответственный за планирование', select=True, track_visibility='onchange')
    job_ids = fields.One2many('kro.job', 'aim_id', ondelete="cascade", string=u'Задачи')
    task_ids = fields.One2many('project.task', 'aim_id', ondelete="cascade", string=u'Задания')
    task_count = fields.Integer(compute='_task_count')
    state = fields.Selection([('plan', u'Планирование'),
                              ('defined', u'Определена'),
                              ('corrections', u'Коррекция'),
                              ('finished', u'Завершена'),
                              ], u'Статус', readonly=True, default='plan')

    @api.model
    def action_tasks(self, active_id):
        search_view = self.env['ir.model.data'].get_object_reference('kro', 'kro_aim_all_tasks')
        view_id = self.env['ir.model.data'].get_object_reference('kro', 'kro_aim_task_search_form')
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
    date_start = fields.Datetime(u'Дата начала')
    date_end = fields.Datetime(u'Дата завершения')
    priority = fields.Selection([('0', u'Низкий'), ('1', u'Средний'), ('2', u'Высокий')], u'Приоритет', select=True)
    aim_id = fields.Many2one('kro.aim', u'Цель', ondelete='set null', readonly=True)
    problem_id = fields.Many2one(related='aim_id.problem_id', string=u'Проблема', readonly=True)
    project_id = fields.Many2one(related='problem_id.kro_project_id', string=u'Проект', readonly=True)
    user_id = fields.Many2one('res.users', u'Ответственный за планирование', select=True, track_visibility='onchange')
    task_ids = fields.One2many('project.task', 'job_id', ondelete="cascade", string=u'Задания')
    task_count = fields.Integer(compute='_task_count')
    total_time = fields.Integer(compute='_total_time', string=u'Затраченное время')
    reason_aside_problem = fields.Many2one('kro.problem', u'Причина откладывания - проблема', select=True, ondelete='set null')
    reason_aside_aim = fields.Many2one('kro.aim', u'Причина откладывания - цель', select=True, ondelete='set null')
    reason_aside_task = fields.Many2one('project.task', u'Причина откладывания - задача', select=True, ondelete='set null')
    reason_correction = fields.Text(u'Причина коррекции')
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

    @api.model
    def _total_time(self, ids):
        if 1:
            return False
        return True


class Task(models.Model):
    _inherit = 'project.task'
    _description = u'Задание'
    date_start_ex = fields.Datetime(u'Старт')
    date_end_ex = fields.Datetime(u'Финиш')
    date_start_pr = fields.Datetime(u'Старт')
    date_end_pr = fields.Datetime(u'Финиш')
    date_start_ap = fields.Datetime(u'Старт')
    date_end_ap = fields.Datetime(u'Финиш')
    job_id = fields.Many2one('kro.job', string=u'Задача', readonly=True)
    aim_id = fields.Many2one('kro.aim', string=u'Цель', readonly=True)
    job_aim_id = fields.Many2one(related='job_id.aim_id', string=u'Цель от задачи', readonly=True)
    problem_id = fields.Many2one(related='job_aim_id.problem_id', string=u'Проблема', readonly=True)
    project_id = fields.Many2one(related='job_aim_id.problem_id.kro_project_id', string=u'Проект', readonly=True)
    required_result = fields.Text(u'Требуемый результат')
    priority = fields.Selection([('0', u'Низкий'), ('1', u'Средний'), ('2', u'Высокий')], u'Priority', select=True)
    user_executor_id = fields.Many2one('res.users', string=u'Исполнитель')
    user_predicator_id = fields.Many2one('res.users', string=u'Утверждающий')
    user_approver_id = fields.Many2one('res.users', string=u'Подтверждающий')
    approved_by_executor = fields.Boolean(u'Согласовал исполнитель')
    approved_by_predicator = fields.Boolean(u'Согласовал утверждающий')
    approved_by_approver = fields.Boolean(u'Согласовал подтверждающий')
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
