from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.common.apps import AppsaabazaAppConfig
from appsaabaza.apps.common.menus import menu_object, menu_secondary, menu_tools
from appsaabaza.apps.navigation.classes import SourceColumn

from .classes import StatisticLineChart, StatisticNamespace
from .links import (
    link_execute, link_namespace_details, link_namespace_list,
    link_statistics, link_view
)
from .tasks import task_execute_statistic  # NOQA - Force registration of task


class StatisticsApp(AppsaabazaAppConfig):
    app_namespace = 'statistics'
    app_url = 'statistics'
    has_static_media = True
    has_tests = True
    name = 'appsaabaza.apps.appsaabaza_statistics'
    verbose_name = _('Statistics')

    def ready(self):
        super(StatisticsApp, self).ready()

        SourceColumn(
            attribute='schedule',
            # Translators: Schedule here is a noun, the 'schedule' at
            # which the statistic will be updated
            include_label=True, label=_('Schedule'),
            source=StatisticLineChart
        )

        SourceColumn(
            attribute='get_last_update', include_label=True,
            label=_('Last update'), source=StatisticLineChart
        )

        menu_object.bind_links(
            links=(link_execute, link_view), sources=(StatisticLineChart,)
        )
        menu_object.bind_links(
            links=(link_namespace_details,), sources=(StatisticNamespace,)
        )
        menu_secondary.bind_links(
            links=(link_namespace_list,),
            sources=(StatisticNamespace, 'statistics:namespace_list')
        )
        menu_tools.bind_links(links=(link_statistics,))
