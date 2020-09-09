from django.apps import apps
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.common.apps import AppsaabazaAppConfig

from .handlers import handler_document_cache_delete, handler_node_cache_delete


class MirroringApp(AppsaabazaAppConfig):
    has_tests = True
    name = 'appsaabaza.apps.mirroring'
    verbose_name = _('Mirroring')

    def ready(self):
        super(MirroringApp, self).ready()

        Document = apps.get_model(app_label='documents', model_name='Document')
        IndexInstanceNode = apps.get_model(
            app_label='document_indexing', model_name='IndexInstanceNode'
        )

        pre_delete.connect(
            handler_document_cache_delete,
            dispatch_uid='mirroring_handler_document_cache_delete',
            sender=Document
        )
        pre_delete.connect(
            handler_node_cache_delete,
            dispatch_uid='mirroring_handler_node_cache_delete',
            sender=IndexInstanceNode
        )
        pre_save.connect(
            handler_document_cache_delete,
            dispatch_uid='mirroring_handler_document_cache_delete',
            sender=Document
        )
        pre_save.connect(
            handler_node_cache_delete,
            dispatch_uid='mirroring_handler_node_cache_delete',
            sender=IndexInstanceNode
        )
