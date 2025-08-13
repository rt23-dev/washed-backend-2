# Use full Debian-based Python image (comes with build tools + common libs preinstalled)
FROM python:3.10-bullseye

# Make sure CA certificates and build tools are present
RUN apt-get update -o Acquire::ForceIPv4=true && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
 && rm -rf /var/lib/apt/lists/*

# Copy all files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask runs on
EXPOSE 5000

# Start the app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
