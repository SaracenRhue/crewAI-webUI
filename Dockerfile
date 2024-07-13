FROM python:3.11-slim

# Install FFmpeg and other necessary dependencies
RUN mkdir -p /app/agents /app/tasks /data/crews \
    && chmod 777 /app/agents /app/tasks /data/crews

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8501

# Define volumes
VOLUME ["/app/agents", "/app/tasks", "/app/crews"]

# Run the application
CMD ["streamlit", "run", "main.py"]