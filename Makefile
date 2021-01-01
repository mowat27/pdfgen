# See https://tech.davis-hansson.com/p/make/ for a write-up of these settings

# Use bash and set strict execution mode
SHELL:=bash
.SHELLFLAGS := -eu -o pipefail -c

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

# -- Docker --------------------------------------------------------------------

.PHONY: up up! generator.shell

up: 
	docker-compose up

down: 
	docker-compose down

up!:
	docker-compose up -d

generator.shell: 
	docker-compose exec generator /bin/bash

# -- Local Development ---------------------------------------------------------

.PHONY: newspaper server

newspaper: 
	bin/generate.sh www/newspaper/index.html

server:
	python -m http.server --directory www

# -- Infrastructure ------------------------------------------------------------

.PHONY: plan apply apply!

plan:
	cd infra && terraform apply

apply:
	cd infra && terraform apply

apply!:
	cd infra && terraform apply --auto-approve

destroy:
	cd infra && terraform destroy

destroy!:
	cd infra && terraform destroy --auto-approve

