# Masters India Invoice Information Extractor (Sample)

This project demonstrates a basic invoice information extraction system using Python, Flask, and Hugging Face Transformers for document understanding. It aims to extract key fields like invoice number, date, and provides a framework for scalable key-value pair extraction.

## Features

- **Invoice Image/PDF Upload:** Upload JPG, JPEG, PNG image files or PDF documents.
- **PDF to Image Conversion:** Automatically converts the first page of an uploaded PDF to an image for processing.
- **Deep Learning based Information Extraction:** Leverages a pre-trained Hugging Face Document Question Answering (DocVQA) model (`impira/layoutlm-invoices`) to extract information based on natural language queries.
- **Basic OCR Fallback:** If the deep learning model encounters an error, it performs a basic OCR using `pytesseract` to show the raw text content.
- **Simple Flask Web UI:** A user-friendly interface to upload files and view extraction results.
- **Scalable Approach:** The use of a DocVQA model demonstrates a flexible approach to extract various fields without rigid templates.

## Technical Stack

- **Backend:** Python 3, Flask
- **Machine Learning:**
  - `transformers` (Hugging Face) for pre-trained deep learning models (e.g., LayoutLM-based)
  - `torch` (PyTorch) as the backend for the Hugging Face model
  - `pytesseract` for Optical Character Recognition (OCR)
- **Image/PDF Processing:** `Pillow` (PIL), `pdf2image`
- **UI:** HTML, CSS

## Scope of Improvement
- Accuracy of Extraction will be increased by fine tunning on some particular dataset
