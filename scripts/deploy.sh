#!/bin/bash

# Mindful Minutes Deployment Script
set -e

echo "🚀 Starting deployment process..."

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the project root."
    exit 1
fi

# Load environment variables
if [ -f ".env" ]; then
    echo "📦 Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "🗄️ Running database migrations..."
flask db upgrade

# Collect static files (if needed)
echo "📁 Collecting static files..."
# This would be for production static file serving

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -v --tb=short

# Start the application
echo "🎯 Starting application..."
if [ "$FLASK_ENV" = "production" ]; then
    echo "🏗️ Starting production server..."
    gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 4 --preload
else
    echo "🔧 Starting development server..."
    flask run --host=0.0.0.0 --port=${PORT:-5000}
fi

echo "✅ Deployment completed successfully!"