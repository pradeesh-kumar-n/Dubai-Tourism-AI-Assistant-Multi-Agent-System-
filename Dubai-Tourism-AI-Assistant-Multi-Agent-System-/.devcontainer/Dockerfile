FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Install system dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends curl

# Set up Python dependencies
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Copy and set up start script
COPY .devcontainer/start.sh .
RUN chmod +x start.sh

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["./start.sh"]