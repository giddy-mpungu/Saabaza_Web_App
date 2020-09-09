from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.common.apps import AppsaabazaAppConfig

from .handlers import handler_auto_admin_account_password_change


class AutoAdminAppConfig(AppsaabazaAppConfig):
    has_tests = True
    name = 'appsaabaza.apps.autoadmin'
    verbose_name = _('Auto administrator')

    def ready(self):
        super(AutoAdminAppConfig, self).ready()

        post_save.connect(
            dispatch_uid='autoadmin_handler_account_password_change',
            receiver=handler_auto_admin_account_password_change,
            sender=settings.AUTH_USER_MODEL
        )
