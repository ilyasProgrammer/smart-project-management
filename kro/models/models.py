# -*- coding: utf-8 -*-

from openerp import models, fields, api
import datetime


class Project(models.Model):
    _inherit = 'project.project'
    problem_ids = fields.One2many('kro.problem', 'kro_project_id', ondelete='set null',  string=u'Проблемы')
    use_tasks = fields.Boolean(default=False)


class Problem(models.Model):
    _name = 'kro.problem'
    _inherit = 'project.task'

    kro_project_id = fields.Many2one('project.project', u'Проект', readonly=True, ondelete="set null")
    date_deadline = fields.Date(u'Плановая дата решения', select=True, copy=False, track_visibility='always')
    fact_date = fields.Date(u'Фактическая дата', select=True, track_visibility='always')
    # user_id = fields.Many2one('res.users', 'Инициатор', select=True, track_visibility='onchange')
    priority = fields.Selection([('0', u'Низкий'), ('1', u'Средний'), ('2', u'Высокий')], u'Приоритет', select=True, track_visibility='always')
    user_aim_id = fields.Many2one('res.users', u'Ответственный за определение целей', select=True, track_visibility='onchange', ondelete='set null')
    # user_admin_id = fields.Many2one('res.users', u'Администратор', select=True, track_visibility='onchange')
    addressee_id = fields.Many2one('res.users', u'Адресат', select=True, track_visibility='onchange', ondelete='set null')
    description = fields.Html(u'Формулировка проблемы', track_visibility='always')
    effects = fields.Text(u'Последствия', track_visibility='always')
    causes = fields.Text(u'Причины', track_visibility='always')
    decision = fields.Text(u'Решение', track_visibility='always')
    reason_aside_problem = fields.Many2one('kro.problem', u'Причина откладывания - проблема', select=True, ondelete='set null', track_visibility='always')
    reason_aside_aim = fields.Many2one('kro.aim', u'Причина откладывания - цель', select=True, ondelete='set null', track_visibility='always')
    reason_aside_task = fields.Many2one('project.task', u'Причина откладывания - задача', select=True, ondelete='set null', track_visibility='always')
    reason_correction = fields.Text(u'Причина коррекции', track_visibility='always')
    aim_ids = fields.One2many('kro.aim', 'problem_id', ondelete="cascade", string=u'Цели', track_visibility='always')
    # stage_id = fields.Many2one('project.task.type', u'Статус', track_visibility='onchange', select=True, domain="[('project_ids', '=', project_id)]", copy=False),
    state = fields.Selection([('plan', u'Планирование'),
                              ('moved', u'Передана'),
                              ('process', u'Обрабатывается'),
                              ('taken', u'Принята'),
                              ('suspended', u'Отложена'),
                              ('canceled', u'Отклонена'),
                              ('closed', u'Закрыта'),
                              ], u'Статус',  default='plan', track_visibility='always')
    remaining_hours = fields.Boolean()
    effective_hours = fields.Boolean()
    total_hours = fields.Boolean()
    progress = fields.Boolean()
    delay_hours = fields.Boolean()
    timesheet_ids = fields.Boolean()
    analytic_account_id = fields.Boolean()

    @api.model
    def _store_history(self, ids):
        if 1:
            return False
        return True

    @api.model
    def _hours_get(self, ids):
        return


