FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Add a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy the requirements file first for better caching
COPY requirement.txt ./ 

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirement.txt

# Copy the rest of the application files
COPY . ./ 

# Ensure the model folder is copied
COPY model/ ./model/ 

# Change ownership and switch to non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Command to run the app using Gunicorn instead of Flask's built-in server
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "--threads", "4", "api:app"]