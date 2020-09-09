from django.utils.translation import ugettext_lazy as _

from drf_yasg import openapi

import appsaabaza
from appsaabaza.apps.common.settings import setting_project_title

openapi_info = openapi.Info(
    title=_('%s API') % setting_project_title.value,
    default_version='v2',
    description=appsaabaza.__description__,
    license=openapi.License(name=appsaabaza.__license__),
)
