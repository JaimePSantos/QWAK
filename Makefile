# ...existing code...

# Define the Sphinx documentation builder command
SPHINXBUILD   = sphinx-build
SOURCEDIR     = docs/source
BUILDDIR      = docs/build
FLASKDIR      = flask_app/static/docs  # Adjust this path to match your Flask app's static directory

# Define the default target
.PHONY: help
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Define the html target
.PHONY: html
html:
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Define the clean target
.PHONY: clean
clean:
	@$(SPHINXBUILD) -M clean "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

# Define the github target
.PHONY: github
github: html
	@echo "Deploying to GitHub Pages..."
	@ghp-import -n -p -f $(BUILDDIR)/html

# Define the flask target
.PHONY: flask
flask: html
	@echo "Copying documentation to Flask static directory..."
	@cp -r $(BUILDDIR)/html/* $(FLASKDIR)

# ...existing code...