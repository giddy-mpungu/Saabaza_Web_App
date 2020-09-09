from django.apps import apps

from ..finders import AppsaabazaAppDirectoriesFinder

from .base import BaseTestCase


class AppsaabazaAppDirectoriesFinderTestCase(BaseTestCase):
    def test_app_detection(self):
        app_list = []

        for app_config in apps.get_app_configs():
            if getattr(app_config, 'has_static_media', False):
                if app_config.name not in app_list:
                    app_list.append(app_config.name)

        test_finder = AppsaabazaAppDirectoriesFinder()

        for finder_app in test_finder.apps:
            if finder_app.startswith('appsaabaza'):
                self.assertTrue(
                    finder_app in app_list, msg='"{}" is missing'.format(finder_app)
                )

        self.assertEqual(
            len(test_finder.apps), len(test_finder.storages)
        )
