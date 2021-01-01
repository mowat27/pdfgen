# See https://tech.davis-hansson.com/p/make/ for a write-up of these settings

# Use bash and set strict execution mode
SHELL:=bash
.SHELLFLAGS := -eu -o pipefail -c

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

DOCKER_BUILD_SENTINAL := docker_build.sentinal
DOCKER_IMAGE := mowat27/pdfgen-generate:latest
INIT_SCRIPT := lib/init.sh

PYFILES := $(shell find . -type f -name '*.py'  -maxdepth 1) 
PACKAGES := $(shell find . -type d -maxdepth 1 ! -path . ! -path ./build) 
DEPS := ../aws ../requirements.txt

SOURCES := $(PYFILES) $(PACKAGES) $(DEPS)


# Targets for making things

.PHONY: image

image: $(DOCKER_BUILD_SENTINAL) build

$(DOCKER_BUILD_SENTINAL): Dockerfile build
	docker build -t $(DOCKER_IMAGE) .
	touch $(DOCKER_BUILD_SENTINAL)

build: $(SOURCES)
	@rm -rf build 
	@mkdir build
	@cp -r $(SOURCES) build
	@ls -l build

clean:
	rm -f $(DOCKER_BUILD_SENTINAL)
	rm -rf build

# Targets for running things

.PHONY: run shell 

run: image
	docker run --rm -it $(DOCKER_IMAGE)

shell: image
	docker run --rm -it $(DOCKER_IMAGE) /bin/bash -l