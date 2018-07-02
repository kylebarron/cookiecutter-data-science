SHELL := /bin/bash
PROJECT_DIR := $(shell cd ../ && pwd -P)

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

# Documentation source files in order
DOCS_SRC_FILES := src/index.md
DOCS_SRC_FILES += src/glossary.md
DOCS_SRC_FILES += src/references.md

.PHONY: all docx pdf mkdocs-html pandoc-html

## Compile everything
all: pdf docx mkdocs-html pandoc-html

## Generate PDF documentation
pdf: pdf/documentation.pdf

## Generate Word documentation
docx: docx/documentation.docx

## Generate HTML documentation using Mkdocs
mkdocs-html: html/mkdocs/index.html

## Generate HTML documentation using Pandoc
pandoc-html: html/documentation.html

{% if cookiecutter.use_rclone_to_sync_with_dropbox == "yes" %}
## Sync documentation with Dropbox
sync:
	rclone sync . {{ cookiecutter.rclone_remote_path }}/docs
{% endif %}

pdf/documentation.pdf: $(DOCS_SRC_FILES) $(PROJECT_DIR)/bibliography.bib
	pandoc \
	 	$(DOCS_SRC_FILES) \
		-o pdf/documentation.pdf \
		-V title:"{{ cookiecutter.project_name }}" \
		$(PANDOC_PDF_OPTS)
	{% if cookiecutter.use_rclone_to_sync_with_dropbox == "yes" %}
	rclone sync pdf/documentation.pdf {{ cookiecutter.rclone_remote_path }}/docs/pdf/
	{% endif %}

docx/documentation.docx: $(DOCS_SRC_FILES) $(PROJECT_DIR)/bibliography.bib
	pandoc \
	 	$(DOCS_SRC_FILES) \
		-o docx/documentation.docx \
		-V title:"{{ cookiecutter.project_name }}" \
		$(PANDOC_OPTS)
	{% if cookiecutter.use_rclone_to_sync_with_dropbox == "yes" %}
	rclone sync docx/documentation.docx {{ cookiecutter.rclone_remote_path }}/docs/docx/
	{% endif %}

html/mkdocs/index.html: $(shell find src) $(PROJECT_DIR)/bibliography.bib
	mkdocs build
	{% if cookiecutter.use_rclone_to_sync_with_dropbox == "yes" %}
	rclone sync html/mkdocs/ {{ cookiecutter.rclone_remote_path }}/docs/html/mkdocs/
	{% endif %}

html/documentation.html: $(DOCS_SRC_FILES) $(PROJECT_DIR)/bibliography.bib
	pandoc \
	 	$(DOCS_SRC_FILES) \
		-o html/documentation.html \
		-V title:"{{ cookiecutter.project_name }}" \
		$(PANDOC_HTML_OPTS)
	{% if cookiecutter.use_rclone_to_sync_with_dropbox == "yes" %}
	rclone sync html/documentation.html {{ cookiecutter.rclone_remote_path }}/docs/html/
	{% endif %}

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

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
