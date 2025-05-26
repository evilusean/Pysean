import sqlite3
import zipfile
import os
import json

def extract_anki_db(apkg_path, start_range=None, end_range=None):
    # Create a temporary directory
    temp_dir = "temp_anki"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Extract the apkg (zip) file
    with zipfile.ZipFile(apkg_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # Connect to the extracted database
    conn = sqlite3.connect(os.path.join(temp_dir, "collection.anki2"))
    cursor = conn.cursor()
    
    # Query to get note data with sort_id
    cursor.execute("SELECT id, flds FROM notes ORDER BY id")
    rows = cursor.fetchall()
    
    # Process the results
    kanji_data = []
    for row in rows:
        sort_id = row[0]
        
        # Check if the sort_id is within the specified range
        if start_range is not None and sort_id < start_range:
            continue
        if end_range is not None and sort_id > end_range:
            continue
            
        # Split fields (they're separated by \x1f character)
        fields = row[1].split('\x1f')
        if len(fields) >= 4:  # Check if we have at least 4 fields
            kanji = fields[0].strip()
            meaning = fields[2].strip()
            context_sentences = fields[3].strip() if len(fields) > 3 else ""
            context_patterns = fields[4].strip() if len(fields) > 4 else ""
            
            # Get readings if they exist
            reading = fields[1].strip() if len(fields) > 1 else ""
            onyomi = fields[5].strip() if len(fields) > 5 else ""
            kunyomi = fields[6].strip() if len(fields) > 6 else ""
            nanori = fields[7].strip() if len(fields) > 7 else ""
            
            # Format the output
            output = f"{sort_id} / {kanji} / {meaning}"
            if reading:
                output += f" / {reading}"
            if onyomi:
                output += f"\nReading_Onyomi: {onyomi}"
            if kunyomi:
                output += f"\nReading_Kunyomi: {kunyomi}"
            if nanori:
                output += f"\nReading_Nanori: {nanori}"
            output += "\n"
            
            # Add context patterns if they exist
            if context_patterns:
                pattern_groups = context_patterns.split(';')
                for group in pattern_groups:
                    if group.strip():
                        output += f"{group.strip()}\n"
            
            # Add context sentences if they exist
            if context_sentences:
                # Split sentences by newline and format each pair
                sentence_pairs = context_sentences.split('\n')
                for pair in sentence_pairs:
                    if '|' in pair:
                        eng, jpn = pair.split('|')
                        output += f"{eng.strip()}|{jpn.strip()}\n"
            
            kanji_data.append({
                'sort_id': sort_id,
                'kanji': kanji,
                'meaning': meaning,
                'reading': reading,
                'onyomi': onyomi,
                'kunyomi': kunyomi,
                'nanori': nanori,
                'context_patterns': context_patterns,
                'context_sentences': context_sentences,
                'formatted_output': output
            })
    
    # Clean up
    conn.close()
    
    # Save formatted output to a text file
    filename = f'kanji_formatted_{start_range}-{end_range}.txt' if start_range and end_range else 'kanji_formatted_all.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        for item in kanji_data:
            f.write(item['formatted_output'] + '\n\n')
    
    # Clean up temporary directory
    import shutil
    shutil.rmtree(temp_dir)
    
    return kanji_data

def main():
    # Hardcoded path to the .apkg file
    apkg_file = "/home/ArchSean/Downloads/books/Wanikani_Ultimate_3_Tokyo_Drift.apkg"
    
    
    # Get the range
    range_input = input("Enter the range (e.g., '1-100' or press Enter for all): ")
    
    start_range = None
    end_range = None
    
    if range_input:
        try:
            start_range, end_range = map(int, range_input.split('-'))
        except ValueError:
            print("Invalid range format. Please use format 'start-end' (e.g., '1-100')")
            return
    
    # Extract and format the data
    result = extract_anki_db(apkg_file, start_range, end_range)
    print(f"Extracted {len(result)} kanji entries")

if __name__ == "__main__":
    main()