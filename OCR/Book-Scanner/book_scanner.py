import cv2
import pytesseract
import numpy as np
import pandas as pd
from datetime import datetime
import os

class BookScanner:
    def __init__(self):
        # Initialize the camera
        self.camera = cv2.VideoCapture(0)
        # Set camera resolution
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        
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

    def capture_and_process(self):
        print("Press SPACE to capture an image, ESC to quit")
        
        books_data = []
        
        while True:
            ret, frame = self.camera.read()
            if not ret:
                print("Failed to grab frame")
                break
                
            # Display the frame
            cv2.imshow('Book Scanner', frame)
            
            key = cv2.waitKey(1)
            if key == 27:  # ESC key
                break
            elif key == 32:  # SPACE key
                # Extract text from the captured frame
                text = self.extract_text(frame)
                title, author = self.process_text(text)
                
                if title:
                    books_data.append({
                        'Title': title,
                        'Author': author,
                        'Date_Scanned': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    print(f"Captured: {title} by {author}")
                else:
                    print("No text detected. Try adjusting the camera position.")

        # Save to CSV
        if books_data:
            df = pd.DataFrame(books_data)
            filename = f'books_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            df.to_csv(filename, index=False)
            print(f"\nSaved {len(books_data)} books to {filename}")
        
        # Cleanup
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    scanner = BookScanner()
    scanner.capture_and_process() 