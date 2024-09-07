import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import csv

#TODO:
#Add CSV with keybindings
#Make Image box Larger
#default image folder wasn't working, need to fix - still asks on startup


# Set the path to your CSV file containing key mappings
key_mapping_file = "/home/ArchSean/Downloads/Unsorted/MeMeLocaSeans.csv"  # Replace with the actual path if needed

# Set the folder containing the images to sort
image_folder = "/home/ArchSean/Downloads/Unsorted"  # Replace with the actual path

# Load key mappings from the CSV file
key_mapping = {}
try:
    with open(key_mapping_file, 'r') as f:
        reader = csv.reader(f)
        key_mapping = {row[0].lower(): row[1] for row in reader}
except FileNotFoundError:
    print(f"Error: Key mapping file not found: {key_mapping_file}")

# Get the first image from the folder (you'll likely loop through all images later)
image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
current_image = os.path.join(image_folder, image_files[0]) if image_files else None


class MemeSorter:
    def __init__(self, master):
        self.master = master
        master.title("TeMeMeSorter")

        # Variables
        self.image_folder = ""
        self.key_mapping = {}
        self.current_image = None
        self.sorted_folder = ""

        # GUI elements
        self.folder_label = tk.Label(master, text="Image Folder:")
        self.folder_label.grid(row=0, column=0)

        self.folder_button = tk.Button(master, text="Select Folder", command=self.select_folder)
        self.folder_button.grid(row=0, column=1)

        self.mapping_label = tk.Label(master, text="Key Mapping:")
        self.mapping_label.grid(row=1, column=0)

        self.mapping_text = tk.Text(master, height=10, width=50)
        self.mapping_text.grid(row=2, column=0, columnspan=2)

        self.image_label = tk.Label(master, text="No image loaded")
        self.image_label.grid(row=3, column=0, columnspan=2)

        self.next_button = tk.Button(master, text="Next/Skip", command=self.next_image, state=tk.DISABLED)
        self.next_button.grid(row=4, column=0)

        self.undo_button = tk.Button(master, text="Undo", command=self.undo_move, state=tk.DISABLED)
        self.undo_button.grid(row=4, column=1)

        # Key bindings
        master.bind("<Key>", self.sort_image)

        self.sort_gifs_button = tk.Button(master, text="Sort GIFs", command=self.sort_all_gifs)
        self.sort_gifs_button.grid(row=5, column=0, columnspan=2)

        # Display key bindings below the image
        self.key_bindings_label = tk.Label(master, text="")
        self.key_bindings_label.grid(row=6, column=0, columnspan=2)
        self.update_key_bindings_display()

        # Store last moved image info for undo
        self.last_moved_image = None
        self.last_moved_from = None

    def select_folder(self):
        """Prompts the user to select an image folder and loads key mappings."""
        self.image_folder = filedialog.askdirectory()
        if self.image_folder:
            self.folder_label.config(text=f"Image Folder: {self.image_folder}")
            self.load_key_mapping()
            self.create_sorted_folder()
            self.load_next_image()

    def load_key_mapping(self):
        """Loads key mappings from a CSV file named 'key_mapping.csv' in the image folder."""
        mapping_file = os.path.join(self.image_folder, "key_mapping.csv")
        try:
            with open(mapping_file, 'r') as f:
                reader = csv.reader(f)
                self.key_mapping = {row[0].lower(): row[1] for row in reader}
            self.mapping_text.delete("1.0", tk.END)
            for key, folder in self.key_mapping.items():
                self.mapping_text.insert(tk.END, f"{key}: {folder}\n")
        except FileNotFoundError:
            messagebox.showerror("Error", f"Key mapping file not found: {mapping_file}")

    def create_sorted_folder(self):
        """Creates a 'Sorted' folder within the image folder."""
        self.sorted_folder = os.path.join(self.image_folder, "Sorted")
        os.makedirs(self.sorted_folder, exist_ok=True)

    def load_next_image(self):
        """Loads the next image from the image folder."""
        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                self.current_image = os.path.join(self.image_folder, filename)
                self.image_label.config(text=f"Current Image: {filename}")
                self.next_button.config(state=tk.NORMAL)
                return
        self.image_label.config(text="No more images to sort!")
        self.next_button.config(state=tk.DISABLED)

    def sort_image(self, event):
        """Moves the current image to the folder associated with the pressed key."""
        key = event.keysym.lower()
        if key in self.key_mapping:
            destination_folder = os.path.join(self.sorted_folder, self.key_mapping[key])
            os.makedirs(destination_folder, exist_ok=True)
            try:
                # Move the image (not delete)
                shutil.move(self.current_image, destination_folder)

                # Store info for undo
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
                self.load_next_image()  # Reload to show the image back
            except Exception as e:
                messagebox.showerror("Error", f"Failed to undo move: {e}")

    def sort_all_gifs(self):
        """Moves all GIF images to the specified 'GIFs' folder."""
        gifs_folder = "/mnt/sdb3/MEmes/GIFs"  # Set your desired GIF folder path here
        os.makedirs(gifs_folder, exist_ok=True)

        for filename in os.listdir(self.image_folder):
            if filename.lower().endswith('.gif'):
                source_path = os.path.join(self.image_folder, filename)
                dest_path = os.path.join(gifs_folder, filename)
                try:
                    shutil.move(source_path, dest_path)
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to move GIF: {e}")
        self.load_next_image()  # Refresh the image display

    def update_key_bindings_display(self):
        """Updates the label to display key bindings."""
        bindings_text = "\n".join([f"{key}: {folder}" for key, folder in self.key_mapping.items()])
        self.key_bindings_label.config(text=bindings_text)

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