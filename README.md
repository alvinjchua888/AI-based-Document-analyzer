# AI-Based Document Analyzer 📄🤖

An intelligent document analysis application built with **Streamlit**, **LangChain**, and **OpenAI/Gemini**. This tool allows users to upload documents (PDF, Word, Excel, PowerPoint) and automatically extract key information including creation dates, revision dates, content summaries, and category suggestions.

## 📸 Application Screenshot

![AI Document Analyzer Interface](https://github.com/user-attachments/assets/178db276-d181-4214-b662-17c1907c890c)

*The main interface showing the configuration sidebar, document upload area, and quick stats dashboard*

## Features ✨

- **Multi-Format Support**: Upload PDF, Word (.docx), Excel (.xlsx), and PowerPoint (.pptx) files
- **Bulk Upload**: Analyze multiple documents at once
- **AI-Powered Analysis**: Uses OpenAI GPT or Google Gemini for intelligent document analysis
- **Automatic Extraction**:
  - Document creation date
  - Last revision date
  - Content summary (AI-generated)
  - Suggested category for classification
- **User-Friendly Interface**: Built with Streamlit for an intuitive web interface
- **Metadata Extraction**: Pulls metadata from document properties when available

## Technology Stack 🛠️

- **Frontend**: Streamlit
- **AI Framework**: LangChain
- **AI Models**: OpenAI GPT-3.5 or Google Gemini Pro
- **Document Processing**:
  - PyPDF2 (PDF files)
  - python-docx (Word documents)
  - openpyxl (Excel spreadsheets)
  - python-pptx (PowerPoint presentations)

## Installation 🚀

### Prerequisites

- Python 3.8 or higher
- OpenAI API key or Google Gemini API key

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/alvinjchua888/AI-based-Document-analyzer.git
   cd AI-based-Document-analyzer
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API keys**
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API key:
   ```
   # For OpenAI
   AI_PROVIDER=openai
   OPENAI_API_KEY=your_openai_api_key_here
   
   # OR for Google Gemini
   AI_PROVIDER=gemini
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## User Interface 🎨

The application features a clean, intuitive interface with three main sections:

### Left Sidebar - Configuration
- **AI Provider Selection**: Choose between OpenAI or Google Gemini
- **API Key Input**: Securely enter your API credentials
- **Supported Formats**: Quick reference of accepted file types
- **Analysis Features**: List of extraction capabilities

### Main Area - Document Upload
- **Drag & Drop Zone**: Simply drag files or click "Browse files"
- **Multi-File Support**: Upload multiple documents at once
- **Format Validation**: Automatic checking for supported formats
- **Progress Tracking**: Real-time analysis progress

### Right Side - Quick Stats
- **Document Count**: Total analyzed documents
- **Category Distribution**: Breakdown by suggested categories
- **Results Display**: Expandable sections showing analysis results

## Usage 📖

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   
   The app will automatically open at `http://localhost:8501`

3. **Configure settings**
   - Select your AI provider (OpenAI or Gemini) in the sidebar
   - Enter your API key (if not set in .env)

4. **Upload documents**
   - Click "Browse files" or drag and drop documents
   - You can upload multiple files at once
   - Supported formats: PDF, DOCX, XLSX, PPTX

5. **Analyze**
   - Click "Analyze Documents" button
   - Wait for the AI to process your documents
   - View results including dates, summaries, and categories

## How It Works 🔍

1. **Document Parsing**: The application extracts text content and metadata from uploaded documents
2. **Metadata Extraction**: Pulls creation and modification dates from document properties
3. **AI Analysis**: Sends document content to LangChain with OpenAI/Gemini for analysis
4. **Information Extraction**: AI extracts:
   - Creation and revision dates (from content if not in metadata)
   - Concise summary of document content
   - Suggested category for classification
5. **Results Display**: Shows all extracted information in a user-friendly format

## Supported Document Categories 📁

The AI can suggest classifications including:
- Financial Report
- Technical Documentation
- Business Proposal
- Legal Document
- Research Paper
- Meeting Minutes
- Marketing Material
- Project Plan
- Training Material
- Policy Document
- And more...

## Project Structure 📂

```
AI-based-Document-analyzer/
├── app.py                  # Main Streamlit application
├── document_parser.py      # Document parsing utilities
├── ai_analyzer.py         # AI analysis module
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## API Keys 🔑

### OpenAI API Key
1. Sign up at [OpenAI Platform](https://platform.openai.com/)
2. Navigate to API Keys section
3. Create a new API key
4. Add to `.env` file

### Google Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add to `.env` file

## Troubleshooting 🔧

**Issue**: "No module named 'streamlit'"
- **Solution**: Make sure you've installed dependencies: `pip install -r requirements.txt`

**Issue**: "Invalid API key"
- **Solution**: Check that your API key is correct in the `.env` file or sidebar

**Issue**: "Error parsing document"
- **Solution**: Ensure the document is not corrupted and is in a supported format

**Issue**: Document text is incomplete
- **Solution**: Some documents may have encoding issues. Try re-saving the document and uploading again

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is open source and available under the MIT License.

## Acknowledgments 🙏

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://langchain.com/)
- AI models from [OpenAI](https://openai.com/) and [Google](https://ai.google.dev/)

## Support 💬

For issues, questions, or suggestions, please open an issue on GitHub.
