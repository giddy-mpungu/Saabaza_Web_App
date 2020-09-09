from django.apps import apps
from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.acls.classes import ModelPermission
from appsaabaza.apps.common.apps import AppsaabazaAppConfig
from appsaabaza.apps.common.menus import menu_facet

from .links import link_document_template_sandbox
from .permissions import permission_template_sandbox


class TemplatingApp(AppsaabazaAppConfig):
    app_namespace = 'templating'
    app_url = 'templating'
    has_static_media = True
    has_tests = True
    name = 'appsaabaza.apps.templating'
    verbose_name = _('Templating')

    def ready(self):
        super(TemplatingApp, self).ready()
        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        ModelPermission.register(
            model=Document, permissions=(
                permission_template_sandbox,
            )
        )

        menu_facet.bind_links(
            links=(
                link_document_template_sandbox,
            ), sources=(Document,)
        )
