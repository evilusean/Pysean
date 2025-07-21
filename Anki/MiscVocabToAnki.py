# TO DO : Create a script that creates anki decks/cards from my vocab lists - formats the first line of the kanji to be large and easily readable, 
# since anki uses html for formatting, this should be as easy as using inline CSS, or setting the card format beforehand,
# so the 'Kanji', 'Hiragana', and 'Romaji' on the front, 
# and puts the English meaning/definition text after the last '=' equals sign on the back of the cards
# some cards are missing the '=' inbetween the kanji=hiragana=romaji, so either I can get AI to reformat cards, 
# or make the script only check for the last '=' sign and put everything before it on the front and everything after it on the back
# also remember I added some lines that have 'Example = .....' that will need to be fixed
# my first set of misc vocab is almost at 1000 lines, I do NOT want to type that out manually creating each new anki card

# Script to convert cleaned vocab list to Anki deck (CSV for import)
# Front: Everything before the final '=' (large text)
# Back: Everything after the final '=' (English meaning)
import csv

INPUT_FILE = 'cleaned_misc_vocab.txt'
OUTPUT_FILE = 'N4Vocab700-Kanji170.csv'

# Helper to format front of card (all non-English fields, large)
def format_front(line):
    # Split by last '='
    if '=' not in line:
        return f"<div style='font-size:2.5em;'>{line.strip()}</div>"
    front, _ = line.rsplit('=', 1)
    return f"<div style='font-size:2.5em;'>{front.strip()}</div>"

# Helper to format back of card (English meaning)
def format_back(line):
    if '=' not in line:
        return ''
    _, back = line.rsplit('=', 1)
    return back.strip()


def main():
    with open(INPUT_FILE, 'r', encoding='utf-8') as infile, open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['Front', 'Back'])
        for line in infile:
            line = line.strip()
            if not line:
                continue
            front = format_front(line).replace(',', '.')
            back = format_back(line).replace(',', '.')
            writer.writerow([front, back])

if __name__ == '__main__':
    main()
