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

### Basic Usage

1. Take photos of your bookshelves (you can include multiple books in each photo)
2. Run the script in one of these ways:

```bash
# Method 1: Specify directory as argument
python book_scanner.py /path/to/images

# Method 2: Let the script prompt for directory
python book_scanner.py
```

### Command Line Options

The script supports the following command-line options:

```bash
# Force 90-degree rotation of images (useful for sideways book spines)
python book_scanner.py -r /path/to/images

# Show help message
python book_scanner.py --help
```

Options:
- `-r, --rotate`: Force 90-degree rotation of images
- `--help`: Show help message and exit

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
- If your book spines are sideways, use the `-r` flag to rotate the images

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

## Troubleshooting

If the script isn't detecting book spines correctly:
1. Try using the `-r` flag if your book spines are sideways
2. Ensure good lighting and contrast in your photos
3. Make sure the book spines are clearly visible and not obscured
4. Try taking photos of smaller sections of your bookshelf if detection is poor
