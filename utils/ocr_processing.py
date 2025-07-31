import pytesseract
from PIL import Image
from transformers import pipeline
import os

# Configure pytesseract path if needed (e.g., on Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load a pre-trained Document Question Answering model from Hugging Face
# You might need to experiment with different models based on performance and specific needs.
# 'impira/layoutlm-invoices' or 'naver-clova-ix/donut-base-finetuned-cord' could also be good.
# For a general DocVQA, 'impira/layoutlm-document-qa' or 'derekmerck/document_qa_manga' could work.
# Let's try one for invoice specifically.
# Note: The first time you run this, it will download the model, which can take a while.
try:
    qa_pipeline = pipeline("document-question-answering", model="impira/layoutlm-invoices")
    print("Hugging Face Document Question Answering pipeline loaded successfully.")
except Exception as e:
    print(f"Error loading Hugging Face pipeline: {e}")
    print("Please ensure you have 'transformers' and 'torch' installed.")
    print("You might need to install specific PyTorch/TensorFlow versions compatible with your GPU if available.")
    qa_pipeline = None # Set to None if loading fails


def perform_ocr(image_path):
    """
    Performs OCR on an image and returns the raw text.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        print(f"Error during OCR with Pytesseract for {image_path}: {e}")
        return ""

def extract_info_with_dl(image_path, questions):
    """
    Extracts information using a Hugging Face Document Question Answering model.

    Args:
        image_path (str): Path to the input image.
        questions (list): A list of questions to ask the model (e.g., ["What is the invoice number?"]).

    Returns:
        dict: A dictionary where keys are questions and values are the model's answers.
    """
    if qa_pipeline is None:
        return {"error": "Deep Learning model not loaded. Please check dependencies."}

    try:
        img = Image.open(image_path).convert("RGB") # Ensure image is in RGB format
        results = {}
        for q in questions:
            # For simplicity, we assume the model can directly answer from the image.
            # More complex scenarios might involve preprocessing the image/text.
            answer = qa_pipeline(image=img, question=q)
            if answer:
                results[q] = answer[0]['answer']
            else:
                results[q] = "N/A" # No answer found
        return results
    except Exception as e:
        print(f"Error during deep learning extraction for {image_path}: {e}")
        return {"error": f"Deep Learning extraction failed: {e}"}

def post_process_invoice_data(extracted_data):
    """
    Post-processes the extracted data to format it nicely.
    This is a placeholder and would involve more complex parsing for production.
    """
    invoice_details = {
        "invoice_number": extracted_data.get("What is the invoice number?", "N/A"),
        "invoice_date": extracted_data.get("What is the invoice date?", "N/A"),
        "line_items": [] # This is the challenging part without a specialized model
    }

    # Placeholder for line item extraction
    # A true line item extraction would involve:
    # 1. Table detection (using another DL model or heuristic)
    # 2. Cell recognition within the table
    # 3. Mapping recognized text to columns (description, quantity, unit price, total)
    # For this sample, we'll try a very basic heuristic if we get raw text.
    # A DocVQA model might struggle to return structured line items directly unless fine-tuned specifically.

    # If you get raw OCR text, you can try regex for simple line item patterns:
    # For example, if line items look like "Item A 10 $10.00 $100.00"
    # raw_text = perform_ocr(image_path) # You'd pass this from the main app
    # lines = raw_text.split('\n')
    # for line in lines:
    #     if re.match(r'.*\d+\s+\$?[\d\.]+\s+\$?[\d\.]+', line): # Very basic pattern
    #         invoice_details["line_items"].append({"raw_line": line.strip()})
    
    # Given the DocVQA approach, we ask specific questions.
    # For line items, you might need to ask "What are the items listed?", "What is the quantity of X?", etc.
    # This sample will keep line item extraction simple or leave it as a future enhancement.
    # For a sample, it's acceptable to show how the *framework* can support this,
    # even if the specific pre-trained model doesn't give perfect structured output.

    return invoice_details

if __name__ == "__main__":
    # Example usage:
    # Make sure you have a sample_invoice.jpg in the root or uploads/
    sample_image_path = "uploads/invoice1.png" # Assume you have this file
    if os.path.exists(sample_image_path):
        # Example questions
        invoice_questions = [
            "What is the invoice number?",
            "What is the date of the invoice?",
            "What is the total amount?",
            "What are the line items?", # This question will likely return raw text or struggle with structure
            "What is the vendor name?",
            "What is the bill to address?"
        ]
        extracted = extract_info_with_dl(sample_image_path, invoice_questions)
        print("\nDeep Learning Extraction Results:")
        for q, a in extracted.items():
            print(f"- {q}: {a}")

        processed_data = post_process_invoice_data(extracted)
        print("\nPost-processed Invoice Data (Simplified):")
        print(processed_data)

    else:
        print(f"Sample image '{sample_image_path}' not found. Please place an invoice image in the 'uploads/' directory.")