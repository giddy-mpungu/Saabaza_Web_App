from django.apps import apps
from django.db.models.signals import m2m_changed, pre_delete
from django.utils.translation import ugettext_lazy as _

from appsaabaza.apps.acls.classes import ModelPermission
from appsaabaza.apps.acls.links import link_acl_list
from appsaabaza.apps.acls.permissions import permission_acl_edit, permission_acl_view
from appsaabaza.apps.common.apps import AppsaabazaAppConfig
from appsaabaza.apps.common.classes import ModelFieldRelated
from appsaabaza.apps.common.menus import (
    menu_facet, menu_list_facet, menu_main, menu_multi_item, menu_object,
    menu_secondary
)
from appsaabaza.apps.documents.search import document_page_search, document_search
from appsaabaza.apps.events.classes import EventModelRegistry, ModelEventType
from appsaabaza.apps.events.links import (
    link_events_for_object, link_object_event_types_user_subcriptions_list,
)
from appsaabaza.apps.events.permissions import permission_events_view
from appsaabaza.apps.navigation.classes import SourceColumn

from .events import (
    event_tag_attach, event_tag_edited, event_tag_remove
)
from .handlers import handler_index_document, handler_tag_pre_delete
from .html_widgets import widget_document_tags
from .links import (
    link_document_tag_list, link_document_multiple_attach_multiple_tag,
    link_document_multiple_tag_multiple_remove,
    link_document_tag_multiple_remove, link_document_tag_multiple_attach, link_tag_create,
    link_tag_delete, link_tag_edit, link_tag_list,
    link_tag_multiple_delete, link_tag_document_list
)
from .menus import menu_tags
from .methods import method_document_get_tags
from .permissions import (
    permission_tag_attach, permission_tag_delete, permission_tag_edit,
    permission_tag_remove, permission_tag_view
)
from .search import tag_search  # NOQA


class TagsApp(AppsaabazaAppConfig):
    app_namespace = 'tags'
    app_url = 'tags'
    has_rest_api = True
    has_static_media = True
    has_tests = True
    name = 'appsaabaza.apps.tags'
    verbose_name = _('Tags')

    def ready(self):
        super(TagsApp, self).ready()
        from .wizard_steps import WizardStepTags  # NOQA

        Document = apps.get_model(
            app_label='documents', model_name='Document'
        )

        DocumentPageResult = apps.get_model(
            app_label='documents', model_name='DocumentPageResult'
        )

        DocumentTag = self.get_model(model_name='DocumentTag')
        Tag = self.get_model(model_name='Tag')

        Document.add_to_class(name='get_tags', value=method_document_get_tags)

        EventModelRegistry.register(model=Tag)

        ModelEventType.register(
            model=Tag, event_types=(
                event_tag_attach, event_tag_edited, event_tag_remove
            )
        )

        ModelFieldRelated(model=Document, name='tags__label')
        ModelFieldRelated(model=Document, name='tags__color')

        ModelPermission.register(
            model=Document, permissions=(
                permission_tag_attach, permission_tag_remove,
                permission_tag_view
            )
        )

        ModelPermission.register(
            model=Tag, permissions=(
                permission_acl_edit, permission_acl_view,
                permission_events_view, permission_tag_attach,
                permission_tag_delete, permission_tag_edit,
                permission_tag_remove, permission_tag_view,
            )
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=DocumentTag
        )

        SourceColumn(
            func=lambda context: widget_document_tags(
                document=context['object'], user=context['request'].user
            ), label=_('Tags'), source=Document
        )

        SourceColumn(
            func=lambda context: widget_document_tags(
                document=context['object'].document,
                user=context['request'].user
            ), label=_('Tags'), source=DocumentPageResult
        )

        SourceColumn(
            attribute='label', is_identifier=True, is_sortable=True,
            source=Tag
        )
        SourceColumn(
            attribute='get_preview_widget', include_label=True, source=Tag
        )
        SourceColumn(
            func=lambda context: context['object'].get_document_count(
                user=context['request'].user
            ), include_label=True, label=_('Documents'), source=Tag
        )

        document_page_search.add_model_field(
            field='document_version__document__tags__label', label=_('Tags')
        )
        document_search.add_model_field(field='tags__label', label=_('Tags'))

        menu_facet.bind_links(
            links=(link_document_tag_list,), sources=(Document,)
        )

        menu_list_facet.bind_links(
            links=(
                link_acl_list, link_events_for_object,
                link_object_event_types_user_subcriptions_list,
                link_tag_document_list,
            ), sources=(Tag,)
        )

        menu_tags.bind_links(
            links=(
                link_tag_list, link_tag_create
            )
        )

        menu_main.bind_links(links=(menu_tags,), position=98)

        menu_multi_item.bind_links(
            links=(
                link_document_multiple_attach_multiple_tag,
                link_document_multiple_tag_multiple_remove
            ),
            sources=(Document,)
        )
        menu_multi_item.bind_links(
            links=(link_tag_multiple_delete,), sources=(Tag,)
        )
        menu_object.bind_links(
            links=(
                link_tag_edit, link_tag_delete
            ),
            sources=(Tag,)
        )
        menu_secondary.bind_links(
            links=(link_document_tag_multiple_attach, link_document_tag_multiple_remove),
            sources=(
                'tags:tag_attach', 'tags:document_tag_list',
                'tags:single_document_multiple_tag_remove'
            )
        )

        # Index update

        m2m_changed.connect(
            dispatch_uid='tags_handler_index_document',
            receiver=handler_index_document,
            sender=Tag.documents.through
        )

        pre_delete.connect(
            dispatch_uid='tags_handler_tag_pre_delete',
            receiver=handler_tag_pre_delete,
            sender=Tag
        )
