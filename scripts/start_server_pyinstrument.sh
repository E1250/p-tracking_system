# Start server with a profiler. 
pyinstrument -o "app/pyinstrument_profile.html" -m uvicorn backend.main:app