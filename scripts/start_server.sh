conda init
conda activate tracking_system

uvicorn backend.main:app --reload