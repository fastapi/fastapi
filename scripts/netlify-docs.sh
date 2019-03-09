#!/usr/bin/env bash
# Install pipenv to be able to install from Pipfile
pip install pipenv
# Install Pipfile including --dev, to install mkdocs and plugins
pipenv install --dev
# Finally, run mkdocs
mkdocs build
