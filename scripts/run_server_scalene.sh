# --ai to make it match ai tools
# --html create webpage to show status
# --cli show output in terminal
# --profile-all profile everything. 

scalene --memory --html --profile-all --outfile "app/scalene_profile.html" -m uvicorn backend.main:app

del "app/scalene_*.json"