import os
import sys
import re
from PIL import Image, ImageOps
import fitz  # PyMuPDF
import subprocess

def tiff_to_pdf(input_folder, output_pdf):
    try:
        # Step 1: List and sort TIFF files by page number at the end of filename
        tiff_files = sorted(
            [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.tiff') or f.endswith('.tif')],
            key=lambda x: int(re.search(r'_(\d+)\.tif{1,2}$', x).group(1)) if re.search(r'_(\d+)\.tif{1,2}$', x) else float('inf')
        )

        # Create a blank document to merge images as PDF pages
        pdf_document = fitz.open()

        for index, tiff_file in enumerate(tiff_files):
            try:
                # Open each TIFF file and convert to RGB mode
                img = Image.open(tiff_file).convert("RGB")

                if index != 0 and index != len(tiff_files) - 1:
                    # Rotate the image 1-2 degrees to the left for all but the cover page and the last page
                    img = img.rotate(0.80, expand=True)

                # Apply border removal
                img = ImageOps.crop(img, border=45)  # Adjust border value as needed

                # Save the image to a temporary PDF file
                temp_pdf_path = tiff_file.replace('.tif', '.pdf').replace('.tiff', '.pdf')
                img.save(temp_pdf_path, "PDF")

                # Open the temporary PDF and insert it into the main document
                temp_pdf = fitz.open(temp_pdf_path)
                pdf_document.insert_pdf(temp_pdf)
                temp_pdf.close()

                # Delete the temporary PDF file
                os.remove(temp_pdf_path)
            except Exception as e:
                print(f"Error processing file {tiff_file}: {e}")

        # Save the combined PDF
        pdf_document.save(output_pdf)
        pdf_document.close()

        print(f"PDF saved as: {output_pdf}")

        # Step 3: OCR to make PDF searchable (OCRmyPDF required)
        searchable_pdf = output_pdf.replace('.pdf', '_searchable.pdf')
        subprocess.run(['ocrmypdf', '--skip-text', output_pdf, searchable_pdf], check=True)
        print(f"Searchable PDF saved as: {searchable_pdf}")

    except Exception as e:
        print(f"Error creating PDF: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python tiff_to_pdf.py <input_folder> <output_pdf>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_pdf = sys.argv[2]
    tiff_to_pdf(input_folder, output_pdf)
