# Dockerfile

# First stage: build the application
FROM python:3.9-slim AS builder

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Second stage: create the final image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the installed dependencies from the builder image
COPY --from=builder /app .

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
