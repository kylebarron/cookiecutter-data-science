SHELL := /bin/bash
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
		-V title:"Patient Transfers" \
		-V date:"$(shell date +"%B %e, %Y")" \
		-V author:"Kyle Barron" \
		--toc \
		--bibliography=../bibliography.bib \
		--standalone \
		-V geometry:"margin=1in" \
		--syntax-definition=<(curl -s https://raw.githubusercontent.com/kylebarron/highlight-sas-stata/master/xml/sas.xml) \
		--syntax-definition=<(curl -s https://raw.githubusercontent.com/kylebarron/highlight-sas-stata/master/xml/stata.xml)
	{% if cookiecutter.rclone_remote_path != "Don't use rclone" %}
	rclone sync pdf/documentation.pdf {{ cookiecutter.rclone_remote_path }}/docs/pdf/
	{% endif %}

docx/documentation.docx: $(shell find src -name '*.md') ../bibliography.bib
	pandoc \
		src/index.md \
	 	src/glossary.md \
		src/references.md \
		-o docx/documentation.docx \
		-V title:"Patient Transfers" \
		-V date:"$(shell date +"%B %e, %Y")" \
		-V author:"Kyle Barron" \
		--toc \
		--bibliography=../bibliography.bib \
		--standalone \
		--syntax-definition=<(curl -s https://raw.githubusercontent.com/kylebarron/highlight-sas-stata/master/xml/sas.xml) \
		--syntax-definition=<(curl -s https://raw.githubusercontent.com/kylebarron/highlight-sas-stata/master/xml/stata.xml)
	{% if cookiecutter.rclone_remote_path != "Don't use rclone" %}
	rclone sync docx/documentation.docx {{ cookiecutter.rclone_remote_path }}/docs/docx/
	{% endif %}

html/mkdocs/index.html: $(shell find src) ../bibliography.bib
	if command -v mkdocs 2>/dev/null; then \
        mkdocs build; \
    else \
        pip install mkdocs mkdocs-material; \
		mkdocs build; \
    fi
	{% if cookiecutter.rclone_remote_path != "Don't use rclone" %}
	rclone sync html/mkdocs/ {{ cookiecutter.rclone_remote_path }}/docs/html/mkdocs/
	{% endif %}

html/documentation.html: $(shell find src) ../bibliography.bib
	pandoc \
		src/index.md \
	 	src/glossary.md \
		src/references.md \
		-o html/documentation.html \
		-V title:"Patient Transfers" \
		-V date:"$(shell date +"%B %e, %Y")" \
		-V author:"Kyle Barron" \
		--toc \
		--bibliography=../bibliography.bib \
		--standalone \
		-H src/aux/css-start.html \
		-H src/aux/github-markdown.css \
		-H src/aux/css-end.html \
		-B src/aux/gh-markdown-start.html \
		-A src/aux/gh-markdown-end.html \
		--mathjax \
		--syntax-definition=<(curl -s https://raw.githubusercontent.com/kylebarron/highlight-sas-stata/master/xml/sas.xml) \
		--syntax-definition=<(curl -s https://raw.githubusercontent.com/kylebarron/highlight-sas-stata/master/xml/stata.xml)
	{% if cookiecutter.rclone_remote_path != "Don't use rclone" %}
	rclone sync html/documentation.html {{ cookiecutter.rclone_remote_path }}/docs/html/
	{% endif %}
