import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import csv
from PIL import Image, ImageTk

#TODO:
#Image still isn't being displayed, added in a bunch of code, still not working
#Changed permissions for 'Unsorted' Folder, still won't show images
#Remove the top row of csv 
#will just move the unsorted folder to memes folder/external HD - future sean problem

# Set the path to your CSV file containing key mappings
key_mapping_file = "/home/ArchSean/Downloads/Unsorted/MeMeLocaSeans.csv"

# Set the folder containing the images to sort
default_image_folder = "/home/ArchSean/Downloads/Unsorted"

# Load key mappings from the CSV file
key_mapping = {}
try:
    with open(key_mapping_file, 'r') as f:
        reader = csv.reader(f)
        key_mapping = {row[0].lower(): row[1] for row in reader}
except FileNotFoundError:
    print(f"Error: Key mapping file not found: {key_mapping_file}")


class MemeSorter:
    def __init__(self, master):
        self.master = master
        master.title("TeMeMeSorter")

        # Variables
        self.image_folder = default_image_folder
        self.key_mapping = key_mapping
        self.current_image = None  # Store the current image path
        self.photo = None  # Initialize self.photo here

        # GUI elements
        self.folder_label = tk.Label(master, text="Image Folder:")
        self.folder_label.grid(row=0, column=0)

        self.folder_label.config(text=f"Image Folder: {self.image_folder}")

        self.folder_button = tk.Button(master, text="Select Folder", command=self.select_folder)
        self.folder_button.grid(row=0, column=1)

        self.mapping_label = tk.Label(master, text="Key Mapping:")
        self.mapping_label.grid(row=1, column=0)

        self.mapping_text = tk.Text(master, height=10, width=50)
        self.mapping_text.grid(row=1, column=1)

        # Create a canvas for image display
        self.image_canvas = tk.Canvas(master, width=500, height=500)  # Adjust size as needed
        self.image_canvas.grid(row=2, column=0, columnspan=2)

        self.image_label = tk.Label(master, text="No image loaded")
        self.image_label.grid(row=3, column=0, columnspan=2)

        # Display key bindings below the image
        self.key_bindings_label = tk.Label(master, text="")
        self.key_bindings_label.grid(row=4, column=0, columnspan=2)
        self.update_key_bindings_display()

        self.next_button = tk.Button(master, text="Next/Skip", command=self.next_image, state=tk.DISABLED)
        self.next_button.grid(row=5, column=0)

        self.undo_button = tk.Button(master, text="Undo", command=self.undo_move, state=tk.DISABLED)
        self.undo_button.grid(row=5, column=1)

        self.sort_gifs_button = tk.Button(master, text="Sort GIFs", command=self.sort_all_gifs)
        self.sort_gifs_button.grid(row=6, column=0, columnspan=2)

        # Store last moved image info for undo
        self.last_moved_image = None
        self.last_moved_from = None

        self.create_sorted_folder()
        self.load_next_image()

    def select_folder(self):
        """Prompts the user to select an image folder and loads key mappings."""
        self.image_folder = filedialog.askdirectory()
        if self.image_folder:
            self.folder_label.config(text=f"Image Folder: {self.image_folder}")
            self.load_key_mapping()  # Reload mappings if a new folder is selected
            self.create_sorted_folder()
            self.load_next_image()

    def load_key_mapping(self):
        """Loads key mappings from a CSV file named 'key_mapping.csv' in the image folder."""
        mapping_file = os.path.join(self.image_folder, "key_mapping.csv")
        try:
            with open(mapping_file, 'r') as f:
                reader = csv.reader(f)
                self.key_mapping = {row[0].lower(): row[1] for row in reader}
            self.update_key_bindings_display()  # Update display after loading
        except FileNotFoundError:
            messagebox.showerror("Error", f"Key mapping file not found: {mapping_file}")

    def create_sorted_folder(self):
        """Creates a 'Sorted' folder within the image folder."""
        self.sorted_folder = os.path.join(self.image_folder, "Sorted")
        os.makedirs(self.sorted_folder, exist_ok=True)

    def load_next_image(self):
        """Loads the next image from the image folder and displays it."""
        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                self.current_image = os.path.join(self.image_folder, filename)
                self.image_label.config(text=f"Current Image: {filename}")
                self.next_button.config(state=tk.NORMAL)

                # Load and display the image
                self.display_image(self.current_image)
                return

        self.image_label.config(text="No more images to sort!")
        self.next_button.config(state=tk.DISABLED)
        self.image_canvas.delete("all")  # Clear the canvas if no images

    def display_image(self, image_path):
        """Displays the image on the canvas."""
        try:
            img = Image.open(image_path)

            # Update the canvas size based on the image BEFORE resizing
            self.image_canvas.config(width=img.width, height=img.height)

            # Resize the image to fit the canvas while preserving aspect ratio
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()
            img.thumbnail((canvas_width, canvas_height))

            # Assign the PhotoImage to the instance variable
            self.photo = ImageTk.PhotoImage(img)

            self.image_canvas.create_image(canvas_width // 2, canvas_height // 2, anchor=tk.CENTER, image=self.photo)
        except Exception as e:
            print(f"Error loading image: {e}")

    def sort_image(self, event):
        """Moves the current image to the folder associated with the pressed key."""
        if self.current_image:  # Only sort if an image is loaded
            key = event.keysym.lower()
            if key in self.key_mapping:
                destination_folder = os.path.join(self.sorted_folder, self.key_mapping[key])
                os.makedirs(destination_folder, exist_ok=True)
                try:
                    shutil.move(self.current_image, destination_folder)

                    self.last_moved_image = os.path.join(destination_folder, os.path.basename(self.current_image))
                    self.last_moved_from = self.image_folder

                    self.undo_button.config(state=tk.NORMAL)
                    self.load_next_image()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to move file: {e}")

    def next_image(self):
        """Skips the current image and loads the next one."""
        self.load_next_image()

    def undo_move(self):
        """Moves the last sorted image back to the original folder."""
        if self.last_moved_image and self.last_moved_from:
            try:
                shutil.move(self.last_moved_image, self.last_moved_from)
                self.last_moved_image = None
                self.last_moved_from = None
                self.undo_button.config(state=tk.DISABLED)
                self.load_next_image()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to undo move: {e}")

    def sort_all_gifs(self):
        """Moves all GIF images to the specified 'GIFs' folder."""
        gifs_folder = "/mnt/sdb3/MEmes/GIFs"
        os.makedirs(gifs_folder, exist_ok=True)

        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith('.gif'):
                source_path = os.path.join(self.image_folder, filename)
                dest_path = os.path.join(gifs_folder, filename)
                try:
                    shutil.move(source_path, dest_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to move GIF: {e}")
        self.load_next_image()

    def update_key_bindings_display(self):
        """Updates the label to display key bindings."""
        bindings_text = "\n".join([f"{key}: {folder}" for key, folder in self.key_mapping.items()])
        self.key_bindings_label.config(text=bindings_text)
        self.mapping_text.delete("1.0", tk.END)  # Clear existing content
        self.mapping_text.insert(tk.END, bindings_text)  # Insert updated bindings


root = tk.Tk()
app = MemeSorter(root)
root.mainloop()






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
#GUI libraries like Tkinter (built-in), PyQt (very powerful), and Kivy (good for touch interfaces). 
#   #These libraries provide ready-made components for image display, buttons, and handling user input.
#if feeling ambitious, add a gif sort function that auto takes all gifs to 'gifs' folder
#if feeling very ambitious, create a hashing algo that checks for dups(I know there is a ton) - future sean problem
#future future sean problem : create a hotkey for saving an image 2 actions/clicks instead of 4 - EfficienSean = 
#instead of click tab -> right click -> save image as -> save Vs click tab -> press button (save into unsorted folder)
#Maybe use GoLang? - Next Language, then AWS - Finish A2/B1 Slovak - Create Anki Decks - Then Go - Then Apply
#   # Then I can start applying for devops/web developer/data analyst/astronaut/doctor/scientist+pastor/pilot
#Maybe build in Go? - I need a GUI for images - speed doesn't really matter, one at a time Vs concuritSean