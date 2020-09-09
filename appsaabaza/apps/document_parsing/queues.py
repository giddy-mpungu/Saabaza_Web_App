from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.task_manager.classes import CeleryQueue
from appsaabaza.apps.task_manager.workers import worker_slow

queue_ocr = CeleryQueue(name='parsing', label=_('Parsing'), worker=worker_slow)
queue_ocr.add_task_type(
    dotted_path='appsaabaza.apps.document_parsing.tasks.task_parse_document_version',
    label=_('Document version parsing')
)
