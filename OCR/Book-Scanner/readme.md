# Book Scanner OCR

A Python application that uses OCR to scan multiple book titles and authors from a single image of a bookshelf and save them to a text file.

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

1. Take photos of your bookshelves (you can include multiple books in each photo)
2. Run the script:
```bash
python book_scanner.py
```
3. When prompted, enter the full path to the directory containing your book images
4. The script will process all images and save the results to a text file

## Supported Image Formats
- JPG/JPEG
- PNG
- BMP

## Tips for Best Results

- Take photos of your entire bookshelf or a section of it
- Ensure good lighting conditions
- Try to capture the books straight-on, with spines clearly visible
- Make sure there's some contrast between book spines
- The script will automatically detect and process each book spine
- Each book will be saved in the format "Title - Author"

## Output

The program will create a text file named `books_YYYYMMDD_HHMMSS.txt` containing one book per line in the format:
```
Book Title - Author Name
```

## How It Works

1. The script detects individual book spines in each image using edge detection
2. It processes each detected spine to extract the text
3. It attempts to separate title and author using common indicators (by, -, etc.)
4. All books are saved to a single text file, one per line
