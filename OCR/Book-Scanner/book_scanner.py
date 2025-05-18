import cv2
import pytesseract
import numpy as np
import pandas as pd
from datetime import datetime
import os
import glob

class BookScanner:
    def __init__(self):
        pass
        
    def preprocess_image(self, image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Apply thresholding to get better text
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # Apply dilation to connect text components
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        return dilated

    def detect_book_spines(self, image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours based on aspect ratio and size
        book_spines = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = h / w if w > 0 else 0
            
            # Book spines are typically tall and narrow
            if aspect_ratio > 2 and h > image.shape[0] * 0.3:  # Adjust these thresholds as needed
                book_spines.append((x, y, w, h))
        
        # Sort book spines from left to right
        book_spines.sort(key=lambda x: x[0])
        
        return book_spines

    def extract_text(self, image):
        # Preprocess the image
        processed_image = self.preprocess_image(image)
        # Extract text using Tesseract with custom configuration
        custom_config = r'--oem 3 --psm 6'  # Assume uniform text block
        text = pytesseract.image_to_string(processed_image, config=custom_config)
        return text

    def process_text(self, text):
        # Split text into lines and clean up
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return None
            
        # Try to identify title and author
        # Look for common author indicators
        author_indicators = ['by', 'BY', 'By', '-', '–', '—']
        
        # Combine all lines into one string
        full_text = ' '.join(lines)
        
        # Try to split on author indicators
        for indicator in author_indicators:
            if indicator in full_text:
                parts = full_text.split(indicator, 1)
                if len(parts) == 2:
                    title = parts[0].strip()
                    author = parts[1].strip()
                    return f"{title} - {author}"
        
        # If no author indicator found, use first line as title and second as author
        if len(lines) >= 2:
            return f"{lines[0]} - {lines[1]}"
        else:
            return lines[0]

    def process_image(self, image_path):
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to read image: {image_path}")
            return []
            
        # Detect book spines
        book_spines = self.detect_book_spines(image)
        
        if not book_spines:
            print(f"No book spines detected in {image_path}")
            return []
            
        print(f"Found {len(book_spines)} potential book spines")
        books = []
        
        # Process each book spine
        for i, (x, y, w, h) in enumerate(book_spines):
            # Extract the book spine region
            book_region = image[y:y+h, x:x+w]
            
            # Extract text from the book spine
            text = self.extract_text(book_region)
            result = self.process_text(text)
            
            if result:
                books.append(result)
                print(f"Processed book {i+1}: {result}")
            
        return books

    def process_directory(self, directory_path):
        # Get all image files in the directory
        image_extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp')
        image_files = []
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(directory_path, ext)))
        
        if not image_files:
            print(f"No image files found in {directory_path}")
            return
        
        print(f"Found {len(image_files)} images to process")
        all_books = []
        
        # Process each image
        for image_path in image_files:
            print(f"\nProcessing: {image_path}")
            books = self.process_image(image_path)
            all_books.extend(books)

        # Save to text file
        if all_books:
            filename = f'books_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                for book in all_books:
                    f.write(f"{book}\n")
            print(f"\nSaved {len(all_books)} books to {filename}")
        else:
            print("\nNo books were successfully processed")

if __name__ == "__main__":
    scanner = BookScanner()
    
    # Get the directory path from user input
    directory_path = input("Enter the directory path containing book images: ").strip()
    
    # Remove quotes if present
    directory_path = directory_path.strip('"').strip("'")
    
    if os.path.isdir(directory_path):
        scanner.process_directory(directory_path)
    else:
        print(f"Invalid directory path: {directory_path}") 