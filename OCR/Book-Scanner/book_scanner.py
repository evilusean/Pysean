import cv2
import pytesseract
import numpy as np
import pandas as pd
from datetime import datetime
import os
import glob
from PIL import Image
import re

class BookScanner:
    def __init__(self):
        # Configure Tesseract parameters
        self.custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,;:!?()[]{}-\'\" "'
        
    def preprocess_image(self, image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh)
        
        # Increase contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Combine the results
        final = cv2.bitwise_and(denoised, enhanced)
        
        return final

    def detect_rotation(self, image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Find lines
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
        
        if lines is not None:
            angles = []
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if x2 - x1 != 0:  # Avoid division by zero
                    angle = np.arctan((y2 - y1) / (x2 - x1)) * 180 / np.pi
                    angles.append(angle)
            
            if angles:
                # Use the most common angle
                angle = np.median(angles)
                return angle
        
        return 0

    def detect_book_spines(self, image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection with adjusted parameters
        edges = cv2.Canny(gray, 30, 200)
        
        # Dilate edges to connect components
        kernel = np.ones((3,3), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        
        # Find contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours based on aspect ratio and size
        book_spines = []
        min_height = image.shape[0] * 0.2  # Reduced minimum height
        max_width = image.shape[1] * 0.3   # Maximum width
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = h / w if w > 0 else 0
            
            # More lenient conditions for book spines
            if (aspect_ratio > 1.5 and  # Reduced aspect ratio requirement
                h > min_height and 
                w < max_width and
                w > 10 and  # Minimum width
                h > 50):    # Minimum height
                book_spines.append((x, y, w, h))
        
        # Sort book spines from left to right
        book_spines.sort(key=lambda x: x[0])
        
        return book_spines

    def clean_text(self, text):
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s.,;:!?()\[\]{}-\'\" ]', '', text)
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

    def extract_text(self, image):
        # Preprocess the image
        processed_image = self.preprocess_image(image)
        
        # Try different PSM modes
        psm_modes = [6, 4, 3]  # Try different page segmentation modes
        best_text = ""
        
        for psm in psm_modes:
            config = f'--oem 3 --psm {psm} {self.custom_config}'
            text = pytesseract.image_to_string(processed_image, config=config)
            text = self.clean_text(text)
            
            if len(text) > len(best_text):
                best_text = text
        
        return best_text

    def process_text(self, text):
        if not text:
            return None
            
        # Clean the text
        text = self.clean_text(text)
        
        # Try to identify title and author
        author_indicators = ['by', 'BY', 'By', '-', '–', '—']
        
        # Try to split on author indicators
        for indicator in author_indicators:
            if indicator in text:
                parts = text.split(indicator, 1)
                if len(parts) == 2:
                    title = parts[0].strip()
                    author = parts[1].strip()
                    if title and author:  # Only return if both parts are non-empty
                        return f"{title} - {author}"
        
        # If no author indicator found, try to split on the last comma or period
        for separator in [',', '.']:
            if separator in text:
                parts = text.rsplit(separator, 1)
                if len(parts) == 2:
                    title = parts[0].strip()
                    author = parts[1].strip()
                    if title and author:  # Only return if both parts are non-empty
                        return f"{title} - {author}"
        
        # If all else fails, return the cleaned text
        return text if len(text) > 3 else None

    def process_image(self, image_path):
        # Read the image
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to read image: {image_path}")
            return []
            
        # Detect and correct rotation
        angle = self.detect_rotation(image)
        if abs(angle) > 5:  # Only rotate if angle is significant
            height, width = image.shape[:2]
            center = (width // 2, height // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            image = cv2.warpAffine(image, rotation_matrix, (width, height))
            
        # Detect book spines
        book_spines = self.detect_book_spines(image)
        
        if not book_spines:
            print(f"No book spines detected in {image_path}")
            return []
            
        print(f"Found {len(book_spines)} potential book spines")
        books = []
        
        # Process each book spine
        for i, (x, y, w, h) in enumerate(book_spines):
            # Extract the book spine region with padding
            padding = 5
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(image.shape[1], x + w + padding)
            y2 = min(image.shape[0], y + h + padding)
            book_region = image[y1:y2, x1:x2]
            
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