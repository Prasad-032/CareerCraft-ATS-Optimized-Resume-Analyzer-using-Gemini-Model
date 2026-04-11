import PyPDF2
import streamlit as st

def extract_text_from_pdf(uploaded_file):
    """Extract text from PDF or DOCX resume files."""
    filename = uploaded_file.name.lower()

    if filename.endswith(".pdf"):
        return _extract_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return _extract_docx(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload a PDF or DOCX file.")
        return ""

def _extract_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        st.error(f"Failed to read PDF: {e}")
        return ""

def _extract_docx(uploaded_file):
    try:
        from docx import Document
        import io
        doc = Document(io.BytesIO(uploaded_file.read()))
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    except ImportError:
        st.error("DOCX support requires `python-docx`. Run: pip install python-docx")
        return ""
    except Exception as e:
        st.error(f"Failed to read DOCX: {e}")
        return ""
