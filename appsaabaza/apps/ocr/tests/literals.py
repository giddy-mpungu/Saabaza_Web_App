# -*- coding: utf-8 -*-

TEST_DOCUMENT_CONTENT = 'Appsaabaza EDMS Documentation'
TEST_DOCUMENT_CONTENT_DEU_1 = 'Repository für elektronische Dokumente.'
TEST_DOCUMENT_CONTENT_DEU_2 = 'Es bietet einen'

TEST_OCR_INDEX_NODE_TEMPLATE = '{% if "appsaabaza" in document.latest_version.ocr_content|join:" "|lower %}appsaabaza{% endif %}'
TEST_OCR_INDEX_NODE_TEMPLATE_LEVEL = 'appsaabaza'
