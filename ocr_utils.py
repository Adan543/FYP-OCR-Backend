import json

import fitz
import os

from flask import jsonify
from google_drive_ocr import GoogleOCRApplication

# Initialize OCR client
client_secret_path = 'c_s.json'
ocr = GoogleOCRApplication(client_secret=client_secret_path)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def convert_pdf_to_images(pdf_path):
    """Convert PDF to images using PyMuPDF."""
    pdf_document = fitz.open(pdf_path)
    images = []

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        image_path = os.path.join(UPLOAD_FOLDER, f"page_{page_num}.png")
        pix.save(image_path)
        images.append(image_path)

    return images


def clean_ocr_output(text):
    """Removes unnecessary blank lines and unwanted lines from OCR output."""
    text = text.strip()  # Remove leading/trailing spaces
    lines = text.split("\n")  # Split into lines

    # Remove unwanted first line (like a separator or header)
    filtered_lines = [line for line in lines if line.strip() and not line.startswith("﻿")]

    return "\n".join(filtered_lines)  # Rejoin lines


def perform_image_ocr(image_path):
    """Perform OCR on an image file and clean the output."""
    extracted_texts = []
    output_path = ocr.get_output_path(image_path)
    status = ocr.perform_ocr(image_path, output_path)

    if status.value in ['Done!', 'Already done!']:
        with open(output_path, 'r', encoding='utf8') as output_file:
            extracted_texts.append(clean_ocr_output(output_file.read()))

        os.remove(image_path)
        os.remove(output_path)

    return jsonify({"status": True, "data": extracted_texts})

def perform_image_ocr_for_pdf(image_path):
    """Perform OCR on an image file and clean the output."""
    extracted_texts = []
    output_path = ocr.get_output_path(image_path)
    status = ocr.perform_ocr(image_path, output_path)

    if status.value in ['Done!', 'Already done!']:
        with open(output_path, 'r', encoding='utf8') as output_file:
            extracted_texts.append(clean_ocr_output(output_file.read()))

        os.remove(image_path)
        os.remove(output_path)

    return extracted_texts


def perform_pdf_ocr(pdf_path):
    """Perform OCR on a PDF file by converting it to images first."""
    extracted_texts = []
    images = convert_pdf_to_images(pdf_path)

    extracted_texts = []

    for img_path in images:
        ocr_output = perform_image_ocr_for_pdf(img_path)

        extracted_texts.append(ocr_output[0])

    # Remove the PDF file after processing
    os.remove(pdf_path)

    return jsonify({"status": True, "data": extracted_texts}), 200