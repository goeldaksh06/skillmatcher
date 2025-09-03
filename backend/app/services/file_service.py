import os
import PyPDF2
from docx import Document
from werkzeug.utils import secure_filename
from typing import Optional, Tuple

class FileService:
    """Service for file upload and parsing operations"""
    
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    
    @staticmethod
    def allowed_file(filename: str) -> bool:
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in FileService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def save_uploaded_file(file, upload_folder: str) -> Tuple[bool, str, Optional[str]]:
        """
        Save uploaded file and return success status, filename, and file path
        
        Returns:
            tuple: (success: bool, message: str, file_path: Optional[str])
        """
        if not file or file.filename == '':
            return False, "No file selected", None
        
        if not FileService.allowed_file(file.filename):
            return False, f"File type not allowed. Supported: {', '.join(FileService.ALLOWED_EXTENSIONS)}", None
        
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            return True, "File uploaded successfully", file_path
        except Exception as e:
            return False, f"Error saving file: {str(e)}", None
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> Tuple[bool, str]:
        """
        Extract text from PDF file
        
        Returns:
            tuple: (success: bool, text_content: str)
        """
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                return True, text.strip()
        except Exception as e:
            return False, f"Error reading PDF: {str(e)}"
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> Tuple[bool, str]:
        """
        Extract text from DOCX file
        
        Returns:
            tuple: (success: bool, text_content: str)
        """
        try:
            doc = Document(file_path)
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return True, text.strip()
        except Exception as e:
            return False, f"Error reading DOCX: {str(e)}"
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> Tuple[bool, str]:
        """
        Extract text from TXT file
        
        Returns:
            tuple: (success: bool, text_content: str)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return True, text.strip()
        except Exception as e:
            return False, f"Error reading TXT: {str(e)}"
    
    @staticmethod
    def parse_resume_file(file_path: str) -> Tuple[bool, str]:
        """
        Parse resume file and extract text based on file extension
        
        Returns:
            tuple: (success: bool, text_content: str)
        """
        if not os.path.exists(file_path):
            return False, "File not found"
        
        file_extension = file_path.lower().split('.')[-1]
        
        if file_extension == 'pdf':
            return FileService.extract_text_from_pdf(file_path)
        elif file_extension == 'docx':
            return FileService.extract_text_from_docx(file_path)
        elif file_extension == 'txt':
            return FileService.extract_text_from_txt(file_path)
        else:
            return False, f"Unsupported file type: {file_extension}"