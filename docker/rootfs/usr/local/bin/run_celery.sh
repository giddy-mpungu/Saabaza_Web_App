#!/bin/bash

# Use -A and not --app. Both are the same but behave differently
# -A can be located before the command while --app cannot.
su appsaabaza -c "${APPSAABAZA_PYTHON_BIN_DIR}celery -A appsaabaza $@"
