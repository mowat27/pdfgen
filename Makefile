# See https://tech.davis-hansson.com/p/make/ for a write-up of these settings

# Use bash and set strict execution mode
SHELL:=bash
.SHELLFLAGS := -eu -o pipefail -c

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

.PHONY: newspaper server plan apply apply!

newspaper: 
	bin/generate.sh www/newspaper/index.html

server:
	python -m http.server --directory www

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

