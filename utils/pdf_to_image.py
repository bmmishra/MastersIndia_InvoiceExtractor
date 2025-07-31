import os
from pdf2image import convert_from_path
from PIL import Image

def convert_pdf_to_images(pdf_path, output_folder=".", dpi=300):
    """
    Converts a PDF file to a list of PIL Image objects.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_folder (str): Folder to save temporary images (not directly used in this version,
                             but convert_from_path can save to file).
        dpi (int): Dots per inch for image resolution.

    Returns:
        list: A list of PIL Image objects, one for each page of the PDF.
              Returns an empty list if conversion fails.
    """
    try:
        images = convert_from_path(pdf_path, dpi=dpi)
        print(f"Successfully converted {pdf_path} to {len(images)} image(s).")
        return images
    except Exception as e:
        print(f"Error converting PDF {pdf_path} to image: {e}")
        return []

if __name__ == "__main__":
    # Example usage:
    # Create a dummy PDF for testing if you don't have one
    # from reportlab.pdfgen import canvas
    # c = canvas.Canvas("dummy_invoice.pdf")
    # c.drawString(100, 750, "Invoice No: INV-2025-001")
    # c.drawString(100, 730, "Date: 2025-07-31")
    # c.drawString(100, 710, "Item 1: 10 @ $5.00 = $50.00")
    # c.drawString(100, 690, "Item 2: 5 @ $10.00 = $50.00")
    # c.save()

    # Assuming you have a PDF named 'sample_invoice.pdf' in the root
    sample_pdf_path = "sample_invoice.pdf" # Replace with your actual PDF path for testing
    if os.path.exists(sample_pdf_path):
        output_dir = "temp_images"
        os.makedirs(output_dir, exist_ok=True)
        converted_images = convert_pdf_to_images(sample_pdf_path, output_folder=output_dir)
        for i, img in enumerate(converted_images):
            img.save(os.path.join(output_dir, f"page_{i+1}.jpg"))
            print(f"Saved page {i+1} to {os.path.join(output_dir, f'page_{i+1}.jpg')}")
    else:
        print(f"Sample PDF '{sample_pdf_path}' not found. Please create or provide one for testing.")