import logging

from django.apps import apps

from appsaabaza.apps.lock_manager.exceptions import LockError
from appsaabaza.apps.lock_manager.runtime import locking_backend
from appsaabaza.celery import app

from .literals import LOCK_EXPIRE

from .classes import FileMetadataDriver

logger = logging.getLogger(name=__name__)


@app.task(ignore_result=True)
def task_process_document_version(document_version_id):
    DocumentVersion = apps.get_model(
        app_label='documents', model_name='DocumentVersion'
    )

    document_version = DocumentVersion.objects.get(pk=document_version_id)

    lock_id = 'task_process_document_version-%d' % document_version_id
    try:
        logger.debug('trying to acquire lock: %s', lock_id)
        # Acquire lock to avoid processing the same document version more
        # than once concurrently
        lock = locking_backend.acquire_lock(name=lock_id, timeout=LOCK_EXPIRE)
        logger.debug('acquired lock: %s', lock_id)
    except LockError:
        logger.debug('unable to obtain lock: %s' % lock_id)
    else:
        FileMetadataDriver.process_document_version(
            document_version=document_version
        )
        lock.release()
