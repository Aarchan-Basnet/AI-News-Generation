# Use the official Python 3.9 slim base image
FROM python:3.9-slim

## Install system dependencies (example: build-essential)
#RUN apt-get update && apt-get install -y build-essential
RUN pip install --no-cache-dir numpy pandas pillow
RUN pip install --no-cache-dir fastapi uvicorn
RUN #pip install --no-cache-dir torch
RUN pip install --no-cache-dir torchvision
RUN pip install --no-cache-dir transformers[torch]


# Copy the openai-clip package and install it
COPY openai-clip.tar.gz /
RUN pip install openai-clip.tar.gz

## Copy the requirements file
COPY requirements.txt /requirements.txt

## Install Python dependencies
#RUN pip install --no-cache-dir -r /requirements.txt

# Copy the rest of the application code
COPY . /

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["python3", "main.py"]
