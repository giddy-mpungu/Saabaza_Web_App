from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.common.apps import AppsaabazaAppConfig
from appsaabaza.apps.common.html_widgets import TwoStateWidget
from appsaabaza.apps.common.menus import menu_secondary, menu_setup, menu_object
from appsaabaza.apps.navigation.classes import SourceColumn

from .classes import Namespace, Setting
from .links import (
    link_namespace_detail, link_namespace_list, link_namespace_root_list,
    link_setting_edit
)
from .widgets import setting_widget


class SmartSettingsApp(AppsaabazaAppConfig):
    app_namespace = 'settings'
    app_url = 'settings'
    has_tests = True
    name = 'appsaabaza.apps.smart_settings'
    verbose_name = _('Smart settings')

    def ready(self):
        super(SmartSettingsApp, self).ready()

        Namespace.initialize()

        SourceColumn(
            func=lambda context: len(context['object'].settings),
            label=_('Setting count'), include_label=True, source=Namespace
        )
        SourceColumn(
            func=lambda context: setting_widget(context['object']),
            label=_('Name'), is_identifier=True, source=Setting
        )
        SourceColumn(
            attribute='serialized_value', include_label=True,
            label=_('Value'), source=Setting
        )
        SourceColumn(
            attribute='is_overridden', include_label=True, source=Setting,
            widget=TwoStateWidget
        )

        menu_object.bind_links(
            links=(link_namespace_detail,), sources=(Namespace,)
        )
        menu_object.bind_links(
            links=(link_setting_edit,), sources=(Setting,)
        )
        menu_secondary.bind_links(
            links=(link_namespace_root_list,), sources=(
                Namespace, Setting, 'settings:namespace_list',
            )
        )
        menu_setup.bind_links(links=(link_namespace_list,))

        Setting.save_last_known_good()
