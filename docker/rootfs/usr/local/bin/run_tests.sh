#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
TEST_ARGUMENT=${@:-"--appsaabaza-apps --no-exclude"}

apt-get update
apt-get install -y --no-install-recommends gcc python3-dev tesseract-ocr-deu

su appsaabaza -c "${APPSAABAZA_PIP_BIN} install -r ${APPSAABAZA_INSTALL_DIR}/testing-base.txt"

su appsaabaza -c "APPSAABAZA_TESTS_SELENIUM_SKIP=true ${APPSAABAZA_BIN} test ${TEST_ARGUMENT} --settings=appsaabaza.settings.testing"
