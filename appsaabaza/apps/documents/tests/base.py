from appsaabaza.apps.common.tests.base import BaseTestCase, GenericViewTestCase

from .mixins import DocumentTestMixin


class GenericDocumentTestCase(DocumentTestMixin, BaseTestCase):
    """Base test case when testing models or classes"""


class GenericDocumentViewTestCase(DocumentTestMixin, GenericViewTestCase):
    """Base test case when testing views"""
