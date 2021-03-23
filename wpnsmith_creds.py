# wpnsmith_creds.py - pulls the credentials of the email address to be used by other wpnsmith functions.
#                       These credentials are stored in emailcreds.txt, where line 0 is assumed to be
#                       the username and line 1 the password.

import os

### Obtains the email credentials from emailcreds.txt
def getLogin():
    # Obtain current working directory
    cwd = os.getcwd()
    
    # Initialize the empty tuple list
    creds = tuple()

    # Loop through the files in the cwd for the file "emailcreds.txt"
    for file in os.listdir(cwd):
        filename = os.fsdecode(file)
        if filename.endswith('emailcreds.txt'):
            # Open the file to obtain the email login information
            with open(file, 'r') as f:
                creds = (f.readline().rstrip(), f.readline().rstrip())

    return creds;