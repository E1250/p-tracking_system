FROM python:3.10-slim

# Working dir inside the container.
WORKDIR /app

# Copies req.txt from local machine into /app inside container.
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the rest of files into /app folder.
COPY . .

# As HF want for backend.
EXPOSE 7860

# Starting the server.  0.0.0.0 accepts connections from anywhere, not just local. 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]