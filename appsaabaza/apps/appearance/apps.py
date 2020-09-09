from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.common.apps import AppsaabazaAppConfig


class AppearanceApp(AppsaabazaAppConfig):
    app_url = 'appearance'
    has_static_media = True
    has_tests = True
    name = 'appsaabaza.apps.appearance'
    verbose_name = _('Appearance')

    def ready(self):
        super(AppearanceApp, self).ready()
