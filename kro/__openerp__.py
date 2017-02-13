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
        'reminder_task_deadline',
        'project_gantt8',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}