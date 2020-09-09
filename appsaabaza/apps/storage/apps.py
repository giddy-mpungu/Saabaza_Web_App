from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.common.apps import AppsaabazaAppConfig

from .classes import DefinedStorage


class StorageApp(AppsaabazaAppConfig):
    has_tests = True
    name = 'appsaabaza.apps.storage'
    verbose_name = _('Storage')

    def ready(self):
        super(StorageApp, self).ready()
        DefinedStorage.initialize()
