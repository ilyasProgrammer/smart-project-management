# -*- coding: utf-8 -*-
{
    'name': "kro project",
    'description': """KRO PROJECT""",
    'author': "Ilyas",
    'website': "https://github.com/ilyasProgrammer",
    'category': 'Project',
    'version': '1.0',
    'depends': [
        'project',
        'calendar',
        # 'reminder_task_deadline',
        'project_gantt8',
        'project_timesheet',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'data/task_sequence.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    "pre_init_hook": "create_code_equal_to_id",
    "post_init_hook": "assign_old_sequences",
}