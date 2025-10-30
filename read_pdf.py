# from langchain_core.tools import tool
# import io
# import PyPDF2
# import requests

# @tool
# def read_pdf(url: str) -> str:
#     """Read and extract text from a PDF file given its URL.

#     Args:
#         url: The URL of the PDF file to read

#     Returns:
#         The extracted text content from the PDF
#     """
#     try:
#         response = requests.get(url)
#         pdf_file = io.BytesIO(response.content)
#         pdf_reader = PyPDF2.PdfReader(pdf_file)
#         num_pages = len(pdf_reader.pages)
#         text = ""
#         for i, page in enumerate(pdf_reader.pages, 1):
#             print(f"Extracting text from page {i}/{num_pages}")
#             text += page.extract_text() + "\n"

#         print(f"Successfully extracted {len(text)} characters of text from PDF")
#         return text.strip()
#     except Exception as e:
#         print(f"Error reading PDF: {str(e)}")
#         raise



from langchain_core.tools import tool
import io
import PyPDF2
import requests

@tool
def read_pdf(url: str) -> str:
    """Read and extract text from a PDF file given its URL.
    On success, returns the extracted text.
    On failure, returns an error message string.

    Args:
        url: The URL of the PDF file to read

    Returns:
        The extracted text content from the PDF OR an error string.
    """
    try:
        response = requests.get(url, timeout=10) # Added a timeout
        response.raise_for_status() # Check for 404s, etc.

        pdf_file = io.BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        if pdf_reader.is_encrypted:
            # --- GOOD: Return error string ---
            return f"Error: The PDF at {url} is encrypted and cannot be read."

        text = ""
        for i, page in enumerate(pdf_reader.pages, 1):
            # print(f"Extracting text from page {i}/{num_pages}") # Too noisy
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        if not text:
             # --- GOOD: Return error string ---
            return f"Error: No text could be extracted from the PDF at {url}. It might be an image-only PDF."

        print(f"Successfully extracted {len(text)} characters of text from PDF")
        return text.strip()
        
    except PyPDF2.errors.PdfReadError as e:
        print(f"Error reading corrupt PDF: {str(e)}")
        # --- GOOD: Return error string ---
        return f"Error: The file at {url} is not a valid or is a corrupt PDF. {str(e)}"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching PDF from URL: {str(e)}")
        # --- GOOD: Return error string ---
        return f"Error: Failed to fetch the PDF from {url}. {str(e)}"
    except Exception as e:
        print(f"Error reading PDF: {str(e)}")
         # --- GOOD: Return error string ---
        return f"Error: An unexpected error occurred while reading the PDF. {str(e)}"
