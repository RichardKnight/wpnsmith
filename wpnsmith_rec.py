# wpnsmith_rec.py - checks for responses to texts sent from wpnsmith_send.py, indicating the mod list needs to be updated

from wpnsmith_getMod import getMod
import smtplib      #   Used to send emails as texts
import imapclient   #   Used to check for any replies
import pyzmail      #   Used to parse received emails

# List of tuples in the following format: (PhoneNumber, 2-char .txt file prefix and carrier char)
guardian = [('8885551111','aza'), ('8885552222','bya'), ('8885553333','cxc')]

# Dictionary used for faster lookup by phone number
prefix = dict(guardian)

### This function logs into the email address to check for any responses, indicating that a mod has been purchased
def rec():
    # Connect to IMAP to check for a previous response
    imapConn = imapclient.IMAPClient('imap.email.com', ssl=True)
    imapConn.login('mailbox@email.com', 'PASSWORD')
    imapConn.select_folder('INBOX')
    
    # Search for unread emails
    UIDs = imapConn.search(['UNSEEN'])
    
    # Determine today's mod in a variable to accomodate for case and new lines
    modName = getMod().casefold() + '\n'
    
    # Counter for valid email responses
    responses = 0
    
    # Loop through unread emails
    for e in UIDs:
        # Grab raw email data and convert to usable data with pyzmail
        rawEmail = imapConn.fetch(e, ['BODY[]', 'FLAGS'])
        email = pyzmail.PyzMessage.factory(rawEmail[e][b'BODY[]'])
        body = email.html_part.get_payload().decode(email.html_part.charset)
        
        # Check body of email for symbol used to indicate an update
        if "$" in body:
            # Isolate the phone number at the front of the email address
            sender = email.get_address('from')[1][0:10]
            
            # Verify that the sender has an associated modlist.txt file
            if sender in prefix:
                # Open appropriate text file for the sender
                file = prefix[sender] + "modlist.txt"
                
                # Increment the number of valid responses
                responses += 1
                
                try:
                    with open(file, 'r') as modList:
                        # Generate list of needed mods
                        modsNeeded = [line.casefold() for line in modList]
                # If file isn't found, create an empty list for modsNeeded
                except:
                    modsNeeded = []
                
                # Search for the daily mod in the list of needed mods
                if modName.casefold() in modsNeeded:
                    # Remove the mod name from the list if it is found
                    modsNeeded.remove(modName)
                    
                    # Write the updated list to the text file
                    with open(file, 'w') as modList:
                        for m in modsNeeded:
                            modList.write(m)
    
    # Disconnect from IMAP
    imapConn.logout()
    
    print("Valid responses received: %d" %responses) 
    
    return;

rec()
