import csv
from googletrans import Translator
import time
import random

#trying to create a way to translate all the lines of slovak using google translate API,
#not working, google is pretty gud at stopping API's/webscraping/etc - might need to go line by line 
#and do a manual english translation... for 1,000's of lines, that's a multi day commitment

# Define the input and output CSV file paths
input_csv_file = "/media/sean/MusIX/Piper/TransLaSean/slovak10.csv"  # Replace with your input CSV file path
output_csv_file = "/media/sean/MusIX/Piper/TransLaSean/slovak10-out.csv"  # Replace with your output CSV file path

# Initialize the Google Translate API
translator = Translator()

# Rate limiting parameters
requests_per_minute = 10  # Adjust this based on Google Translate's rate limits
time_between_requests = 60 / requests_per_minute  # Seconds between requests

# Process the input CSV file
with open(input_csv_file, 'r', encoding='utf-8') as csvfile, open(output_csv_file, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.reader(csvfile)
    writer = csv.writer(outfile)

    # Write the header row (optional)
    writer.writerow(["English", "Slovak"])

    # Skip the header row (if any)
    next(reader)

    for i, row in enumerate(reader):
        slovak_text = row[1].strip()

        # Rate limiting
        time.sleep(random.uniform(time_between_requests * 0.8, time_between_requests * 1.2))  # Introduce random jitter

        try:
            # Translate the Slovak text to English
            english_text = translator.translate(slovak_text, dest='en').text
        except AttributeError as e:
            print(f"Translation failed for: {slovak_text} - Error: {e}")
            english_text = slovak_text  # Or handle the error differently
        except Exception as e:  # Catch other potential errors
            print(f"General error during translation: {e}")
            english_text = slovak_text  # Or handle the error differently

        # Write the translated English and original Slovak to the output CSV
        writer.writerow([english_text, slovak_text])

print("Translation complete!")

#Consider using a different translation service like DeepL (https://www.deepl.com/en/translator) or
#  Microsoft Translator (https://www.microsoft.com/en-us/translator). 
# These services often have more generous rate limits and might handle translations more reliably.