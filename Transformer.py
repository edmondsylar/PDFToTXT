import PyPDF2
import os
from rich.console import Console
import shutil

console = Console()


def extract_pdf_text(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        text = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    return text



def process_pdfs_in_directory(directory_path):

    completed_files = []
    broken_files = []

    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(directory_path, filename)

            try:
                text = extract_pdf_text(file_path)
                # Save the extracted text to a .txt file
                txt_filename = os.path.splitext(filename)[0] + '.txt'
                txt_file_path = os.path.join('TXTData', txt_filename)
                with open(txt_file_path, 'w') as txt_file:
                    txt_file.write(text)
                    console.print(f"Extracted text from {filename} and saved to {txt_filename}. \n")

                    # Move the processed file to the 'ProcessedFiles' directory
                    move_file('PDFs', 'ProcessedFiles', filename)
                    completed_files.append(filename)

            # If an error occurs, print a message to the console
            except:
                text = "couldn't generate text"
                console.log(f"Couldn't extract text from {filename}.")

                # add the filename to the list of broken files
                broken_files.append(filename)

                move_file('PDFs', 'BrokenFiles', filename)

    logReport = f"Processed {len(completed_files)} files and {len(broken_files)} files are broken. \n"
    console.print(logReport)
    return logReport
            


def move_file(src_folder, dest_folder, filename):
    src_path = os.path.join(src_folder, filename)
    dest_path = os.path.join(dest_folder, filename)
    shutil.move(src_path, dest_path)


def process_single_pdf(filename):
    directory_path = "PDFs/"
    file_path = os.path.join(directory_path, filename)
    if os.path.isfile(file_path) and filename.endswith(".pdf"):
        text = extract_pdf_text(file_path)

        # Save the extracted text to a .txt file
        txt_filename = os.path.splitext(filename)[0] + '.txt'
        txt_file_path = os.path.join('TXTData', txt_filename)
        with open(txt_file_path, 'w') as txt_file:
            txt_file.write(text)
            console.print(f"Extracted text from {filename} and saved to {txt_filename}. \n")
    else:
        console.print(f"{filename} does not exist in the directory or is not a PDF file. \n")

    return f"Completed processing the file. {filename} \n"


