from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.task_manager.classes import CeleryQueue
from appsaabaza.apps.task_manager.workers import worker_medium

queue_metadata = CeleryQueue(
    label=_('Metadata'), name='metadata', worker=worker_medium
)
queue_metadata.add_task_type(
    label=_('Remove metadata type'),
    dotted_path='appsaabaza.apps.metadata.tasks.task_remove_metadata_type'
)
queue_metadata.add_task_type(
    label=_('Add required metadata type'),
    dotted_path='appsaabaza.apps.metadata.tasks.task_add_required_metadata_type'
)
