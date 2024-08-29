#create a python script for sorting memes from one folder into many folders(25) 
#and I can press a key to send it to the folder, I will also need on the GUI a display of the key to press with 
#a folder location - the folders already exist, I need to transfer into them, 
#the folders all have unique names that are different, add custom mapping to keys and folders and 
#then display the key mapping in the gui below where the image will be displayed
#create a custom csv with key mappings and folder locations, use that for input
#take the custom mapping and display it in the GUI
#then take the images one by one to display in the GUI, take the mapping and then sort to correct folder
#afer being sorted, delete the old image from the unsorted folder and move the new image to correct folder
#add an undo button, I will inevitably press the wrong key
#'Next/Skip' Button
#add a sorted folder, and just delete that after done, that way if I do mess up, just sort by most recent
# or move it to a cache? seems easier to just switch it to a new folder, if I ctrl+z, put it back 
# and then move the original to the sorted folder, and one to the correct directory
# almost all images will have a unqiue name, don't need to worry about clashing names
#still need to think of GUI options, almost all python I've built has been text input -> text output 
# use OS and what other package/library? what is the best GUI option for displaying images?
#if feeling ambitious, add a gif sort function that auto takes all gifs to 'gifs' folder
#if feeling very ambitious, create a hashing algo that checks for dups(I know there is a ton) - future sean problem
#future future sean problem : create a hotkey for saving an image 2 actions/clicks instead of 4 - EfficienSean = 
#instead of click tab -> right click -> save image as -> save Vs click tab -> press button (save into unsorted folder)