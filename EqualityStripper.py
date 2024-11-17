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
input_string = """auto= car
dedko= grandfather
dieťa= child
dom= house
doma= at home
futbalista= footballer
kniha= book
kosť= bone
kvet= flower
lekáreň= chemist
mačka= cat
múzeum= museum
muž= man
námestie= square
pes= dog
posteľ= bed
ruža= rose
srdce= heart
šteňa= puppy
žena= woman

vysoký= high
nízky= low
veľký= large, great
malý= small
pekný= nice
krásny= beautiful
dobrý= good
nový= new
starý= old
moderný= modern
červený= red
zelený= green
čierny= black
biely= white
modrý= blue
žltý= yellow

kto= who
čo= what
aký, aká, aké= what, which
ten, tá, to= that, the, the one that
tento, táto, toto= this
nejaký, nejaká, nejaké= a, an, some, any
je= is
veľmi= very
tam= there, in that place
tu= here
a= and
alebo= or"""

# Specify the symbols for replacement
old_symbol = '='
new_symbol = ','
comma_replacement = '.' 

# Convert the input string to CSV format
csv_output = convert_to_csv_format(input_string, old_symbol, new_symbol)

# Print the output
print(csv_output)