# probably one of the most convenient scripts, just take a screenshot and get the OCR of all the text
# bindd = Super+Shift, T, Character recognition,exec,grim -g "$(slurp $SLURP_ARGS)" "tmp.png" && tesseract "tmp.png" - | wl-copy && rm "tmp.png" # OCR to clipboard

# Script for OCR capture and clipboard copy

# Capture selected screen area to a temp file, run Tesseract OCR, copy to clipboard, and delete the temp file.
grim -g "$(slurp)" "tmp.png" && \
tesseract "tmp.png" - | wl-copy && \
rm "tmp.png"
