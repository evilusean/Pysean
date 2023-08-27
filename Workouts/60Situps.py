#adds datetime situps 60 to Workout.csv
import csv
from datetime import datetime

def write_in_csv(rows):

    with open(r'/Users/teams/Desktop/Workouts/Workout.csv', 'a', newline='') as file:

        file_write = csv.writer(file)

        for val in rows:
            
            # writing the data in csv file
            file_write.writerow(val)
  
  
# list to store the values of the rows
rows = []
val = []

current_date_time = datetime.now()
val1 = "Situps"
val2 = " 60 "


val.append(current_date_time)
val.append(val1)
val.append(val2)

rows.append(val)

write_in_csv(rows)
