# Book Scanner OCR

A Python application that uses OCR to scan book titles and authors from images of book spines and save them to a CSV file.

## Prerequisites

1. Python 3.8 or higher
2. Tesseract OCR installed on your system:
   - For Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
   - For macOS: `brew install tesseract`
   - For Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Take photos of your book spines and save them in a directory
2. Run the script:
```bash
python book_scanner.py
```
3. When prompted, enter the full path to the directory containing your book images
4. The script will process all images and save the results to a CSV file

## Supported Image Formats
- JPG/JPEG
- PNG
- BMP

## Tips for Best Results

- Ensure good lighting conditions when taking photos
- Hold the camera steady and parallel to the book spine
- Make sure the text is clearly visible and not blurry
- The first line detected will be considered the title, and the second line will be considered the author
- Try to capture one book spine per image for best results

## Output

The program will create a CSV file named `books_YYYYMMDD_HHMMSS.csv` containing:
- Title
- Author
- Image filename
- Date and time of processing
