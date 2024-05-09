import os
import shutil
from datetime import datetime

# Get the absolute path of the current script
parent_directory_path = os.path.dirname(os.path.abspath(__file__))

directory_path = os.path.join(parent_directory_path, "tempUserData")

print("Exploring directories in:", directory_path)

# Iterate over the items in the directory
for item in os.listdir(directory_path):
    # Build the full path of the item
    item_path = os.path.join(directory_path, item)
    # Check if it is a directory
    if os.path.isdir(item_path):
        # Get the date of the last modification
        mod_time = os.path.getmtime(item_path)
        # Convert the modification date into a readable format
        mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        # Calculate the age of the directory in mins
        age_minutes = int((datetime.now() - datetime.fromtimestamp(mod_time)).total_seconds() / 60)
         # Check if the age is greater than 10 minutes
        if age_minutes > 10:
            # Remove the directory and its contents
            shutil.rmtree(item_path)
        print(f"Directory: {item}, Last Modified: {mod_time_str}, Age: {age_minutes} minutes")