class Aim(models.Model):
    _name = 'kro.aim'
    _inherit = 'project.task'
    date_start = fields.Date(string=u'Дата начала', compute='_time_count', store=True)
    date_end = fields.Date(string=u'Дата завершения', compute='_time_count', store=True)
    problem_id = fields.Many2one('kro.problem', u'Проблема', ondelete='set null', readonly=True)
    project_id = fields.Many2one(related='problem_id.kro_project_id', readonly=True, string=u'Проект', ondelete='set null')
    priority = fields.Selection([('0', u'Низкий'), ('1', u'Средний'), ('2', u'Высокий')], u'Приоритет', select=True, track_visibility='always')
    reason_aside_problem = fields.Many2one('kro.problem', u'Причина откладывания - проблема', select=True, ondelete='set null', track_visibility='always')
    reason_aside_aim = fields.Many2one('kro.aim', u'Причина откладывания - цель', select=True, ondelete='set null', track_visibility='always')
    reason_aside_task = fields.Many2one('project.task', u'Причина откладывания - задача', select=True, ondelete='set null', track_visibility='always')
    reason_correction = fields.Text(u'Причина коррекции', track_visibility='always')
    user_id = fields.Many2one('res.users', u'Ответственный за планирование', select=True, track_visibility='onchange', ondelete="set null")
    job_ids = fields.One2many('kro.job', 'aim_id', ondelete="cascade", string=u'Задачи', track_visibility='always')
    task_ids = fields.One2many('project.task', 'aim_id', ondelete="cascade", string=u'Задания', track_visibility='always')
    task_count = fields.Integer(compute='_task_count')
    state = fields.Selection([('plan', u'Планирование'),
                              ('defined', u'Определена'),
                              ('corrections', u'Коррекция'),
                              ('finished', u'Завершена'),
                              ], u'Статус', readonly=True, default='plan', track_visibility='always')
    remaining_hours = fields.Boolean()
    effective_hours = fields.Boolean()
    total_hours = fields.Boolean()
    planned_hours = fields.Float(compute='_time_count', string=u'Запланированно часов всего')
    total_time = fields.Integer(compute='_time_count', string=u'Затраченно часов всего')
    progress = fields.Float(compute='_time_count', string=u'Прогресс')
    delay_hours = fields.Boolean()
    timesheet_ids = fields.Boolean()
    analytic_account_id = fields.Boolean()

    @api.one
    @api.depends('job_ids', 'task_ids')
    def _time_count(self):
        planned_hours = 0
        total_time = 0
        planned_hours += sum([r.planned_hours for r in self.task_ids])
        total_time += sum([r.effective_hours for r in self.task_ids])
        for rec in self.job_ids:
            planned_hours += sum([r.planned_hours for r in rec.task_ids])
            total_time += sum([r.effective_hours for r in rec.task_ids])
        if total_time and planned_hours:
            self.planned_hours = planned_hours
            self.total_time = total_time
            self.progress = round(min(100.0 * total_time / planned_hours, 99.99), 2)
        start_dates = [datetime.datetime.strptime(r.date_start, '%Y-%m-%d') for r in self.task_ids if r.date_start is not False]
        end_dates = [datetime.datetime.strptime(r.date_end, '%Y-%m-%d') for r in self.task_ids if r.date_end is not False]
        start_dates += [datetime.datetime.strptime(r.date_start, '%Y-%m-%d') for r in self.job_ids if r.date_start is not False]
        end_dates += [datetime.datetime.strptime(r.date_end, '%Y-%m-%d') for r in self.job_ids if r.date_end is not False]
        if len(start_dates):
            self.date_start = min(start_dates)
        if len(end_dates):
            self.date_end = max(end_dates)
        if self.total_time and self.planned_hours:
            self.progress = round(min(100.0 * self.total_time / self.planned_hours, 99.99), 2)

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

    @api.model
    def _hours_get(self, ids):
        return


