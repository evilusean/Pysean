# Book Scanner OCR

A Python application that uses OCR to scan book titles and authors from your bookshelf and save them to a CSV file.

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

1. Run the script:
```bash
python book_scanner.py
```

2. Point your camera at a book spine
3. Press SPACE to capture and process the image
4. Press ESC to quit and save the results to a CSV file

## Tips for Best Results

- Ensure good lighting conditions
- Hold the camera steady and parallel to the book spine
- Make sure the text is clearly visible and not blurry
- Adjust the camera distance to get the best focus
- The first line detected will be considered the title, and the second line will be considered the author

## Output

The program will create a CSV file named `books_YYYYMMDD_HHMMSS.csv` containing:
- Title
- Author
- Date and time of scanning
