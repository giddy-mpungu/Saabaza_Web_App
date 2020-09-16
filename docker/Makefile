#!make
include config.env

HOST_IP = `/sbin/ip route|awk '/docker0/ { print $$9 }'`
APT_PROXY ?= $(HOST_IP):3142
CONSOLE_COLUMNS ?= `echo $$(tput cols)`
CONSOLE_LINES ?= `echo $$(tput lines)`
IMAGE_VERSION ?= `cat docker/rootfs/version`
PIP_INDEX_URL ?= http://$(HOST_IP):3141/root/pypi/+simple/
PIP_TRUSTED_HOST ?= $(HOST_IP)
DOCKER_HOST_REGISTRY_NAME ?= $(DOCKER_HOST_REGISTRY_NAME)
DOCKER_HOST_REGISTRY_PORT ?= $(DOCKER_HOST_REGISTRY_PORT)
DOCKER_IMAGE_APPSAABAZA_NAME ?= $(DOCKER_IMAGE_APPSAABAZA_NAME)

docker-build: ## Build a new image locally.
	docker build -t $(DOCKER_IMAGE_APPSAABAZA_NAME):$(IMAGE_VERSION) -f docker/Dockerfile .

docker-build-with-proxy: ## Build a new image locally using an APT proxy as APT_PROXY.
docker-build-with-proxy: devpi-start
	docker build -t $(DOCKER_IMAGE_APPSAABAZA_NAME):$(IMAGE_VERSION) -f docker/Dockerfile --build-arg APT_PROXY=$(APT_PROXY) --build-arg PIP_INDEX_URL=$(PIP_INDEX_URL) --build-arg PIP_TRUSTED_HOST=$(PIP_TRUSTED_HOST) --build-arg HTTP_PROXY=$(HTTP_PROXY) --build-arg HTTPS_PROXY=$(HTTPS_PROXY) .
	$(MAKE) devpi-stop

docker-build-with-proxy-push: ## Build an image with an APT proxy and push to the test registry.
docker-build-with-proxy-push: docker-build-with-proxy docker-registry-push

docker-registry-push: ## Push a built image to the test Docker registry.
	docker tag $(DOCKER_IMAGE_APPSAABAZA_NAME):$(IMAGE_VERSION) $(DOCKER_HOST_REGISTRY_NAME):$(DOCKER_HOST_REGISTRY_PORT)/$(DOCKER_IMAGE_APPSAABAZA_NAME):$(IMAGE_VERSION)
	docker push $(DOCKER_HOST_REGISTRY_NAME):$(DOCKER_HOST_REGISTRY_PORT)/$(DOCKER_IMAGE_APPSAABAZA_NAME):$(IMAGE_VERSION)
	# /etc/docker/daemon.json {"insecure-registries" : ["docker-registry.local:5000"]}
	# /etc/hosts <ip address>  docker-registry.local

docker-registry-pull: ## Pull an image from the test Docker registry.
	docker pull $(DOCKER_HOST_REGISTRY_NAME):$(DOCKER_HOST_REGISTRY_PORT)/$(DOCKER_IMAGE_APPSAABAZA_NAME):$(IMAGE_VERSION)
	docker tag $(DOCKER_HOST_REGISTRY_NAME):$(DOCKER_HOST_REGISTRY_PORT)/$(DOCKER_IMAGE_APPSAABAZA_NAME):$(IMAGE_VERSION) $(DOCKER_IMAGE_APPSAABAZA_NAME):$(IMAGE_VERSION)

docker-registry-catalog: ## Show the test Docker registry catalog.
	curl http://$(DOCKER_HOST_REGISTRY_NAME):$(DOCKER_HOST_REGISTRY_PORT)/v2/_catalog

docker-registry-tags: ## Show the tags for the image in the test Docker registry.
	curl http://$(DOCKER_HOST_REGISTRY_NAME):$(DOCKER_HOST_REGISTRY_PORT)/v2/$(DOCKER_IMAGE_APPSAABAZA_NAME)/tags/list

docker-registry-run: # Launch a test Docker registry.
	docker run -d -p 5000:5000 --name registry registry:2

docker-shell: ## Launch a bash instance inside a running container. Pass the container name via DOCKER_CONTAINER.
	docker exec -e TERM=$(TERM) -e "COLUMNS=$(CONSOLE_COLUMNS)" -e "LINES=$(CONSOLE_LINES)" -it $(DOCKER_CONTAINER) /bin/bash

docker-runtest-container: ## Run a test container.
docker-runtest-container: docker-test-cleanup
	docker run \
	-d \
	--name test-Saabaza_Web_App \
	-p 80:8000 \
	-v test-appsaabaza_data:/var/lib/appsaabaza \
	$(DOCKER_IMAGE_APPSAABAZA_NAME):$(IMAGE_VERSION)

docker-runtest-cleanup: ## Delete the test container and the test volume.
	@docker rm -f test-Saabaza_Web_App || true
	@docker volume rm test-appsaabaza_data || true