class Job(models.Model):
    _name = 'kro.job'
    _inherit = 'project.task'
    _description = u'Задача'
    date_start = fields.Date(string=u'Дата начала', compute='_time_count', store=True)
    date_end = fields.Date(string=u'Дата завершения', compute='_time_count', store=True)
    priority = fields.Selection([('0', u'Низкий'), ('1', u'Средний'), ('2', u'Высокий')], u'Приоритет', select=True, track_visibility='always')
    aim_id = fields.Many2one('kro.aim', u'Цель', ondelete='set null', readonly=True, track_visibility='always')
    problem_id = fields.Many2one(related='aim_id.problem_id', string=u'Проблема', readonly=True, ondelete="set null")
    project_id = fields.Many2one(related='problem_id.kro_project_id', string=u'Проект', readonly=True, ondelete='set null')
    user_id = fields.Many2one('res.users', u'Ответственный за планирование', select=True, track_visibility='onchange', ondelete="set null")
    task_ids = fields.One2many('project.task', 'job_id', ondelete="cascade", string=u'Задания', track_visibility='always')
    task_count = fields.Integer(compute='_task_count', string=u'Количество заданий')
    planned_hours = fields.Float(compute='_time_count', string=u'Запланированно часов всего')
    total_time = fields.Integer(compute='_time_count', string=u'Затраченно часов всего')
    reason_aside_problem = fields.Many2one('kro.problem', u'Причина откладывания - проблема', select=True, ondelete='set null', track_visibility='always')
    reason_aside_aim = fields.Many2one('kro.aim', u'Причина откладывания - цель', select=True, ondelete='set null', track_visibility='always')
    reason_aside_task = fields.Many2one('project.task', u'Причина откладывания - задача', select=True, ondelete='set null', track_visibility='always')
    reason_correction = fields.Text(u'Причина коррекции', track_visibility='always')
    state = fields.Selection([('plan', u'Планирование'),
                              ('defined', u'Определена'),
                              ('suspended', u'Отложена'),
                              ('corrections', u'Коррекция'),
                              ('finished', u'Завершена'),
                              ], u'Статус', readonly=True, default='plan', track_visibility='always')
    remaining_hours = fields.Boolean()
    effective_hours = fields.Boolean()
    total_hours = fields.Boolean()
    progress = fields.Float(compute='_time_count', string=u'Прогресс')
    delay_hours = fields.Boolean()
    timesheet_ids = fields.Boolean()
    analytic_account_id = fields.Boolean()

    @api.one
    @api.depends('task_ids')
    def _time_count(self):
        if len(self.task_ids):
            self.planned_hours = sum([r.planned_hours for r in self.task_ids])
            self.total_time = sum([r.effective_hours for r in self.task_ids])
            start_dates = [datetime.datetime.strptime(r.date_start, '%Y-%m-%d') for r in self.task_ids if r.date_start is not False]
            end_dates = [datetime.datetime.strptime(r.date_end, '%Y-%m-%d') for r in self.task_ids if r.date_end is not False]
            if len(start_dates):
                self.date_start = min(start_dates)
            if len(end_dates):
                self.date_end = max(end_dates)
            if self.total_time and self.planned_hours:
                self.progress = round(min(100.0 * self.total_time / self.planned_hours, 99.99), 2)

    @api.model
    def _store_history(self, ids):
        if 1:
            return False
        return True

    @api.model
    def _hours_get(self, ids):
        return


