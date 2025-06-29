.PHONY: docker
docker:
	docker build -f docker/Dockerfile -t vpodcasts:latest .