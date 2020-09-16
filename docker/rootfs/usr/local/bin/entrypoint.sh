#!/bin/bash

# Use bash and not sh to support argument slicing "${@:2}"
# sh defaults to dash instead of bash.

set -e
echo "appsaabaza: starting entrypoint.sh"
INSTALL_FLAG=/var/lib/appsaabaza/system/SECRET_KEY
CONCURRENCY_ARGUMENT=--concurrency=

DEFAULT_USER_UID=1000
DEFAULT_USER_GID=1000

APPSAABAZA_USER_UID=${APPSAABAZA_USER_UID:-${DEFAULT_USER_UID}}
APPSAABAZA_USER_GID=${APPSAABAZA_USER_GID:-${DEFAULT_USER_GID}}

export APPSAABAZA_ALLOWED_HOSTS='["*"]'
export APPSAABAZA_BIN=/opt/Saabaza_Web_App/bin/Saabaza_Web_App.py
export APPSAABAZA_INSTALL_DIR=/opt/Saabaza_Web_App
export APPSAABAZA_PYTHON_BIN_DIR=/opt/Saabaza_Web_App/bin/
export APPSAABAZA_MEDIA_ROOT=/var/lib/appsaabaza
export APPSAABAZA_SETTINGS_MODULE=${APPSAABAZA_SETTINGS_MODULE:-appsaabaza.settings.production}

# Set DJANGO_SETTINGS_MODULE to APPSAABAZA_SETTINGS_MODULE to avoid two
# different environments for the setting file.
export DJANGO_SETTINGS_MODULE=${APPSAABAZA_SETTINGS_MODULE}

export APPSAABAZA_GUNICORN_BIN=${APPSAABAZA_PYTHON_BIN_DIR}gunicorn
export APPSAABAZA_GUNICORN_WORKERS=${APPSAABAZA_GUNICORN_WORKERS:-2}
export APPSAABAZA_GUNICORN_TIMEOUT=${APPSAABAZA_GUNICORN_TIMEOUT:-120}
export APPSAABAZA_PIP_BIN=${APPSAABAZA_PYTHON_BIN_DIR}pip
export APPSAABAZA_STATIC_ROOT=${APPSAABAZA_INSTALL_DIR}/static

APPSAABAZA_WORKER_FAST_CONCURRENCY=${APPSAABAZA_WORKER_FAST_CONCURRENCY:-0}
APPSAABAZA_WORKER_MEDIUM_CONCURRENCY=${APPSAABAZA_WORKER_MEDIUM_CONCURRENCY:-0}
APPSAABAZA_WORKER_SLOW_CONCURRENCY=${APPSAABAZA_WORKER_SLOW_CONCURRENCY:-1}

if [ "$APPSAABAZA_WORKER_FAST_CONCURRENCY" -eq 0 ]; then
    APPSAABAZA_WORKER_FAST_CONCURRENCY=
else
    APPSAABAZA_WORKER_FAST_CONCURRENCY="${CONCURRENCY_ARGUMENT}${APPSAABAZA_WORKER_FAST_CONCURRENCY}"
fi
export APPSAABAZA_WORKER_FAST_CONCURRENCY

if [ "$APPSAABAZA_WORKER_MEDIUM_CONCURRENCY" -eq 0 ]; then
    APPSAABAZA_WORKER_MEDIUM_CONCURRENCY=
else
    APPSAABAZA_WORKER_MEDIUM_CONCURRENCY="${CONCURRENCY_ARGUMENT}${APPSAABAZA_WORKER_MEDIUM_CONCURRENCY}"
fi
export APPSAABAZA_WORKER_MEDIUM_CONCURRENCY

if [ "$APPSAABAZA_WORKER_SLOW_CONCURRENCY" -eq 0 ]; then
    APPSAABAZA_WORKER_SLOW_CONCURRENCY=
else
    APPSAABAZA_WORKER_SLOW_CONCURRENCY="${CONCURRENCY_ARGUMENT}${APPSAABAZA_WORKER_SLOW_CONCURRENCY}"
