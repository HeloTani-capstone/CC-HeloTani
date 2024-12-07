FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and application files
COPY requirements.txt ./
COPY . ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Command to run the app
CMD ["python", "api.py"]
