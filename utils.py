import io
from PyPDF2 import PdfReader
import docx
from langchain_text_splitters import RecursiveCharacterTextSplitter

def read_file(uploaded_file):
    """Reads text from an uploaded file (PDF, DOCX, TXT)."""
    if uploaded_file is None:
        return ""
    
    file_type = uploaded_file.name.split('.')[-1].lower()
    text = ""

    try:
        if file_type == 'pdf':
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        elif file_type == 'docx':
            doc = docx.Document(uploaded_file)
            for para in doc.paragraphs:
                text += para.text + "\n"
        elif file_type == 'txt':
            text = uploaded_file.read().decode("utf-8")
        else:
            return "Error: Unsupported file type."
    except Exception as e:
        return f"Error reading file: {e}"

    return text

def chunk_text(text, chunk_size=2000):
    """Splits text into manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    chunks = text_splitter.split_text(text)
    return chunks
