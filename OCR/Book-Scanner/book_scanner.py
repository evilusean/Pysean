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

    def extract_text(self, image):
        # Preprocess the image
        processed_image = self.preprocess_image(image)
        # Extract text using Tesseract
        text = pytesseract.image_to_string(processed_image)
        return text

    def process_text(self, text):
        # Split text into lines and clean up
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Try to identify title and author
        # This is a simple heuristic - you might need to adjust based on your books
        title = lines[0] if lines else ""
        author = lines[1] if len(lines) > 1 else ""
        
        return title, author

    def process_image(self, image_path):
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to read image: {image_path}")
            return None
            
        # Extract text from the image
        text = self.extract_text(image)
        title, author = self.process_text(text)
        
        if title:
            return {
                'Title': title,
                'Author': author,
                'Image': os.path.basename(image_path),
                'Date_Scanned': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        return None

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
        books_data = []
        
        # Process each image
        for image_path in image_files:
            print(f"\nProcessing: {image_path}")
            result = self.process_image(image_path)
            if result:
                books_data.append(result)
                print(f"Captured: {result['Title']} by {result['Author']}")
            else:
                print("No text detected in this image")

        # Save to CSV
        if books_data:
            df = pd.DataFrame(books_data)
            filename = f'books_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            df.to_csv(filename, index=False)
            print(f"\nSaved {len(books_data)} books to {filename}")
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