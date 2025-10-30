# # from langchain_core.tools import tool
# # from datetime import datetime
# # from pathlib import Path
# # import subprocess
# # import shutil

# # @tool
# # def render_latex_pdf(latex_content: str) -> str:
# #     """Render a LaTeX document to PDF.
# #     If successful, returns the path to the PDF.
# #     If unsuccessful, returns a string containing the compiler error.

# #     Args:
# #         latex_content: The LaTeX document content as a string

# #     Returns:
# #         Path to the generated PDF document or an error message.
# #     """
    
# #     # 1. Check if tectonic is installed
# #     if shutil.which("tectonic") is None:
# #         return "Error: tectonic compiler is not installed on the system. Please install it to generate PDFs."

# #     output_dir = Path("output").absolute()
# #     output_dir.mkdir(exist_ok=True)
    
# #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# #     tex_filename = f"paper_{timestamp}.tex"
# #     pdf_filename = f"paper_{timestamp}.pdf"
    
# #     tex_file = output_dir / tex_filename
# #     pdf_file = output_dir / pdf_filename

# #     try:
# #         # 2. Write the .tex file
# #         tex_file.write_text(latex_content)

# #         # 3. Run the tectonic compiler
# #         #    We run this from *inside* the output directory
# #         result = subprocess.run(
# #                     ["tectonic", tex_filename, "--outdir", "."],
# #                     cwd=output_dir,
# #                     capture_output=True,
# #                     text=True,
# #                     timeout=30 # Add a timeout for safety
# #                 )

# #         # 4. Check if the compiler succeeded
# #         if result.returncode != 0:
# #             # --- THIS IS THE CRITICAL CHANGE ---
# #             # The compile failed! Return the error message to the AI.
# #             # Tectonic prints its errors to stderr.
# #             error_message = f"Error: LaTeX compilation failed.\n"
# #             error_message += f"Return Code: {result.returncode}\n"
# #             error_message += f"Stderr: {result.stderr}\n"
# #             error_message += f"Stdout: {result.stdout}"
# #             print(error_message) # For your own debugging
# #             return error_message # Return the error to the AI

# #         # 5. Check if the PDF file was actually created
# #         if not pdf_file.exists():
# #             # --- THIS IS ALSO AN ERROR TO RETURN ---
# #             return f"Error: Tectonic ran successfully, but the PDF file '{pdf_filename}' was not found in {output_dir}."

# #         # 6. Success! Return the path.
# #         success_path = str(pdf_file.absolute())
# #         print(f"Successfully generated PDF at {success_path}")
# #         return success_path

# #     except Exception as e:
# #         # --- CATCH ALL OTHER ERRORS ---
# #         # Catch other errors (like file write permissions) and return them
# #         print(f"An unexpected error occurred: {str(e)}")
# #         return f"Error: An unexpected error occurred while rendering LaTeX: {str(e)}"




# from langchain_core.tools import tool
# from datetime import datetime
# from pathlib import Path
# import subprocess
# import shutil

# @tool
# def render_latex_pdf(latex_content: str) -> str:
#     """Render a LaTeX document to PDF.
#     If successful, returns the path to the PDF.
#     If unsuccessful, returns a string containing the compiler error.

#     Args:
#         latex_content: The LaTeX document content as a string

#     Returns:
#         Path to the generated PDF document or an error message.
#     """
    
#     # 1. Check if tectonic is installed
#     if shutil.which("tectonic") is None:
#         print("Error: tectonic compiler is not installed.")
#         # Return an error message for the AI
#         return "Error: tectonic compiler is not installed on the system. Please ask the user to install it to generate PDFs."

#     # Create the output directory
#     output_dir = Path("output").absolute()
#     output_dir.mkdir(exist_ok=True)
    
#     # Define filenames
#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     tex_filename = f"paper_{timestamp}.tex"
#     pdf_filename = f"paper_{timestamp}.pdf"
    
#     tex_file = output_dir / tex_filename
#     pdf_file = output_dir / pdf_filename

#     try:
#         # 2. Write the .tex file
#         tex_file.write_text(latex_content)

#         # 3. Run the tectonic compiler
#         #    We run this from *inside* the output directory
#         result = subprocess.run(
#                     ["tectonic", tex_filename, "--outdir", "."], # Run in output_dir
#                     cwd=output_dir, # Set current working directory
#                     capture_output=True, # Capture stdout/stderr
#                     text=True,
#                     timeout=30 # Add a timeout for safety
#                 )

