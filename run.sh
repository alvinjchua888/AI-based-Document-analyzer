#!/bin/bash
# Quick start script for AI Document Analyzer

echo "🚀 AI Document Analyzer - Quick Start"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -q -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "   Create .env from .env.example and add your API key"
    echo "   cp .env.example .env"
    echo ""
fi

# Start the application
echo "🌟 Starting Streamlit application..."
echo "   The app will open in your browser at http://localhost:8501"
echo "   Press Ctrl+C to stop"
echo ""
streamlit run app.py
