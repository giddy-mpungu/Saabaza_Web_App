from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.acls.classes import ModelPermission
from appsaabaza.apps.acls.links import link_acl_list
from appsaabaza.apps.acls.permissions import permission_acl_edit, permission_acl_view
from appsaabaza.apps.common.apps import AppsaabazaAppConfig
from appsaabaza.apps.common.menus import (
    menu_list_facet, menu_multi_item, menu_object, menu_secondary, menu_tools
)
from appsaabaza.apps.events.classes import EventModelRegistry, ModelEventType
from appsaabaza.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list
)
from appsaabaza.apps.navigation.classes import SourceColumn

from .events import event_cache_edited, event_cache_purged
from .links import (
    link_caches_list, link_cache_multiple_purge, link_cache_purge
)
from .permissions import permission_cache_purge, permission_cache_view


class FileCachingConfig(AppsaabazaAppConfig):
    app_namespace = 'file_caching'
    app_url = 'file_caching'
    has_tests = True
    name = 'appsaabaza.apps.file_caching'
    verbose_name = _('File caching')

    def ready(self):
        super(FileCachingConfig, self).ready()

        Cache = self.get_model(model_name='Cache')

        EventModelRegistry.register(model=Cache)

        ModelEventType.register(
            event_types=(event_cache_edited, event_cache_purged,),
            model=Cache
        )

        ModelPermission.register(
            model=Cache, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_cache_purge, permission_cache_view
            )
        )

        SourceColumn(
            attribute='label', is_identifier=True, source=Cache
        )
        SourceColumn(
            attribute='get_maximum_size_display', include_label=True,
            is_sortable=True, sort_field='maximum_size', source=Cache
        )
        SourceColumn(
            attribute='get_total_size_display', include_label=True,
            source=Cache
        )

        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_events_for_object,
                link_object_event_types_user_subcriptions_list,
            ), sources=(Cache,)
        )

        menu_object.bind_links(
            links=(link_cache_purge,),
            sources=(Cache,)
        )
        menu_multi_item.bind_links(
            links=(link_cache_multiple_purge,),
            sources=(Cache,)
        )
        menu_secondary.bind_links(
            links=(link_caches_list,), sources=(
                Cache,
            )
        )

        menu_tools.bind_links(links=(link_caches_list,))