#         # 4. Check if the compiler succeeded
#         if result.returncode != 0:
#             # --- THIS IS THE CRITICAL CHANGE ---
#             # The compile failed! Return the error message to the AI.
#             # Tectonic prints its errors to stderr.
#             error_message = f"Error: LaTeX compilation failed.\n"
#             error_message += f"Return Code: {result.returncode}\n"
            
#             # Get the compiler's log, preferring stderr
#             compiler_output = result.stderr if result.stderr else result.stdout
            
#             # Clean up the output for the AI
#             error_message += f"Compiler Output: {compiler_output[-2000:]}" # Send last 2000 chars
            
#             print(error_message) # For your own debugging
#             return error_message # Return the error to the AI

#         # 5. Check if the PDF file was actually created
#         if not pdf_file.exists():
#             # --- THIS IS ALSO AN ERROR TO RETURN ---
#             print(f"Error: Tectonic ran but PDF not found at {pdf_file}")
#             return f"Error: Tectonic ran successfully, but the PDF file '{pdf_filename}' was not found in {output_dir}."

#         # 6. Success! Return the path.
#         success_path = str(pdf_file.absolute())
#         print(f"Successfully generated PDF at {success_path}")
#         # Return the path surrounded by backticks for easier parsing in the frontend
#         return f"Successfully generated PDF. Path: `{success_path}`"

#     except Exception as e:
#         # --- CATCH ALL OTHER ERRORS ---
#         # Catch other errors (like file write permissions) and return them
#         print(f"An unexpected error occurred: {str(e)}")
#         return f"Error: An unexpected error occurred while rendering LaTeX: {str(e)}"



from langchain_core.tools import tool
from datetime import datetime
from pathlib import Path
import subprocess
import shutil

@tool
def render_latex_pdf(latex_content: str) -> str:
    """Render a LaTeX document to PDF.
    If successful, returns a formatted string with the absolute path to the PDF.
    If unsuccessful, returns a string containing the compiler error.

    Args:
        latex_content: The LaTeX document content as a string

    Returns:
        Path to the generated PDF document or an error message.
    """
    
    # 1. Check if tectonic is installed
    if shutil.which("tectonic") is None:
        print("Error: tectonic compiler is not installed.")
        # Return an error message for the AI
        return "Error: tectonic compiler is not installed on the system. Please ask the user to install it to generate PDFs."

    # Create the output directory
    output_dir = Path("output").absolute()
    output_dir.mkdir(exist_ok=True)
    
    # Define filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    tex_filename = f"paper_{timestamp}.tex"
    pdf_filename = f"paper_{timestamp}.pdf"
    
    tex_file = output_dir / tex_filename
    pdf_file = output_dir / pdf_filename

    try:
        # 2. Write the .tex file
        tex_file.write_text(latex_content)

        # 3. Run the tectonic compiler
        #    We run this from *inside* the output directory
        result = subprocess.run(
                    ["tectonic", tex_filename, "--outdir", "."], # Run in output_dir
                    cwd=output_dir, # Set current working directory
                    capture_output=True, # Capture stdout/stderr
                    text=True,
                    timeout=30 # Add a timeout for safety
                )

        # 4. Check if the compiler succeeded
        if result.returncode != 0:
            # --- THIS IS THE CRITICAL CHANGE ---
            # The compile failed! Return the error message to the AI.
            # Tectonic prints its errors to stderr.
            error_message = f"Error: LaTeX compilation failed.\n"
            error_message += f"Return Code: {result.returncode}\n"
            
            # Get the compiler's log, preferring stderr
            compiler_output = result.stderr if result.stderr else result.stdout
            
            # Clean up the output for the AI
            error_message += f"Compiler Output: {compiler_output[-2000:]}" # Send last 2000 chars
            
            print(error_message) # For your own debugging
            return error_message # Return the error to the AI

        # 5. Check if the PDF file was actually created
        if not pdf_file.exists():
            # --- THIS IS ALSO AN ERROR TO RETURN ---
            print(f"Error: Tectonic ran but PDF not found at {pdf_file}")
            return f"Error: Tectonic ran successfully, but the PDF file '{pdf_filename}' was not found in {output_dir}."

        # 6. Success! Return the path.
        # --- THIS IS THE KEY LINE ---
        # We return a clean, parse-able string for the frontend.
        success_path = str(pdf_file.absolute())
        print(f"Successfully generated PDF at {success_path}")
        return f"Successfully generated PDF. Path: `{success_path}`"

    except Exception as e:
        # --- CATCH ALL OTHER ERRORS ---
        # Catch other errors (like file write permissions) and return them
        print(f"An unexpected error occurred: {str(e)}")
        return f"Error: An unexpected error occurred while rendering LaTeX: {str(e)}"

