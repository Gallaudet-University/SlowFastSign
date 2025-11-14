# Variables
IMAGE_NAME=python-docker
CONTAINER_NAME=python-docker-container
DATASET_PATH=$(shell pwd)/dataset
PROJECT_PATH=$(shell pwd)

# Check if python-docker is built
build:
	@if docker image inspect $(IMAGE_NAME) > /dev/null 2>&1; then \
		echo " Image '$(IMAGE_NAME)' already exists. Rebuild? (y/n)"; \
		read answer; \
		if [ "$$answer" = "y" ] || [ "$$answer" = "Y" ]; then \
			echo "Cleaning up and rebuilding $(IMAGE_NAME)..."; \
			docker stop $(docker ps -aq) || true; \
			docker rm -f $(docker ps -aq) || true; \
			docker system prune -af --volumes; \
			docker build -t $(IMAGE_NAME) .; \
		else \
			echo "Skipping build."; \
		fi; \
	else \
		echo "Building $(IMAGE_NAME)..."; \
		docker build -t $(IMAGE_NAME) .; \
	fi

run:
	docker run --rm -it \
		-v $(DATASET_PATH):/project/dataset \
		-v $(PROJECT_PATH):/project \
		--name $(CONTAINER_NAME) \
		$(IMAGE_NAME) bash	

clean-everything:
	docker stop $(docker ps -aq) || true
	docker rm -f $(docker ps -aq) || true
	docker system prune -af --volumes