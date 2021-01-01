# See https://tech.davis-hansson.com/p/make/ for a write-up of these settings

# Use bash and set strict execution mode
SHELL:=bash
.SHELLFLAGS := -eu -o pipefail -c

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

DOCKER_BUILD_SENTINAL := docker_build.sentinal

.PHONY: image

image: $(DOCKER_BUILD_SENTINAL)

$(DOCKER_BUILD_SENTINAL): Dockerfile requirements.txt
	docker build -t pdfgen-generate:latest .
	touch $(DOCKER_BUILD_SENTINAL)

requirements.txt:
	cp ../requirements.txt .

clean:
	rm $(DOCKER_BUILD_SENTINAL)