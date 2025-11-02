#!/bin/bash
# Railway Deployment Start Script for StyleSense.AI Backend
# This script starts the FastAPI/Flask backend using Gunicorn with production settings

# Exit on any error
set -e

# Log startup information
echo "🚀 Starting StyleSense.AI Backend..."
echo "📦 Python version: $(python --version)"
echo "🌍 Environment: ${FLASK_ENV:-production}"

# Verify required environment variables
if [ -z "$MONGODB_URI" ]; then
    echo "⚠️  Warning: MONGODB_URI not set - database features will be limited"
fi

if [ -z "$HF_API_KEY" ]; then
    echo "⚠️  Warning: HF_API_KEY not set - ML features may be limited"
fi

if [ -z "$OPENWEATHER_API_KEY" ]; then
    echo "⚠️  Warning: OPENWEATHER_API_KEY not set - weather-based recommendations unavailable"
fi

# Set default port if not provided
PORT=${PORT:-5000}
echo "🔌 Using PORT: $PORT"

# Set default number of workers (2 * CPU cores + 1)
WORKERS=${WORKERS:-4}
echo "👷 Using $WORKERS workers"

# Set worker timeout (important for ML model operations)
TIMEOUT=${TIMEOUT:-120}
echo "⏱️  Worker timeout: ${TIMEOUT}s"

# Start Gunicorn with optimized settings for Railway
echo "✨ Starting Gunicorn..."
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers $WORKERS \
    --timeout $TIMEOUT \
    --worker-class sync \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    --capture-output \
    --enable-stdio-inheritance \
    app:app
