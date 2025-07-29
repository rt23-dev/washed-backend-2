FROM python:3.10-slim

# Install system dependencies needed for mediapipe
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Start the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
