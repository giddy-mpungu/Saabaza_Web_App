#!/bin/bash

export APPSAABAZA_WORKER_NAME=${APPSAABAZA_WORKER_NAME:-$1}

QUEUE_LIST_DEFAULT=`su appsaabaza -c "${APPSAABAZA_PYTHON_BIN_DIR}Saabaza_Web_App.py platformtemplate worker_queues"`

APPSAABAZA_QUEUE_LIST=${APPSAABAZA_QUEUE_LIST:-${QUEUE_LIST_DEFAULT}}

# Use -A and not --app. Both are the same but behave differently
# -A can be located before the command while --app cannot.
# Pass ${@:2} to allow overriding the defaults arguments
su appsaabaza -c "${APPSAABAZA_PYTHON_BIN_DIR}celery -A appsaabaza worker -Ofair -l ERROR -Q ${APPSAABAZA_QUEUE_LIST} ${@:2}"
