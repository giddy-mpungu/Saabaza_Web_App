from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.common.apps import AppsaabazaAppConfig


class DashboardsApp(AppsaabazaAppConfig):
    app_namespace = 'dashboards'
    app_url = 'dashboards'
    has_rest_api = False
    has_tests = False
    name = 'appsaabaza.apps.dashboards'
    verbose_name = _('Dashboards')
