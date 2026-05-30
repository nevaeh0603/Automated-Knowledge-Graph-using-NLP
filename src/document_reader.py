import pdfplumber #best for text extraction from PDF
import PyPDF2 #backup if PDF fails
from docx import Document   
import os  

''' 4 functions -> 1. Read PDF  2. Read TXT  3. Read Docx  4. Detect file type automatically'''

#Read PDF using pdfplumber
def read_pdf_pdfplumber(filepath):
    text=" "
    try:
        with pdfplumber.open(filepath) as pdf: #with automatically closes the opened file
            for page in pdf.pages:
                page_text= page.extract_text()
                if page_text:
                    text+=page_text + "\n"
    except Exception as e:
        print("pdfplumber failed! ", e)
    return text

#Backup PDF reader
def read_pdf_PyPDF2(filepath):
    text=" "
    try: 
        with open(filepath, "rb") as file:
            reader= PyPDF2.PdfReader(file)
            for page in reader.pages:
                text+=page.extract_text() + "\n"
    except Exception as e:
        print("PyPDF failed! ",e)
    return text

#Read txt
def read_text(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print("TXT read failed: ",e)
        return " "

def read_docx(filepath):
    text=" "
    try:
        doc=Document(filepath)
        for para in doc.paragraphs:
            text+=para.text+"\n"
    except Exception as e:
        print("Docx read failed: ",e)
    return text
    
#Main Function  
def extract_text_document(filepath):
    file_extension=os.path.splitext(filepath)[1] #extension-> .pdf, .py, .txt, .docx| splits the path root and file extension and takes out the extension
    file_extension=file_extension.lower().strip()

    print("Detected file extension: ", file_extension)

    if file_extension==".pdf":
        text= read_pdf_pdfplumber(filepath)

        #if pdfplumber fails
        if len(text.strip())==0:
            print("Switching to PyPDF2...")
            text=read_pdf_PyPDF2(filepath)

        return text
    
    elif file_extension==".txt":
        return read_text(filepath)
    
    elif file_extension==".docx":
        return read_docx(filepath)
    
    else:
        print("Unsupported file format!")
        return " "