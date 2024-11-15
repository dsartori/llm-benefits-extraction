# Base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install Bash and vim
RUN apt-get update && apt-get install -y bash vim && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Set the default command to Bash (will be overridden in docker-compose.yml)
CMD ["/bin/bash"]
