from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.permissions import PermissionNamespace

namespace = PermissionNamespace(label=_('Events'), name='events')

permission_events_view = namespace.add_permission(
    label=_('Access the events of an object'), name='events_view'
)
