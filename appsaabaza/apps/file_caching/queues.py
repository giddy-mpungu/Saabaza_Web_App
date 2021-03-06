from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.common.queues import queue_tools

queue_tools.add_task_type(
    dotted_path='appsaabaza.apps.file_caching.tasks.task_cache_purge',
    label=_('Purge a file cache')
)
