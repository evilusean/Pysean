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
input_string = """Ako sa voláš? = What's your name?
Volám sa Kristína. Teší ma. = My name is Kristina. It makes me happy(to meet you)
Si študentka? = Are you a student?
Odkiaľ si, Kristína? = Where are you from, Kristina?
Ja som zo Slovenska, z Bratislavy. Kde bývaš? V ktorom meste? = I am from Slovakia, from Bratislava. Where do you live? In which city?
Bývam vo Vilniuse. =  live in Vilnius.
Akými jazykmi hovoríš? = What languages ​​do you speak?
Hovorím po litovsky, po anglicky a trochu po slovensky. = I speak Lithuanian, English and a little Slovak
Koľko máš rokov? Ja mám dvadsať (20) rokov. A ty? =  How old are you? I am twenty (20) years old. And you?"""

# Specify the symbols for replacement
old_symbol = '='
new_symbol = ','
comma_replacement = '.' 

# Convert the input string to CSV format
csv_output = convert_to_csv_format(input_string, old_symbol, new_symbol, comma_replacement)

# Print the output
print(csv_output)