fi
export APPSAABAZA_WORKER_SLOW_CONCURRENCY

if mount | grep '/dev/shm' > /dev/null; then
    APPSAABAZA_GUNICORN_TEMPORARY_DIRECTORY="--worker-tmp-dir /dev/shm"
else
    APPSAABAZA_GUNICORN_TEMPORARY_DIRECTORY=
fi

# Allow importing of user setting modules
export PYTHONPATH=$PYTHONPATH:$APPSAABAZA_MEDIA_ROOT

apt_get_install() {
    apt-get -q update
    apt-get install -y --force-yes --no-install-recommends --auto-remove "$@"
    apt-get -q clean
    rm -rf /var/lib/apt/lists/*
}

initialsetup() {
    echo "appsaabaza: initialsetup()"

    # Change the owner of the /var/lib/appsaabaza always to allow adding the
    # initial files. Top level only.
    chown appsaabaza:appsaabaza ${APPSAABAZA_MEDIA_ROOT}

    su appsaabaza -c "${APPSAABAZA_BIN} initialsetup --force --no-dependencies"
}

make_ready() {
    # Check if this is a new install, otherwise try to upgrade the existing
    # installation on subsequent starts
    if [ ! -f $INSTALL_FLAG ]; then
        initialsetup
    else
        performupgrade
    fi
}

run_all() {
    echo "appsaabaza: start()"
    rm -rf /var/run/supervisor.sock
    exec /usr/bin/supervisord -nc /etc/supervisor/supervisord.conf
}

os_package_installs() {
    echo "appsaabaza: os_package_installs()"
    if [ "${APPSAABAZA_APT_INSTALLS}" ]; then
        DEBIAN_FRONTEND=noninteractive apt_get_install $APPSAABAZA_APT_INSTALLS
    fi
}

performupgrade() {
    echo "appsaabaza: performupgrade()"
    su appsaabaza -c "${APPSAABAZA_BIN} performupgrade --no-dependencies"
}

pip_installs() {
    echo "appsaabaza: pip_installs()"
    if [ "${APPSAABAZA_PIP_INSTALLS}" ]; then
        su appsaabaza -c "${APPSAABAZA_PIP_BIN} install $APPSAABAZA_PIP_INSTALLS"
    fi
}

update_uid_gid() {
    echo "appsaabaza: update_uid_gid()"
    groupmod appsaabaza -o -g ${APPSAABAZA_USER_GID}
    usermod appsaabaza -o -u ${APPSAABAZA_USER_UID}

    if [ ${APPSAABAZA_USER_UID} -ne ${DEFAULT_USER_UID} ] || [ ${APPSAABAZA_USER_GID} -ne ${DEFAULT_USER_GID} ]; then
        echo "appsaabaza: Updating file ownership. This might take a while if there are many documents."
        chown -R appsaabaza:appsaabaza ${APPSAABAZA_INSTALL_DIR} ${APPSAABAZA_STATIC_ROOT}
        if [ "${APPSAABAZA_SKIP_CHOWN_ON_STARTUP}" = "true" ]; then
            echo "appsaabaza: skipping chown on startup"
        else
            chown -R appsaabaza:appsaabaza ${APPSAABAZA_MEDIA_ROOT}
        fi
    fi
}

# Start execution here
wait.sh ${APPSAABAZA_DOCKER_WAIT}
update_uid_gid
os_package_installs || true
pip_installs || true


case "$1" in

run_initialsetup)
    initialsetup
    ;;

run_performupgrade)
    performupgrade
    ;;

run_all)
    make_ready
    run_all
    ;;

run_celery)
    run_celery.sh "${@:2}"
    ;;

run_command)
    su appsaabaza -c "${APPSAABAZA_BIN} ${@:2}"
    ;;

run_frontend)
    run_frontend.sh
    ;;

run_tests)
    make_ready
    run_tests.sh "${@:2}"
    ;;

run_worker)
    run_worker.sh "${@:2}"
    ;;

*)
    su appsaabaza -c "$@"
    ;;

esac
