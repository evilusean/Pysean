### Steps to Setup and Run epub_to_audiobook on Arch Linux

#### 1. Install the Package from AUR
First, install the `epub_to_audiobook` wrapper and package using your preferred AUR helper (such as `yay`):
'yay -S epub_to_audiobook'
2. Create and Activate a Python Virtual Environment
Since system Python environments or strict wrapper environments can restrict package installations or lack visibility into --user spaces, set up a dedicated virtual environment:

Bash
python -m venv ~/venv
source ~/venv/bin/activate
3. Install All Required Python Dependencies via Pip
Because the AUR package environment requires specific parsing, audio manipulation, and TTS modules that may not be pulled in automatically depending on your Python version, install the full suite of correct packages directly:

Bash
'pip install ebooklib edge-tts beautifulsoup4 pydub mutagen audioop-lts sentencex'
4. Run the Conversion Command
With the virtual environment active and all dependencies satisfied, execute the conversion tool pointing to your EPUB file, output folder, and desired chapter range:

Bash
epub_to_audiobook "/home/archsean/Downloads/Books/Tesla Inventor of the Electrical Age (W. Bernard Carlson) (z-library.sk, 1lib.sk, z-lib.sk).epub" "/home/archsean/Downloads/Audiobooks" --tts edge
