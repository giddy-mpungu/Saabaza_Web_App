from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.navigation.classes import Link

from .icons import (
    icon_namespace_detail, icon_namespace_list, icon_setting_edit
)
from .permissions import permission_settings_edit, permission_settings_view

link_namespace_list = Link(
    icon_class=icon_namespace_list, permissions=(permission_settings_view,),
    text=_('Settings'), view='settings:namespace_list'
)
link_namespace_detail = Link(
    args='resolved_object.name', icon_class=icon_namespace_detail,
    permissions=(permission_settings_view,), text=_('Settings'),
    view='settings:namespace_detail'
)
# Duplicate the link to use a different name
link_namespace_root_list = Link(
    icon_class=icon_namespace_list, permissions=(permission_settings_view,),
    text=_('Namespaces'), view='settings:namespace_list'
)
link_setting_edit = Link(
    args='resolved_object.global_name', icon_class=icon_setting_edit,
    permissions=(permission_settings_edit,), text=_('Edit'),
    view='settings:setting_edit_view'
)