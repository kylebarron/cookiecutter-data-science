SHELL := /bin/bash
PROJECT_DIR := "$(shell cd ../ && pwd -P)"
.PHONY: all docx pdf mkdocs-html pandoc-html

all:
	$(MAKE) pdf
	$(MAKE) docx
	$(MAKE) mkdocs-html
	$(MAKE) pandoc-html

pdf:
	$(MAKE) pdf/documentation.pdf

docx:
	$(MAKE) docx/documentation.docx

mkdocs-html:
	$(MAKE) html/mkdocs/index.html

pandoc-html:
	$(MAKE) html/documentation.html

pdf/documentation.pdf: $(shell find src -name '*.md') ../bibliography.bib
	pandoc \
		src/index.md \
	 	src/glossary.md \
		src/references.md \
		-o pdf/documentation.pdf \
		-V title:"{{ cookiecutter.project_name }}" \
		-V date:"$(shell date +"%B %e, %Y")" \
		-V author:"{{ cookiecutter.author_name }}" \
		--toc \
		--bibliography=../bibliography.bib \
		--standalone \
		-V geometry:"margin=1in" \
		--syntax-definition=<(curl -s https://raw.githubusercontent.com/kylebarron/highlight-sas-stata/master/xml/sas.xml) \
		--syntax-definition=<(curl -s https://raw.githubusercontent.com/kylebarron/highlight-sas-stata/master/xml/stata.xml)
	{% if cookiecutter.use_rclone_to_sync_with_dropbox == "yes" %}
	rclone sync pdf/documentation.pdf {{ cookiecutter.rclone_remote_path }}/docs/pdf/
	{% endif %}

docx/documentation.docx: $(shell find src -name '*.md') ../bibliography.bib
	pandoc \
		src/index.md \
	 	src/glossary.md \
		src/references.md \
		-o docx/documentation.docx \
		-V title:"{{ cookiecutter.project_name }}" \
		-V date:"$(shell date +"%B %e, %Y")" \
		-V author:"{{ cookiecutter.author_name }}" \
		--toc \
		--bibliography=../bibliography.bib \
		--standalone \
		--syntax-definition=<(curl -s https://raw.githubusercontent.com/kylebarron/highlight-sas-stata/master/xml/sas.xml) \
		--syntax-definition=<(curl -s https://raw.githubusercontent.com/kylebarron/highlight-sas-stata/master/xml/stata.xml)
	{% if cookiecutter.use_rclone_to_sync_with_dropbox == "yes" %}
	rclone sync docx/documentation.docx {{ cookiecutter.rclone_remote_path }}/docs/docx/
	{% endif %}

html/mkdocs/index.html: $(shell find src) ../bibliography.bib
	if command -v mkdocs 2>/dev/null; then \
        mkdocs build; \
    else \
        pip install mkdocs mkdocs-material; \
		mkdocs build; \
    fi
	{% if cookiecutter.use_rclone_to_sync_with_dropbox == "yes" %}
	rclone sync html/mkdocs/ {{ cookiecutter.rclone_remote_path }}/docs/html/mkdocs/
	{% endif %}

html/documentation.html: $(shell find src) ../bibliography.bib
	pandoc \
		src/index.md \
	 	src/glossary.md \
		src/references.md \
		-o html/documentation.html \
		-V title:"{{ cookiecutter.project_name }}" \
		-V date:"$(shell date +"%B %e, %Y")" \
		-V author:"{{ cookiecutter.author_name }}" \
		--toc \
		--bibliography=../bibliography.bib \
		--standalone \
		-H $(PROJECT_DIR)/lib/pandoc-config/aux/html/gh-markdown-header.html \
		-B $(PROJECT_DIR)/lib/pandoc-config/aux/html/gh-markdown-start.html \
		-A $(PROJECT_DIR)/lib/pandoc-config/aux/html/gh-markdown-end.html \
		--mathjax \
		--syntax-definition=<(curl -s https://raw.githubusercontent.com/kylebarron/highlight-sas-stata/master/xml/sas.xml) \
		--syntax-definition=<(curl -s https://raw.githubusercontent.com/kylebarron/highlight-sas-stata/master/xml/stata.xml)
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
