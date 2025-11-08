from typing import List, Dict, Any
from PyPDF2 import PdfReader
from docx import Document
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from privacy_layer import PrivacyLayer

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200, epsilon: float = 1.0):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.embeddings_model = OpenAIEmbeddings()
        self.privacy_layer = PrivacyLayer(epsilon=epsilon)
    
    def load_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def load_docx(self, file_path: str) -> str:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    def load_document(self, file_path: str) -> str:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            return self.load_pdf(file_path)
        elif ext in ['.docx', '.doc']:
            return self.load_docx(file_path)
        elif ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    def chunk_text(self, text: str) -> List[str]:
        chunks = self.text_splitter.split_text(text)
        return chunks
    
    def create_embeddings(self, texts: List[str], use_privacy: bool = True) -> List[List[float]]:
        embeddings = self.embeddings_model.embed_documents(texts)
        
        if use_privacy:
            embeddings = self.privacy_layer.perturb_embeddings(embeddings)
        
        return embeddings
    
    def process_document(self, file_path: str) -> Dict[str, Any]:
        text = self.load_document(file_path)
        chunks = self.chunk_text(text)
        embeddings = self.create_embeddings(chunks, use_privacy=True)
        
        return {
            "file_name": os.path.basename(file_path),
            "full_text": text,
            "chunks": chunks,
            "embeddings": embeddings,
            "num_chunks": len(chunks),
            "privacy_protected": True
        }
