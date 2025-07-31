import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory # Add send_from_directory here
from werkzeug.utils import secure_filename
from PIL import Image

# Import helper functions
# Import helper functions
from utils.pdf_to_image import convert_pdf_to_images # This is already there
from pdf2image import convert_from_path # ADD THIS LINE
from utils.ocr_processing import extract_info_with_dl, post_process_invoice_data, perform_ocr # Import perform_ocr for fallback/full text

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'pdf'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# --- ADD THIS NEW ROUTE TO SERVE UPLOADED FILES ---
@app.route('/uploaded_files/<filename>')
def uploaded_file(filename):
    # This serves files from the UPLOAD_FOLDER
    # It ensures secure access by not exposing the direct file system path
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
# --------------------------------------------------

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    extracted_data = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            image_paths = []
            final_image_filename = filename # Store the name of the image file that will be processed/displayed

            if filename.lower().endswith('.pdf'):
                print(f"Converting PDF: {filepath}")
                images = convert_from_path(filepath) # Call pdf2image directly here, or use convert_pdf_to_images if it returns PIL Image objects directly
                if not images:
                    return render_template('index.html', error="Failed to convert PDF to image.")
                
                # Save first page as image for processing and display
                # Use a different name to avoid conflict if original filename was long or special
                final_image_filename = filename.rsplit('.', 1)[0] + '.jpg'
                first_page_img_path = os.path.join(app.config['UPLOAD_FOLDER'], final_image_filename)
                images[0].save(first_page_img_path)
                image_to_process = first_page_img_path # This is the path for ML processing
                print(f"Saved first page of PDF as: {first_page_img_path}")
            else:
                image_to_process = filepath # This is the path for ML processing

            if image_to_process:
                # Define the questions for the DocVQA model
                invoice_questions = [
                    "What is the invoice number?",
                    "What is the invoice date?",
                    "What is the total amount?",
                    "What are the line items?",
                    "What is the vendor name?",
                    "What is the bill to address?",
                    "What is the amount due?"
                ]

                # Extract information using the deep learning model
                extracted_raw = extract_info_with_dl(image_to_process, invoice_questions)
                
                # If DL extraction fails, fall back to basic OCR for full text
                if "error" in extracted_raw:
                    full_text_ocr = perform_ocr(image_to_process)
                    extracted_raw["full_text_ocr"] = full_text_ocr
                    extracted_data = extracted_raw
                else:
                    extracted_data = post_process_invoice_data(extracted_raw)
                    extracted_data['raw_dl_answers'] = extracted_raw

            # Clean up uploaded PDF if converted, but keep the processed JPG for display
            if filename.lower().endswith('.pdf') and os.path.exists(filepath):
                os.remove(filepath) # Remove original PDF

            # --- Pass the *filename* of the image to display to the template ---
            return render_template('index.html', extracted_data=extracted_data, uploaded_image_name=final_image_filename) # Changed variable name for clarity
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)