class Task(models.Model):
    _inherit = 'project.task'
    _description = u'Задание'
    _order = 'code'
    # date_start_ex = fields.Datetime(u'Старт') используем date_start для гантта
    date_start = fields.Date(u'Исполнитель дата начала', track_visibility='always')
    date_end_ex = fields.Date(u'Исполнитель дата окончания', track_visibility='onchange')
    date_start_pr = fields.Date(u'Утверждающий дата начала', track_visibility='onchange')
    date_end_pr = fields.Date(u'Утверждающий дата окончания', track_visibility='onchange')
    date_start_ap = fields.Date(u'Подтверждающий дата начала', track_visibility='onchange')
    date_end_ap = fields.Date(u'Подтверждающий дата окончания', track_visibility='always')
    date_end = fields.Date(compute='_set_date_end', track_visibility='always')
    plan_time_ex = fields.Float(u'План по времени исполнитель', track_visibility='onchange')
    plan_time_pr = fields.Float(u'План по времени утверждающий', track_visibility='onchange')
    plan_time_ap = fields.Float(u'План по времени подтверджающий', track_visibility='onchange')
    got_approver = fields.Boolean(u'С подтверждающим', track_visibility='onchange')
    amount = fields.Float(u'Бюджет', track_visibility='onchange')
    mark_state = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7')], string=u'Оценка статуса', track_visibility='onchange')
    mark_result = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7')], string=u'Оценка результата', track_visibility='onchange')
    job_id = fields.Many2one('kro.job', string=u'Задача', readonly=True, ondelete="set null")
    aim_id = fields.Many2one('kro.aim', string=u'Цель', readonly=True, ondelete="set null")
    job_aim_id = fields.Many2one(related='job_id.aim_id', string=u'Цель', readonly=True)
    problem_id = fields.Many2one(related='job_aim_id.problem_id', string=u'Проблема', readonly=True)
    project_id = fields.Many2one(related='job_aim_id.problem_id.kro_project_id', string=u'Проект', readonly=True)
    required_result = fields.Text(u'Требуемый результат', track_visibility='onchange')
    priority = fields.Selection([('0', u'Низкий'), ('1', u'Средний'), ('2', u'Высокий')], u'Приоритет', select=True, track_visibility='onchange')
    user_executor_id = fields.Many2one('res.users', string=u'Исполнитель', ondelete="set null", track_visibility='onchange')
    user_predicator_id = fields.Many2one('res.users', string=u'Утверждающий', ondelete="set null", track_visibility='onchange')
    user_approver_id = fields.Many2one('res.users', string=u'Подтверждающий', ondelete="set null", track_visibility='onchange')
    approved_by_executor = fields.Boolean(u'Согласовал исполнитель', track_visibility='onchange')
    approved_by_predicator = fields.Boolean(u'Согласовал утверждающий', track_visibility='onchange')
    approved_by_approver = fields.Boolean(u'Согласовал подтверждающий', track_visibility='onchange')
    state = fields.Selection([('plan', u'Планирование'),
                              ('agreement', u'Согласование'),
                              ('assigned', u'Назначено'),
                              ('execution', u'Выполнение'),
                              ('stating', u'Утверждение'),
                              ('stated', u'Утверждено'),
                              ('approvement', u'Подтверждение'),
                              ('approved', u'Подтверждено'),
                              ('finished', u'Завершено'),
                              ('correction', u'Коррекция'),
                              ], u'Статус',  default='plan', track_visibility='onchange')
    planned_hours = fields.Float(compute='_time_count', string=u'Запланированно часов', readonly=True)
    depend_on_ids = fields.Many2many('project.task', relation='depend_on_rel', column1='col_name1', column2='col_name2', string=u'Основание', track_visibility='onchange')
    dependent_ids = fields.Many2many('project.task', relation='dependent_rel', column1='col_name3', column2='col_name4', string=u'Зависимые', track_visibility='onchange')

    @api.one
    @api.depends('plan_time_ex', 'plan_time_pr', 'plan_time_ap')
    def _time_count(self):
        self.planned_hours = self.plan_time_ex+self.plan_time_pr+self.plan_time_ap

    @api.model
    def action_move_time(self, active_id):
        task = self.env['project.task'].browse(active_id)
        start = datetime.datetime.strptime(task.date_start, '%Y-%m-%d')
        end = datetime.datetime.strptime(task.date_end, '%Y-%m-%d')
        for dep in task.dependent_ids:
            r_start = datetime.datetime.strptime(dep.date_start, '%Y-%m-%d')
            r_end = datetime.datetime.strptime(dep.date_end, '%Y-%m-%d')
            r_diff = r_end - r_start
            if r_start < end:
                dep.date_start = task.date_end
                dep.date_end = end + r_diff
            if r_start > end:
                dep.date_start = task.date_end
                dep.date_end = end + r_diff
        for base in task.depend_on_ids:
            r_end = datetime.datetime.strptime(base.date_end, '%Y-%m-%d')
            if r_end > start:
                task.date_start = base.date_end

    @api.one
    @api.depends('date_end_ap', 'date_end_pr')
    def _set_date_end(self):
        end_date_ap = int(self.date_end_ap.replace('-', '')) if self.date_end_ap else 0
        end_date_pr = int(self.date_end_pr.replace('-', '')) if self.date_end_pr else 0
        if end_date_ap > end_date_pr:
            self.date_end = self.date_end_ap
        elif end_date_ap < end_date_pr:
            self.date_end = self.date_end_pr
