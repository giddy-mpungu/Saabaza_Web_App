from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.common.apps import AppsaabazaAppConfig
from appsaabaza.apps.common.menus import menu_facet, menu_secondary

from .links import link_search, link_search_advanced, link_search_again


class DynamicSearchApp(AppsaabazaAppConfig):
    app_namespace = 'search'
    app_url = 'search'
    has_rest_api = True
    has_tests = True
    name = 'appsaabaza.apps.dynamic_search'
    verbose_name = _('Dynamic search')

    def ready(self):
        super(DynamicSearchApp, self).ready()

        menu_facet.bind_links(
            links=(link_search, link_search_advanced),
            sources=(
                'search:search', 'search:search_advanced', 'search:results'
            )
        )
        menu_secondary.bind_links(
            links=(link_search_again,), sources=('search:results',)
        )
