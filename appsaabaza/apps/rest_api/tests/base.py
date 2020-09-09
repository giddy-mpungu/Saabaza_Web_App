from rest_framework.test import APITestCase

from appsaabaza.apps.common.tests.base import GenericViewTestCase
from appsaabaza.apps.permissions.classes import Permission
from appsaabaza.apps.smart_settings.classes import Namespace


class BaseAPITestCase(APITestCase, GenericViewTestCase):
    """
    API test case class that invalidates permissions and smart settings
    """
    expected_content_types = None

    def setUp(self):
        super(BaseAPITestCase, self).setUp()
        Namespace.invalidate_cache_all()
        Permission.invalidate_cache()
