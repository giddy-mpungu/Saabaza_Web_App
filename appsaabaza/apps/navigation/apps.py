from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.common.apps import AppsaabazaAppConfig


class NavigationApp(AppsaabazaAppConfig):
    has_tests = True
    name = 'appsaabaza.apps.navigation'
    verbose_name = _('Navigation')
