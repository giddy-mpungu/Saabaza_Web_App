from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.common.apps import AppsaabazaAppConfig


class LockManagerApp(AppsaabazaAppConfig):
    has_tests = True
    name = 'appsaabaza.apps.lock_manager'
    verbose_name = _('Lock manager')
