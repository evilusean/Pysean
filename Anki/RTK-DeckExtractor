import sqlite3
import zipfile
import os
import json

'''
Created a script to pull out all the data I will need to make Kanji Drop 
from the Remembering the Kanji Anki deck. - Heisig's RTK 6th Edition, Found at :
Remembering_the_Kanji_1_6th_Edition_2200_Kanji.apkg
https://ankiweb.net/shared/info/1654787298
Since '.apkg' files are similar to SQLite databases,
 I will extract the data from the database and save it to a JSON file.
I want future Sean to create another game that flashes the kanji on the screen briefly
 and then shows the answer after a brief delay, should be easy enough, and useful
 you should be able to select a range, 2200 kanji, learn 100-200, or 0-2200 for all,
 so if you want to learn 20 kanji a day, simply add your range of 1-20, 21-40, etc, etc, 
 and then to review all just add them all together like 1-200, for 10 days of review
 just set the range, play the game in the background, every time your consciousness glances over,
 try to remember what each kanji means, 20 a day seems pretty reasonable, stop when you know all the drops
Since there are no readings (multiple onyomi/kunyomi/etc/etc for each kanji) -  it is just the kanji and it's meaning, which is way easier to infer

Future Future Sean Problems : WaniKani has an API, you could use that to do whatever a user has learned on their platform
'''

def extract_anki_db(apkg_path):
    # Create a temporary directory
    temp_dir = "temp_anki"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Extract the apkg (zip) file
    with zipfile.ZipFile(apkg_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
    
    # Connect to the extracted database
    conn = sqlite3.connect(os.path.join(temp_dir, "collection.anki2"))
    cursor = conn.cursor()
    
    # Query to get note data
    cursor.execute("SELECT flds FROM notes")
    rows = cursor.fetchall()
    
    # Process the results
    kanji_meanings = []
    for index, row in enumerate(rows, 1):  # Start enumeration from 1
        # Split fields (they're separated by \x1f character)
        fields = row[0].split('\x1f')
        if len(fields) >= 3:  # Check if we have at least 3 fields
            kanji = fields[0].strip()
            meaning = fields[2].strip()  # Get the third field instead of second
            kanji_meanings.append({
                'index': index,
                'kanji': kanji,
                'meaning': meaning
            })
    
    # Clean up
    conn.close()
    
    # Save to a file
    with open('kanji_meanings.json', 'w', encoding='utf-8') as f:
        json.dump(kanji_meanings, f, ensure_ascii=False, indent=2)
    
    # Clean up temporary directory
    import shutil
    shutil.rmtree(temp_dir)
    
    return kanji_meanings

# Usage
apkg_file = "/home/ArchSean/Downloads/RTK/Remembering_the_Kanji_1_6th_Edition_2200_Kanji.apkg"
result = extract_anki_db(apkg_file)
print(f"Extracted {len(result)} kanji-meaning pairs")
