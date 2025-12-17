"""
AI Analyzer Module
Uses LangChain with OpenAI or Gemini to analyze document content.
"""

import os
from typing import Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import json


class AIDocumentAnalyzer:
    """Analyze documents using AI to extract insights and summaries."""
    
    def __init__(self, provider: str = "openai", api_key: Optional[str] = None):
        """
        Initialize the AI analyzer.
        
        Args:
            provider: AI provider to use ('openai' or 'gemini')
            api_key: API key for the provider (if not in environment)
        """
        self.provider = provider.lower()
        
        if self.provider == "openai":
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.3,
                api_key=api_key or os.getenv("OPENAI_API_KEY")
            )
        elif self.provider == "gemini":
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-pro",
                temperature=0.3,
                google_api_key=api_key or os.getenv("GOOGLE_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'openai' or 'gemini'")
    
    def analyze_document(self, document_data: Dict) -> Dict[str, str]:
        """
        Analyze document content and extract key information.
        
        Args:
            document_data: Dictionary containing document text and metadata
            
        Returns:
            Dictionary with analysis results including creation date, 
            revision date, summary, and category
        """
        text_content = document_data.get('text_content', '')
        metadata = document_data.get('metadata', {})
        file_name = document_data.get('file_name', 'Unknown')
        
        # Extract dates from metadata if available
        creation_date = self._extract_creation_date(metadata)
        revision_date = self._extract_revision_date(metadata)
        
        # Create prompt for AI analysis
        prompt = self._create_analysis_prompt(text_content, metadata, file_name)
        
        try:
            # Get AI response
            response = self.llm.invoke(prompt)
            
            # Parse the response
            analysis = self._parse_ai_response(response.content)
            
            # Combine metadata dates with AI analysis
            result = {
                'file_name': file_name,
                'creation_date': creation_date or analysis.get('creation_date', 'Not available'),
                'revision_date': revision_date or analysis.get('revision_date', 'Not available'),
                'summary': analysis.get('summary', 'Unable to generate summary'),
                'category': analysis.get('category', 'Uncategorized')
            }
            
            return result
            
        except Exception as e:
            return {
                'file_name': file_name,
                'creation_date': creation_date or 'Not available',
                'revision_date': revision_date or 'Not available',
                'summary': f'Error analyzing document: {str(e)}',
                'category': 'Error'
            }
    
    def _extract_creation_date(self, metadata: Dict) -> Optional[str]:
        """Extract creation date from metadata."""
        # Try different metadata fields
        for field in ['created', 'creation_date', 'CreationDate']:
            if field in metadata and metadata[field]:
                date_str = str(metadata[field])
                # Clean up PDF date format (e.g., D:20230101120000)
                if date_str.startswith('D:'):
                    date_str = date_str[2:14]
                    try:
                        from datetime import datetime
                        parsed_date = datetime.strptime(date_str, '%Y%m%d%H%M%S')
                        return parsed_date.strftime('%Y-%m-%d')
                    except:
                        pass
                return date_str
        return None
    
    def _extract_revision_date(self, metadata: Dict) -> Optional[str]:
        """Extract last revision date from metadata."""
        # Try different metadata fields
        for field in ['modified', 'modification_date', 'ModDate']:
            if field in metadata and metadata[field]:
                date_str = str(metadata[field])
                # Clean up PDF date format
                if date_str.startswith('D:'):
                    date_str = date_str[2:14]
                    try:
                        from datetime import datetime
                        parsed_date = datetime.strptime(date_str, '%Y%m%d%H%M%S')
                        return parsed_date.strftime('%Y-%m-%d')
                    except:
                        pass
                return date_str
        return None
    
    def _create_analysis_prompt(self, text_content: str, metadata: Dict, file_name: str) -> list:
        """Create a structured prompt for document analysis."""
        
        # Truncate text if too long (to stay within token limits)
        max_chars = 8000
        if len(text_content) > max_chars:
            text_content = text_content[:max_chars] + "\n... (truncated)"
        
        system_message = SystemMessage(content="""You are an expert document analyzer. 
Analyze the provided document and extract the following information:
1. Creation date (if mentioned in the document content)
2. Last revision date (if mentioned in the document content)
3. A concise summary of the document content (2-3 sentences)
4. A suggested category for classification

Respond ONLY with a JSON object in this exact format:
{
    "creation_date": "YYYY-MM-DD or 'Not found in content'",
    "revision_date": "YYYY-MM-DD or 'Not found in content'",
    "summary": "Brief summary of the document",
    "category": "Suggested category"
}

For the category, choose from or suggest: Financial Report, Technical Documentation, 
Business Proposal, Legal Document, Research Paper, Meeting Minutes, Marketing Material, 
Project Plan, Training Material, Policy Document, or other relevant category.""")
        
        human_message = HumanMessage(content=f"""File name: {file_name}

Document content:
{text_content}

Metadata available:
{json.dumps(metadata, indent=2)}

Analyze this document and provide the requested information in JSON format.""")
        
        return [system_message, human_message]
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, str]:
        """Parse the AI response and extract structured data."""
        try:
            # Try to parse as JSON
            # Remove markdown code blocks if present
            response_text = response_text.strip()
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
            
            response_text = response_text.strip()
            
            parsed = json.loads(response_text)
            return {
                'creation_date': parsed.get('creation_date', 'Not available'),
                'revision_date': parsed.get('revision_date', 'Not available'),
                'summary': parsed.get('summary', 'No summary available'),
                'category': parsed.get('category', 'Uncategorized')
            }
        except json.JSONDecodeError:
            # Fallback: try to extract information from text
            return {
                'creation_date': 'Not available',
                'revision_date': 'Not available',
                'summary': response_text[:500] if response_text else 'Unable to parse response',
                'category': 'Uncategorized'
            }
