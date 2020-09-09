from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.task_manager.classes import CeleryQueue
from appsaabaza.apps.task_manager.workers import worker_slow

queue_statistics = CeleryQueue(
    label=_('Statistics'), name='statistics', transient=True, worker=worker_slow
)

task_execute_statistic = queue_statistics.add_task_type(
    label=_('Execute statistic'),
    dotted_path='appsaabaza.apps.appsaabaza_statistics.tasks.task_execute_statistic'
)
