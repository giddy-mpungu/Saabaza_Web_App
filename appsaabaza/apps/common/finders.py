import os

from django.apps import apps
from django.contrib.staticfiles.finders import AppDirectoriesFinder


class AppsaabazaAppDirectoriesFinder(AppDirectoriesFinder):
    def __init__(self, *args, **kwargs):
        super(AppsaabazaAppDirectoriesFinder, self).__init__(*args, **kwargs)
        for app_config in apps.get_app_configs():
            if getattr(app_config, 'has_static_media', False):
                if app_config.name not in self.apps:
                    self.storages[app_config.name] = self.storage_class(
                        os.path.join(app_config.path, self.source_dir)
                    )
                    self.apps.append(app_config.name)
