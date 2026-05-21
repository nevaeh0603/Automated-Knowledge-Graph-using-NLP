import pdfplumber #best for text extraction
import PyPDF2 #backup if PDF fails
import os

''' 3 functions -> 1. Read PDF  2. Read TXT  3. Detect file type automatically'''

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
    
#Main Function  
def extract_text_document(filepath):
    file_extension=os.path.splitext(filepath)[1] #extension-> .pdf, .py, .txt| splits the path root and file extension and takes out the extension
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
    
    else:
        print("Unsupported file format!")
        return " "