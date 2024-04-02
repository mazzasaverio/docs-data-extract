import os
import json
from PyPDF2 import PdfReader
from langchain_community.document_loaders import UnstructuredPDFLoader


def extract_text_with_pypdf2(input_file_path):
    with open(input_file_path, "rb") as file:
        pdf = PdfReader(file)
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text


def extract_text_with_langchain(input_file_path):
    loader = UnstructuredPDFLoader(input_file_path)
    pages = loader.load_and_split()
    text = "".join([page.page_content for page in pages])
    return text


def save_extracted_text_to_json(data, output_dir, file_name):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, file_name + ".json")
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
    print(f"Extracted text saved as {output_path}")


def extract_text_from_pdf(input_file_path, output_dir_path, method="pypdf2"):
    file_name = os.path.splitext(os.path.basename(input_file_path))[0]

    if method == "pypdf2":
        text = extract_text_with_pypdf2(input_file_path)
    elif method == "langchain":
        text = extract_text_with_langchain(input_file_path)
    else:
        raise ValueError(f"Invalid extraction method: {method}")

    data = {"id": file_name, "file_name": file_name + ".pdf", "text_extracted": text}

    save_extracted_text_to_json(data, output_dir_path, file_name)


if __name__ == "__main__":
    input_file_path = (
        "/home/sam/github/docs-data-extract/data/raw/230829 - FED Cattolica.pdf"
    )
    output_dir_path = "/home/sam/github/docs-data-extract/data/extraction"

    method = "langchain"

    extract_text_from_pdf(input_file_path, output_dir_path, method)
