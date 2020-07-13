# Minimal makefile for Sphinx documentation

# You can set these variables from the command line, and also
# from the environment for the first two.
BUILDOPTS ?=
BUILDTOOL ?= sphinx-build
SOURCEDIR  = source
BUILDDIR   = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(BUILDTOOL) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(BUILDOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option. $(O) is meant as a shortcut for $(BUILDOPTS).
%: Makefile
	@$(BUILDTOOL) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(BUILDOPTS) $(O)
