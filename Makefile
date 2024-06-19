IMAGE := myimage
GIT_ID := $(shell git rev-parse --short HEAD)

docker-build:
	DOCKER_BUILDKIT=1 docker build -f Dockerfile --target runtime -t ${IMAGE}:${GIT_ID} .

docker-push:
	docker push ${IMAGE}:${GIT_ID}

docker-deploy:
	docker-build docker-push

docker-run:
	docker run --rm --name my-container --env-file .env ${IMAGE}:${GIT_ID}
