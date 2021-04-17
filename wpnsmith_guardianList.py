# wpnsmith_guardianList.py - generates a list of tuples from the modlist.txt files in the current directory

import os

### Create list of tuples in the following format: (PhoneNumber, 2-char .txt file prefix and carrier char) from available txt files
def guardianList():
    # Obtain current working directory
    cwd = os.getcwd()
    
    # Initialize the empty tuple list
    guardian = list()

    # Loop through the files in the cwd for any files ending in "modlist.txt"
    for file in os.listdir(cwd):
        filename = os.fsdecode(file)
        if filename.endswith('modlist.txt'):
            # Open the file to obtain the phone number (first line of txt file) and the initials and carrier code (filename)
            with open(file, 'r') as f:
                gTuple = (f.readline().rstrip(), filename[0:3])
                # Add the tuple to the list of tuples
                guardian.append(gTuple)
    
    return guardian;