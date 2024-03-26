import fitz
from utils import index_docs


def update_pdffile(filepath: str) -> None:
    try:
        print("before", filepath)
        pdf = fitz.open(filepath)
        print("after", filepath)
        file_content = ""
        for page in pdf:  # Iterate through each page
            file_content += page.get_text()
        if not file_content.strip():
            print("PDF is empty")
            return

        # Constructing the document with more structured data
        file_name = filepath.split("/")[-1].split(".")[0]
        doc = {
            "_id": filepath,
            "file_name": file_name,
            "text": file_content
        }
        index_docs([doc])
    except Exception as e:  # Catching a more general exception since PyMuPDF might raise different exceptions
        print(f"Error processing PDF file: {e}")
