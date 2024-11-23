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
input_string = """ja= I
ty= you (singular)
on= he
ona= she
ono= it
my= we
vy= you (plural)
oni= they (masculine or mixed)
ony= they (feminine)
byť= to be
bývať= to live
volať sa= to be called
mať= to have
hovoriť= to speak, to talk
mať sa= to fare, to be [doing]
čítať= to read
písať= to write
česať sa= to tease
piť= to drink
ísť= to go
robiť= to do
ahoj!, čau!= hello! Hi!
dobré ráno= good morning
dobrý deň= good afternoon, good day
dobrý večer= good evening
dovidenia!, dovi!= goodbye! bye!
dobrú noc= good night
zbohom= farewell
Teší ma.= Pleased to meet you.
Ako sa máš?= How are you?
ďakujem= thank you
po slovensky= in Slovak
po poľsky= in Polish
po nemecky= in German
po litovsky= in Lithuanian
po anglicky= in English
ako= how
odkiaľ= from where, whence
kde= where
koľko= how much
ktorý= which
devätnásť= nineteen
dvadsať= twenty
dvadsaťdva= twenty-two
dvadsaťtri= twenty-three
dvadsaťpäť= twenty-five
dobre= ok, fine, good
zle= badly, poorly, not well
tiež, aj= also, too
áno= yes
nie= no
ostatní= other
trochu= a little bit
na, v, vo= on, in, to
z, zo= of, from
teraz= now
potom= then"""

# Specify the symbols for replacement
old_symbol = '='
new_symbol = ','
comma_replacement = '.' 

# Convert the input string to CSV format
csv_output = convert_to_csv_format(input_string, old_symbol, new_symbol, comma_replacement)

# Print the output
print(csv_output)