docker-runtest-all: ## Executed the test suite in a test container.
	docker run --rm $(DOCKER_IMAGE_APPSAABAZA_NAME):$(IMAGE_VERSION) run_tests

docker-compose-build:
	docker-compose -f docker/docker-compose.yml -p Saabaza_Web_App build

docker-compose-build-with-proxy: devpi-start
	docker-compose -f docker/docker-compose.yml -p Saabaza_Web_App build --build-arg APT_PROXY=$(APT_PROXY) --build-arg PIP_INDEX_URL=$(PIP_INDEX_URL) --build-arg PIP_TRUSTED_HOST=$(PIP_TRUSTED_HOST) --build-arg HTTP_PROXY=$(HTTP_PROXY) --build-arg HTTPS_PROXY=$(HTTPS_PROXY)
	$(MAKE) devpi-stop

docker-compose-up:
	docker-compose -f docker/docker-compose.yml -p Saabaza_Web_App up

docker-staging-network-create:
	@docker network rm appsaabaza-staging || true
	docker network create appsaabaza-staging

docker-staging-container-postgresql-start:
	docker run \
	-d \
	--name appsaabaza-staging-postgres \
	--network=appsaabaza-staging \
	-e POSTGRES_USER=($DEFAULT_DATABASE_USER) \
	-e POSTGRES_DB=$(DEFAULT_DATABASE_NAME) \
	-e POSTGRES_PASSWORD=$(DEFAULT_DATABASE_PASSWORD) \
	-v appsaabaza-staging-postgres:/var/lib/postgresql/data \
	$(DOCKER_POSTGRES_IMAGE_VERSION)

docker-staging-container-redis-start:
	docker run \
	-d \
	--name appsaabaza-staging-redis \
	--network=appsaabaza-staging \
	-v appsaabaza-staging-redis:/data \
	$(DOCKER_REDIS_IMAGE_VERSION) \
	redis-server \
	--databases \
	"2" \
	--maxmemory-policy \
	allkeys-lru \
	--save \
	"" \
	--requirepass appsaabazaredispassword

docker-staging-container-rabbitmq-start:
	docker run \
	-d \
	--name appsaabaza-staging-rabbitmq \
	--network=appsaabaza-staging \
	-v appsaabaza-staging-rabbitmq:/var/lib/rabbitmq \
	$(DOCKER_RABBITMQ_IMAGE_VERSION) \

docker-staging-container-appsaabaza-start:
	sleep 5 && docker run \
	-d \
	--name appsaabaza-staging-app \
	--network=appsaabaza-staging \
	-p 80:8000 \
	-e APPSAABAZA_DATABASE_ENGINE=django.db.backends.postgresql \
	-e APPSAABAZA_DATABASE_HOST=appsaabaza-staging-postgres \
	-e APPSAABAZA_DATABASE_NAME=$(DEFAULT_DATABASE_NAME) \
	-e APPSAABAZA_DATABASE_PASSWORD=($DEFAULT_DATABASE_PASSWORD) \
	-e APPSAABAZA_DATABASE_USER=appsaabaza \
	-e APPSAABAZA_CELERY_BROKER_URL=$(APPSAABAZA_CELERY_BROKER_URL) \
	-e APPSAABAZA_CELERY_RESULT_BACKEND="redis://:appsaabazaredispassword@appsaabaza-staging-redis:6379/1" \
	-v appsaabaza-staging-app:/var/lib/appsaabaza \
	$(DOCKER_IMAGE_APPSAABAZA_NAME):$(IMAGE_VERSION)

docker-staging-start-with-rabbitmq: APPSAABAZA_CELERY_BROKER_URL="amqp://guest:guest@appsaabaza-staging-rabbitmq:5672/"
docker-staging-start-with-rabbitmq: docker-staging-start

docker-staging-start-with-redis: APPSAABAZA_CELERY_BROKER_URL="redis://:appsaabazaredispassword@appsaabaza-staging-redis:6379/0"
docker-staging-start-with-redis: docker-staging-start

docker-staging-start: docker-staging-cleanup docker-staging-network-create docker-staging-container-postgresql-start docker-staging-container-rabbitmq-start docker-staging-container-redis-start docker-staging-container-appsaabaza-start
	docker logs -f appsaabaza-staging-app

docker-staging-cleanup: ## Delete the test container and the test volume.
	@docker rm -f appsaabaza-staging-app || true
	@docker rm -f appsaabaza-staging-redis || true
	@docker rm -f appsaabaza-staging-rabbitmq || true
	@docker rm -f appsaabaza-staging-postgres || true
	@docker volume rm appsaabaza-staging-app || true
	@docker volume rm appsaabaza-staging-postgres || true
	@docker volume rm appsaabaza-staging-rabbitmq || true
	@docker volume rm appsaabaza-staging-redis || true
	@docker network rm appsaabaza-staging || true

devpi-init:
	@if [ -z "$$(pip list | grep devpi-server)" ]; then echo "devpi-server not installed"; exit 1;fi
	devpi-server --init || true

devpi-start: devpi-init
	devpi-server --start --host=0.0.0.0 || true

devpi-stop:
	devpi-server --stop || true
