from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.common.apps import AppsaabazaAppConfig


class PlatformApp(AppsaabazaAppConfig):
    app_namespace = 'platform'
    app_url = 'platform'
    has_rest_api = False
    has_tests = True
    name = 'appsaabaza.apps.platform'
    verbose_name = _('Platform')

    def ready(self):
        super(PlatformApp, self).ready()
