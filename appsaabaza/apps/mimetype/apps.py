from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.common.apps import AppsaabazaAppConfig


class MIMETypesApp(AppsaabazaAppConfig):
    name = 'appsaabaza.apps.mimetype'
    has_tests = True
    verbose_name = _('MIME types')

    def ready(self, *args, **kwargs):
        super(MIMETypesApp, self).ready(*args, **kwargs)
