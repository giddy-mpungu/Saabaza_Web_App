from django.utils.encoding import force_text

from appsaabaza.apps.common.tests.base import BaseTestCase
from appsaabaza.apps.documents.permissions import permission_document_view
from appsaabaza.apps.documents.search import document_search
from appsaabaza.apps.documents.tests.mixins import DocumentTestMixin

from ..backends.django import DjangoSearchBackend


class DjangoSearchBackendDocumentSearchTestCase(
    DocumentTestMixin, BaseTestCase
):
    auto_upload_test_document = False

    def setUp(self):
        super(DjangoSearchBackendDocumentSearchTestCase, self).setUp()
        self.search_backend = DjangoSearchBackend()

    def test_simple_search_after_related_name_change(self):
        """
        Test that simple search works after related_name changes to
        document versions and document version pages
        """
        self._upload_test_document(label='first_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'q': 'first'}, user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

    def test_advanced_search_after_related_name_change(self):
        # Test versions__filename
        self._upload_test_document()
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'label': self.test_document.label},
            user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

        # Test versions__mimetype
        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={
                'versions__mimetype': self.test_document.file_mimetype
            }, user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)
        self.assertTrue(self.test_document in queryset)

    def test_meta_only(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'q': 'OR first'}, user=self._test_case_user
        )

        self.assertEqual(queryset.count(), 1)

    def test_simple_or_search(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )
        self._upload_test_document(label='second_doc')
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )
        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'q': 'first OR second'}, user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(self.test_documents[0] in queryset)
        self.assertTrue(self.test_documents[1] in queryset)

    def test_advanced_or_search(self):
        self._upload_test_document(label='first_doc')
        self.grant_access(
            obj=self.test_documents[0], permission=permission_document_view
        )

        self._upload_test_document(label='second_doc')
        self.grant_access(
            obj=self.test_documents[1], permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'label': 'first OR second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 2)
        self.assertTrue(self.test_documents[0] in queryset)
        self.assertTrue(self.test_documents[1] in queryset)

    def test_simple_and_search(self):
        self._upload_test_document(label='second_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'q': 'non_valid second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'q': 'second non_valid'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_simple_negated_search(self):
        self._upload_test_document(label='second_doc')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'q': '-non_valid second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'label': '-second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'label': '-second -Appsaabaza'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'label': '-second OR -Appsaabaza'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'label': '-non_valid -second'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_search_with_dashed_content(self):
        self._upload_test_document(label='second-document')

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'label': '-second-document'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'label': '-"second-document"'},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 0)

    def test_search_field_transformation_functions(self):
        self._upload_test_document()

        self.grant_access(
            obj=self.test_document, permission=permission_document_view
        )

        queryset = self.search_backend.search(
            search_model=document_search,
            query_string={'uuid': force_text(self.test_document.uuid)},
            user=self._test_case_user
        )
        self.assertEqual(queryset.count(), 1)
