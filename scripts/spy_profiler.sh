# This one is NOT working for now

# Show aux then pull Uvicorn.
# ps aux | grep uvicorn

# py-spy top --pid 000
# conda init bash
# conda deactivat/e
# !#/bin/bash
py-spy top -- -m uvicorn backend.main:app