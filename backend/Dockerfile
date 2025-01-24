
# Step 1: Builder Stage
FROM python:3.12-slim AS builder

WORKDIR /app

# Copy dependency files
COPY pyproject.toml requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels -r requirements.txt

# Copy the source code
COPY src src
RUN pip wheel --no-cache-dir --no-deps --wheel-dir wheels .

# Step 2: Runner Stage
FROM python:3.12-slim AS runner

# Create a directory for logs
RUN mkdir -p /app/logs

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

# Set the working directory
WORKDIR /app

# Ensure the log file path in the Python code points to `/app/logs/app.log`
ENV LOG_PATH=/app/logs/app.log

# Expose the application port
EXPOSE 8000

# Start the FastAPI application with uvicorn
CMD ["uvicorn", "mysite.main:app", "--host", "0.0.0.0", "--port", "8000"]
