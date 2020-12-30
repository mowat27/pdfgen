# See https://tech.davis-hansson.com/p/make/ for a write-up of these settings

# Use bash and set strict execution mode
SHELL:=bash
.SHELLFLAGS := -eu -o pipefail -c

MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

target/google.pdf: target
	python -m generate "https://www.google.com/" target/google.pdf
	open target/google.pdf

target/basic.pdf: target
	python -m generate www/basic/index.html target/basic.pdf
	open target/basic.pdf

target: 
	mkdir -p target

server:
	python -m http.server --directory www

clean:
	rm -f target/*.pdf
