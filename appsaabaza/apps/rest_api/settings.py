from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.smart_settings.classes import Namespace

namespace = Namespace(
    label=_('REST API'), name='rest_api', version='0001'
)

setting_disable_links = namespace.add_setting(
    global_name='REST_API_DISABLE_LINKS', default=False,
    help_text=_(
        'Disable the REST API links in the tools menu.'
    ),
)
