@echo off
REM Quick start script for AI Document Analyzer (Windows)

echo 🚀 AI Document Analyzer - Quick Start
echo ======================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    echo ✓ Virtual environment created
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo 📥 Installing dependencies...
    pip install -q -r requirements.txt
    echo ✓ Dependencies installed
) else (
    echo ✓ Dependencies already installed
)

REM Check for .env file
if not exist ".env" (
    echo ⚠️  Warning: .env file not found
    echo    Create .env from .env.example and add your API key
    echo    copy .env.example .env
    echo.
)

REM Start the application
echo 🌟 Starting Streamlit application...
echo    The app will open in your browser at http://localhost:8501
echo    Press Ctrl+C to stop
echo.
streamlit run app.py
