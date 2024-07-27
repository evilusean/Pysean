import piper
#work in progress, need to get 1,000's of lines, if I could use a wrapper that would be easier and just wrap the text in 'slovak("text")' and default in English
#If I use it like this, that will be 1,000's of variables 'english_text1, 2, 3...' 'slovak_text1, 2, 3...' but it should in theory work, and save it as one big '.wav' file
#going to see if there is an easier way to do this, instead of manually translating 1,000 + lines of slovak and creating a new variable for each line x2
#https://github.com/rhasspy/piper
#I could just create a bunch of files, one set in english, 
#one set in slovak(use it for anki, add an incrementing number automatically update title to the input name,
#   have it automatically save the file as '.mp3' (does '.wav' work?),
#save to a CSV with a link to .mp3 and english translation, and then combine them all into one file using ffmpeg or something, 
#   and add each incremented filename to a big file + english translations - need to think

# Define the text in both languages
english_text = "Hello, world!"
slovak_text = "Dobrý deň!"

# Specify the voices for each language
english_voice = "en_US-lessac-medium"
slovak_voice = "sk_SK-lili-medium" 

# Create a list of tuples containing the text and voice for each language
language_data = [
    (english_text, english_voice),
    (slovak_text, slovak_voice)
]

# Define the output file
output_file = "multi_language.wav"

# Synthesize speech for each language and concatenate the audio
with open(output_file, "wb") as outfile:
    for text, voice in language_data:
        audio_data = piper.synthesize(text, voice)
        outfile.write(audio_data)

print(f"Speech synthesized and saved to {output_file}")
