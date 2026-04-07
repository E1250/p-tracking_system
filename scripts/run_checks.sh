# Stop in any command fails
set -e 

# pre-commit - Already runnging ruff
pre-commit run --all-files

# ruff
# echo "Running ruff to check for bad imports, messy structure and style drift."
# ruff format .
# ruff check . --fix
# ruff check . 
# Fix the rest of ruff manually

# Pyright 
echo "Running pyright to check for wrong retuns and type contracts"
pyright

# Pytest
pytest

# Mkdocs
mkdocs build



echo "#### Checking Done ####"