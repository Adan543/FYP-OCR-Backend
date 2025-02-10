import os
import json
from flask import Blueprint, request, render_template, jsonify
from ocr_utils import perform_image_ocr, perform_pdf_ocr, UPLOAD_FOLDER
from tts_utils import text_to_speech  # Import TTS function

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/ocr/scan-image', methods=['POST'])
def scan_image():
    """Handle image file upload and OCR processing."""
    try:
        if 'images' not in request.files:
            return jsonify({"status": False, "message": "please provide  a image"}), 500
        file = request.files.getlist('images')

        extracted_texts = []

        for each_file in file:
            if not each_file.filename.lower().endswith(('png', 'jpg', 'jpeg')):  # Now checking for each file
                return jsonify({"status": False, "message": "Invalid image format. Please upload PNG or JPG"}), 500

            file_path = os.path.join(UPLOAD_FOLDER, each_file.filename)
            each_file.save(file_path)

            ocr_response = perform_image_ocr(file_path)
            print(ocr_response)

            data = ocr_response.data
            if isinstance(data, bytes):
                data = data.decode('utf-8')  # Decode bytes to a UTF-8 string
            if isinstance(data, str):
                data = json.loads(data)  # Convert JSON string to a dictionary if necessary

            # Extract just the text data from ocr_response
            extracted_texts.append({
                'filename': each_file.filename,
                'status': ocr_response.status,
                'data': data.get('data', 'unable to extract text') if isinstance(data, dict) else data
            })

        return extracted_texts

    except Exception as e:
        return jsonify({'status':False, "message" : str(e)}), 500

@routes.route('/ocr/scan-pdf', methods=['POST'])
def scan_pdf():
    """Handle PDF file upload and OCR processing."""
    try:
        if 'file' not in request.files:
            return jsonify({"status": False, "message": "No PDF uploaded"}), 500

        file = request.files['file']
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"status": False, "message": "Invalid PDF format"}), 500

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        extracted_texts = perform_pdf_ocr(file_path)

        # if (not (extracted_texts.status)):
        #     return jsonify({'status': False, "message": extracted_texts.message}), 500

        return extracted_texts

    except Exception as e:
        return jsonify({'status':False, "message" : str(e)}), 500
@routes.route('/tts', methods=['POST'])
def generate_tts():
    """Convert text to speech and return Base64 encoded audio."""
    try:
        data = request.json
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "اردو متن فراہم کریں۔"}), 400

        base64_audio = text_to_speech(text)
        return jsonify({"audio_base64": base64_audio, "status": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500