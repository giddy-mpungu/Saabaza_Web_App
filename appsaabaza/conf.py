"""
This module should be called settings.py but is named conf.py to avoid a
clash with the appsaabaza/settings/* module
"""
from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.smart_settings.classes import Namespace

namespace = Namespace(name='appsaabaza', label=_('Appsaabaza'))

setting_celery_class = namespace.add_setting(
    help_text=_('The class used to instantiate the main Celery app.'),
    global_name='APPSAABAZA_CELERY_CLASS',
    default='celery.Celery'
)
