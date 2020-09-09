from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.common.queues import queue_tools
from appsaabaza.apps.task_manager.classes import CeleryQueue
from appsaabaza.apps.task_manager.workers import worker_medium

queue_indexing = CeleryQueue(label=_('Indexing'), name='indexing', worker=worker_medium)

queue_indexing.add_task_type(
    label=_('Delete empty index nodes'),
    dotted_path='appsaabaza.apps.document_indexing.tasks.task_delete_empty'
)
queue_indexing.add_task_type(
    label=_('Remove document'),
    dotted_path='appsaabaza.apps.document_indexing.tasks.task_remove_document'
)
queue_indexing.add_task_type(
    label=_('Index document'),
    dotted_path='appsaabaza.apps.document_indexing.tasks.task_index_document'
)
queue_tools.add_task_type(
    label=_('Rebuild index'),
    dotted_path='appsaabaza.apps.document_indexing.tasks.task_rebuild_index'
)