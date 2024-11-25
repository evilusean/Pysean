def convert_to_csv_format(input_string, old_symbol='=', new_symbol=',', comma_replacement='.'):
    # Replace existing commas with periods
    input_string = input_string.replace(',', comma_replacement)
    
    # Split the input string into lines
    lines = input_string.splitlines()
    
    # Replace the old symbol with the new symbol in each line
    converted_lines = [line.replace(old_symbol, new_symbol) for line in lines]
    
    # Join the converted lines back into a single string
    output_string = '\n'.join(converted_lines)
    
    return output_string

# Example input string (you can replace this with your actual long string)
input_string = """- Kto ste (vy)? = Who are you (you)?
- Odkiaľ ste? = where are you from
- Ako sa máte? = how are you
- Ako sa voláte = what is your name
- Zbohom. = Goodbye
- Dovidenia./Dovi. = Goodbye
"""

# Specify the symbols for replacement
old_symbol = '='
new_symbol = ','
comma_replacement = '.' 

# Convert the input string to CSV format
csv_output = convert_to_csv_format(input_string, old_symbol, new_symbol, comma_replacement)

# Print the output
print(csv_output)