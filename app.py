"""
AI-Based Document Analyzer - Streamlit Application
Main application for uploading and analyzing documents using AI.
"""

import streamlit as st
import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv
from document_parser import DocumentParser
from ai_analyzer import AIDocumentAnalyzer

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Document Analyzer",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
if 'analyzed_documents' not in st.session_state:
    st.session_state.analyzed_documents = []

def main():
    """Main application function."""
    
    # Header
    st.title("📄 AI-Based Document Analyzer")
    st.markdown("""
    Upload your documents (PDF, Word, Excel, PowerPoint) and let AI analyze them!
    Get automated insights including creation dates, summaries, and suggested categories.
    """)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # AI Provider selection
        ai_provider = st.selectbox(
            "Select AI Provider",
            ["openai", "gemini"],
            help="Choose between OpenAI or Google Gemini"
        )
        
        # API Key input
        api_key = st.text_input(
            f"{ai_provider.upper()} API Key",
            type="password",
            help="Enter your API key or set it in .env file"
        )
        
        st.markdown("---")
        
        st.markdown("""
        ### 📚 Supported Formats
        - PDF (.pdf)
        - Word (.docx)
        - Excel (.xlsx)
        - PowerPoint (.pptx)
        
        ### 🤖 Analysis Features
        - Creation date extraction
        - Last revision date
        - Content summary
        - Category suggestion
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload Documents")
        
        # File uploader (supports multiple files)
        uploaded_files = st.file_uploader(
            "Choose document(s)",
            type=['pdf', 'docx', 'xlsx', 'pptx'],
            accept_multiple_files=True,
            help="You can upload multiple documents at once"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} document(s) uploaded")
            
            # Analyze button
            if st.button("🔍 Analyze Documents", type="primary"):
                analyze_documents(uploaded_files, ai_provider, api_key)
    
    with col2:
        st.subheader("📊 Quick Stats")
        if st.session_state.analyzed_documents:
            total_docs = len(st.session_state.analyzed_documents)
            categories = {}
            for doc in st.session_state.analyzed_documents:
                cat = doc.get('category', 'Unknown')
                categories[cat] = categories.get(cat, 0) + 1
            
            st.metric("Total Documents Analyzed", total_docs)
            st.markdown("**Categories Distribution:**")
            for cat, count in categories.items():
                st.write(f"- {cat}: {count}")
    
    # Display results
    if st.session_state.analyzed_documents:
        st.markdown("---")
        st.subheader("📋 Analysis Results")
        
        # Option to clear results
        if st.button("🗑️ Clear All Results"):
            st.session_state.analyzed_documents = []
            st.rerun()
        
        # Display each analyzed document
        for idx, doc_analysis in enumerate(st.session_state.analyzed_documents):
            with st.expander(f"📄 {doc_analysis['file_name']}", expanded=(idx == len(st.session_state.analyzed_documents) - 1)):
                display_analysis_results(doc_analysis)


def analyze_documents(uploaded_files, ai_provider, api_key):
    """Process and analyze uploaded documents."""
    
    # Validate API key
    if not api_key:
        # Try to get from environment
        if ai_provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
        else:
            api_key = os.getenv("GOOGLE_API_KEY")
        
        if not api_key:
            st.error(f"❌ Please provide an API key for {ai_provider.upper()} in the sidebar or .env file")
            return
    
    # Initialize parsers and analyzer
    parser = DocumentParser()
    
    try:
        analyzer = AIDocumentAnalyzer(provider=ai_provider, api_key=api_key)
    except Exception as e:
        st.error(f"❌ Error initializing AI analyzer: {str(e)}")
        return
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Process each file
    for idx, uploaded_file in enumerate(uploaded_files):
        try:
            status_text.text(f"Processing: {uploaded_file.name}")
            
            # Save uploaded file to temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Parse document
            with st.spinner(f"Parsing {uploaded_file.name}..."):
                document_data = parser.parse_document(tmp_file_path)
            
            # Analyze with AI
            with st.spinner(f"Analyzing {uploaded_file.name} with AI..."):
                analysis_results = analyzer.analyze_document(document_data)
            
            # Store results
            st.session_state.analyzed_documents.append(analysis_results)
            
            # Clean up temp file
            os.unlink(tmp_file_path)
            
            # Update progress
            progress_bar.progress((idx + 1) / len(uploaded_files))
            
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
            # Clean up temp file if it exists
            if 'tmp_file_path' in locals() and os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)
    
    status_text.text("✅ All documents processed!")
    progress_bar.empty()
    status_text.empty()
    
    st.success(f"🎉 Successfully analyzed {len(uploaded_files)} document(s)!")
    st.rerun()


def display_analysis_results(doc_analysis):
    """Display analysis results in a structured format."""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📅 Creation Date:**")
        st.info(doc_analysis.get('creation_date', 'Not available'))
        
        st.markdown("**🔄 Last Revision Date:**")
        st.info(doc_analysis.get('revision_date', 'Not available'))
    
    with col2:
        st.markdown("**📁 Suggested Category:**")
        category = doc_analysis.get('category', 'Uncategorized')
        st.success(category)
    
    st.markdown("**📝 Summary:**")
    summary = doc_analysis.get('summary', 'No summary available')
    st.write(summary)


if __name__ == "__main__":
    main()
