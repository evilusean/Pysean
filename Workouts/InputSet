# Importing required modules
import csv
from datetime import datetime
  
# function to write in csv file
def write_in_csv(rows):
  
    # Opening the CSV file in read and
    # write mode using the open() module
    with open(r'/Users/teams/Desktop/Workouts/Workout.csv', 'a', newline='') as file:
  
        # creating the csv writer
        file_write = csv.writer(file)
  
        # Iterating over all the data in the rows 
        # variable
        for val in rows:
            
            # writing the data in csv file
            file_write.writerow(val)
  
  
# list to store the values of the rows
rows = []
  
# while loop to take inputs from the user
run = ''
while run != 'no':
  
    # lists to store the user data
    val = []
  
    # Taking inputs from the user
    val1 = input("Enter Exercise: ")
    val2 = input("Enter Reps: ")
  
    # storing current date and time
    current_date_time = datetime.now()
  
    # Appending the inputs in a list
    val.append(current_date_time)
    val.append(val1)
    val.append(val2)
  
    # Taking input to add one more row
    # If user enters 'no' then the will loop will break
    run = input("Do you want to add one more row? Type Yes or No:- ")
    run = run.lower()
  
    # Adding the stored data in rows list
    rows.append(val)
  
# Calling function to write in csv file
write_in_csv(rows)
