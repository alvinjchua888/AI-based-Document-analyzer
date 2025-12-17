# Usage Guide

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/alvinjchua888/AI-based-Document-analyzer.git
cd AI-based-Document-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your API key:

**For OpenAI:**
```
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-api-key-here
```

**For Google Gemini:**
```
AI_PROVIDER=gemini
GOOGLE_API_KEY=your-google-api-key-here
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

## Features Overview

### Document Upload

- **Single Upload**: Upload one document at a time
- **Bulk Upload**: Upload multiple documents simultaneously
- **Supported Formats**: PDF, DOCX, XLSX, PPTX

### Analysis Output

For each document, you'll receive:

1. **Creation Date**: When the document was first created
2. **Revision Date**: When the document was last modified
3. **Summary**: AI-generated summary of the content
4. **Category**: Suggested classification category

### AI Provider Selection

You can choose between two AI providers:

#### OpenAI (GPT-3.5-Turbo)
- **Pros**: Fast, reliable, well-tested
- **Cost**: Pay per token
- **API**: https://platform.openai.com/

#### Google Gemini (Gemini-Pro)
- **Pros**: Competitive pricing, good performance
- **Cost**: Free tier available
- **API**: https://makersuite.google.com/

## Usage Examples

### Example 1: Analyzing a Single Financial Report

1. Upload a PDF financial report
2. Select "OpenAI" as provider
3. Click "Analyze Documents"
4. Review the extracted information:
   - Creation date
   - Summary of financial data
   - Category: "Financial Report"

### Example 2: Bulk Processing Meeting Minutes

1. Select multiple DOCX files containing meeting minutes
2. Choose your preferred AI provider
3. Click "Analyze Documents"
4. View all analyzed documents with their summaries
5. Export or review the suggested categories

### Example 3: Analyzing Presentations

1. Upload PowerPoint files (.pptx)
2. The AI will analyze all slides
3. Get a comprehensive summary of the presentation content
4. Receive category suggestions like "Marketing Material" or "Training Material"

## Tips for Best Results

### Document Quality
- Ensure documents are not password-protected
- Use clear, readable text (avoid scanned images without OCR)
- For best results, use documents with proper formatting

### AI Analysis
- Longer documents may take more time to analyze
- Very large documents (>100 pages) may be truncated
- The AI works best with well-structured content

### API Keys
- Keep your API keys secure
- Never commit `.env` files to version control
- Monitor your API usage to avoid unexpected costs

## Troubleshooting

### Common Issues

**Problem**: Application won't start
```bash
# Solution: Check if all dependencies are installed
pip install -r requirements.txt --upgrade
```

**Problem**: API key error
```bash
# Solution: Verify your .env file
cat .env
# Ensure the key is correct and has no extra spaces
```

**Problem**: Document parsing fails
```bash
# Solution: Check file format and corruption
# Try opening the file in its native application
# Re-save and try uploading again
```

**Problem**: Out of memory errors
```bash
# Solution: For large documents, try:
# - Splitting documents into smaller files
# - Processing fewer documents at once
# - Increasing system memory
```

## Advanced Configuration

### Custom Categories

You can modify the AI analyzer to suggest custom categories by editing `ai_analyzer.py`:

```python
# In the _create_analysis_prompt method, update the category list:
For the category, choose from: Custom Category 1, Custom Category 2, etc.
```

### Adjusting AI Temperature

For more creative or conservative summaries, modify the temperature parameter:

```python
# In ai_analyzer.py, __init__ method:
self.llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.3,  # Lower = more focused, Higher = more creative
    api_key=api_key or os.getenv("OPENAI_API_KEY")
)
```

### Using Different AI Models

To use GPT-4 or other models:

```python
# In ai_analyzer.py:
self.llm = ChatOpenAI(
    model="gpt-4",  # Change to "gpt-4" or other available models
    temperature=0.3,
    api_key=api_key or os.getenv("OPENAI_API_KEY")
)
```

## Performance Optimization

### For Large Batches
- Process documents in smaller batches
- Use async processing if available
- Consider caching results

### Memory Management
- Close the app between large batch processes
- Clear analysis results regularly using the "Clear All Results" button

## Data Privacy

- Documents are processed locally and sent only to the selected AI provider
- No documents are stored permanently on servers
- API providers may have their own data retention policies
- Review your AI provider's privacy policy for details

## API Cost Management

### OpenAI
- GPT-3.5-Turbo: ~$0.002 per 1K tokens
- Monitor usage at: https://platform.openai.com/usage

### Google Gemini
- Gemini Pro: Free tier available
- Check current pricing at: https://ai.google.dev/pricing

### Tips to Reduce Costs
- Use GPT-3.5-Turbo instead of GPT-4 for most tasks
- Process only necessary documents
- Optimize document content before upload
- Consider batching similar documents

## Support

For issues or questions:
1. Check this guide first
2. Review the main README.md
3. Open an issue on GitHub
4. Contact the repository maintainer
