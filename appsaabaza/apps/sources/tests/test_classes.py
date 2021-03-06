import os
import shutil

from appsaabaza.apps.common.tests.base import BaseTestCase
from appsaabaza.apps.documents.tests.literals import TEST_NON_ASCII_DOCUMENT_PATH
from appsaabaza.apps.storage.utils import mkdtemp

from ..classes import StagingFile

from .mocks import MockStagingFolder


class StagingFileTestCase(BaseTestCase):
    def test_unicode_staging_file(self):
        temporary_directory = mkdtemp()
        shutil.copy(TEST_NON_ASCII_DOCUMENT_PATH, temporary_directory)

        filename = os.path.basename(TEST_NON_ASCII_DOCUMENT_PATH)

        staging_file_1 = StagingFile(
            staging_folder=MockStagingFolder(),
            filename=filename
        )

        staging_file_2 = StagingFile(
            staging_folder=MockStagingFolder(),
            encoded_filename=staging_file_1.encoded_filename
        )

        self.assertEqual(filename, staging_file_2.filename)

        shutil.rmtree(temporary_directory)
