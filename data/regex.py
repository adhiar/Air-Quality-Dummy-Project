import os
import re

# Define the directory containing the files
directory = './submission/data'

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Make sure we're only dealing with files (ignore directories)
    if os.path.isfile(os.path.join(directory, filename)):
        
        # Match the pattern: prsa_name1_name2_name3 (or with any extension like .txt, .jpg)
        match = re.match(r'PRSA_(\w+)_(\w+)', filename)
        
        if match:
            # Extract name1 and name2
            name1 = match.group(1)
            name2 = match.group(2)
            
            
            # Create the new filename: name1_name2 (with extension if any)
            new_filename = f'{name2}.csv'
            
            # Get the full paths
            old_file = os.path.join(directory, filename)
            new_file = os.path.join(directory, new_filename)
            
            # Rename the file
            os.rename(old_file, new_file)
            print(f'Renamed: {filename} -> {new_filename}')
