################################################################################
# GLOBALS                                                                      #
################################################################################

SHELL := /bin/bash
PROJECT_DIR := "$(shell pwd -P)"
PROJECT_NAME := {{ cookiecutter.repo_name }}
DATA_DIR := $(PROJECT_DIR)/data

EVAL_GLOBALS := PROJECT_DIR=$(PROJECT_DIR) DATA_DIR=$(DATA_DIR)
RUN_STATA := $(EVAL_GLOBALS) bash $(PROJECT_DIR)/lib/statab.sh do
RUN_PYTHON := $(EVAL_GLOBALS) python

PANDOC_INCLUDE := perl -ne 's/^\[(.+)\].*/`cat $1`/e;print'

PANDOC_OPTS := -V author:"{{ cookiecutter.author_name }}"
PANDOC_OPTS += -V date:"$(shell date +"%B %e, %Y")"
PANDOC_OPTS += --toc
PANDOC_OPTS += --filter=$(PROJECT_DIR)/lib/pandoc-config/filters/pandoc-svg.py
PANDOC_OPTS += -V lof:"true"
PANDOC_OPTS += -V toc-depth:"2"
PANDOC_OPTS += -V citecolor:"blue"
PANDOC_OPTS += --bibliography=$(PROJECT_DIR)/bibliography.bib
PANDOC_OPTS += --standalone
PANDOC_OPTS += --syntax-definition=<(curl -s https://raw.githubusercontent.com/kylebarron/highlight-sas-stata/master/xml/stata.xml)
PANDOC_OPTS += --syntax-definition=<(curl -s https://raw.githubusercontent.com/kylebarron/highlight-sas-stata/master/xml/sas.xml)

PANDOC_HTML_OPTS := $(PANDOC_OPTS) --self-contained
PANDOC_HTML_OPTS += -H $(PROJECT_DIR)/lib/pandoc-config/aux/html/gh-markdown-header.html
PANDOC_HTML_OPTS += -B $(PROJECT_DIR)/lib/pandoc-config/aux/html/gh-markdown-start.html
PANDOC_HTML_OPTS += -A $(PROJECT_DIR)/lib/pandoc-config/aux/html/gh-markdown-end.html
PANDOC_HTML_OPTS += --mathjax

PANDOC_PDF_OPTS := $(PANDOC_OPTS) -V geometry:"margin=1.5in"

################################################################################
# COMMANDS                                                                     #
################################################################################

.PHONY: clean dependencies

## Install Development Environment
dependencies: local/miniconda/bin/python local/bin/rclone
	./local/miniconda/bin/conda env create -f environment.yml

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

local/miniconda/bin/python:
	@echo "Installing miniconda into the project directory"
	wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda3.sh
	mkdir -p local
	bash /tmp/miniconda3.sh -b -p local/miniconda

local/bin/rclone:
    wget https://downloads.rclone.org/rclone-current-linux-amd64.zip -O /tmp/rclone.zip
	mkdir -p local/bin/ local/share/
	unzip -j /tmp/rclone.zip "rclone-v*-linux-amd64/rclone" -d local/bin/
	unzip -j /tmp/rclone.zip "rclone-v*-linux-amd64/rclone.1" -d local/share/

################################################################################
# PROJECT RULES                                                                #
################################################################################

.PHONY: all code report lit_review docs emails sync
## Run everything
all: code report docs sync

## Run code
code:
	@echo "Running code"

## Download emails relevant to the project from Gmail
emails:
	cd admin/emails && python download_emails.py

## Generate report
report: writeup/pdf/report.pdf writeup/docx/report.docx writeup/html/report.html
	@echo "Generating report"

## Generate literature review
lit_review: writeup/pdf/lit_review.pdf writeup/docx/lit_review.docx writeup/html/lit_review.html

## Generate documentation
docs:
	cd docs && $(MAKE) all

## Sync project folder with Dropbox
sync: local/bin/rclone
	./local/bin/rclone sync . {{ cookiecutter.rclone_remote_path }} \
		--exclude ".git/**" \
		--exclude "data/**" \
		--exclude "admin/emails/**" \
		--exclude "local/**"

################################################################################
# Detailed Rules                                                               #
################################################################################

writeup/pdf/report.pdf: writeup/src/report.md bibliography.bib
	pandoc writeup/src/report.md -o writeup/pdf/report.pdf \
	-V title:"{{ cookiecutter.project_name }}" \
	$(PANDOC_PDF_OPTS)

writeup/docx/report.docx: writeup/src/report.md bibliography.bib
	pandoc writeup/src/report.md -o writeup/docx/report.docx \
	-V title:"{{ cookiecutter.project_name }}" \
	$(PANDOC_OPTS)

writeup/html/report.html: writeup/src/report.md bibliography.bib
	pandoc writeup/src/report.md -o writeup/html/report.html \
	-V title:"{{ cookiecutter.project_name }}" \
	$(PANDOC_HTML_OPTS)


writeup/pdf/lit_review.pdf: writeup/src/lit_review.md bibliography.bib
	pandoc writeup/src/lit_review.md -o writeup/pdf/lit_review.pdf \
	-V title:"{{ cookiecutter.project_name }} Literature Review" \
	$(PANDOC_PDF_OPTS)

writeup/docx/lit_review.docx: writeup/src/lit_review.md bibliography.bib
	pandoc writeup/src/lit_review.md -o writeup/docx/lit_review.docx \
	-V title:"{{ cookiecutter.project_name }} Literature Review" \
	$(PANDOC_OPTS)

writeup/html/lit_review.html: writeup/src/lit_review.md bibliography.bib
	pandoc writeup/src/lit_review.md -o writeup/html/lit_review.html \
	-V title:"{{ cookiecutter.project_name }} Literature Review" \
	$(PANDOC_HTML_OPTS)




################################################################################
# Self Documenting Commands                                                    #
################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
	
## See this help information
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
