# See https://tech.davis-hansson.com/p/make/ for a write-up of these settings

# Use bash and set strict execution mode
SHELL:=bash
.SHELLFLAGS := -eu -o pipefail -c

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

target/google.pdf: target
	python -m generate "https://www.google.com/" target/google.pdf
	open target/google.pdf

target/newspaper.pdf: target
	python -m generate www/newspaper/index.html target/newspaper.pdf
	open target/newspaper.pdf

target: 
	mkdir -p target

server:
	python -m http.server --directory www

clean:
	rm -f target/*.pdf
