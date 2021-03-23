# wpnsmith_send.py - sends a text when Banshee is selling a mod that is not in Collections

from wpnsmith_creds import getLogin
from wpnsmith_getMod import getMod
from wpnsmith_guardianList import guardianList
import smtplib      #   Used to send emails as texts

# Create list of phone numbers, initials, and carrier code formatted: (PhoneNumber, 2-char .txt file prefix and carrier char)
guardian = guardianList()

# Dictionary used for faster email lookup
domain = {
    'a': '@mms.att.net',
    'c': '@mms.cricketwireless.net',
    'v': '@vzwpix.com'
}

# Get credentials to log into the email address
creds = getLogin()

### This function searches for the daily Banshee mod among the available modlist.txt files
###     and sends a text if the mod is listed as not owned.
def send():
    # Connect to SMTP to send emails
    smtpConn = smtplib.SMTP('smtp.gmail.com', 587)
    smtpConn.ehlo()
    smtpConn.starttls()
    smtpConn.login(creds[0], creds[1])
    
    # Determine today's mod
    modName = getMod()
    
    # Counter for number of texts sent
    sent = 0
    
    # Loop through each modlist file
    for g in guardian:
        # Open appropriate text file
        file = g[1][0:2] + 'modlist.txt'
        
        try:
            with open(file, 'r') as modList:
                # Generate list of needed mods
                modsNeeded = [line.casefold() for line in modList]
                
                # Search for the daily mod in the list of needed mods, accomodating for case and new lines
                if (modName.casefold()+'\n') in modsNeeded:
                    # Send text/email
                    message = 'Guardian. Just a heads up. I have the ' + modName + ' mod in stock today. It\'s not in your collection. Send me a "$" to let me know if you pick it up, and I\'ll cross it off for ya.'
                    recipient = modsNeeded[0] + domain[g[1][2]]
                    smtpConn.sendmail(creds[0], recipient, message)
                    
                    # Increment number of text notifications sent
                    sent += 1
         
        # If file cannot be opened, skip the rest of the function
        except: 
            modsNeeded = []
        
    # Disconnect from SMTP
    smtpConn.quit()
    
    print("Notifications sent: %d" %sent)
    
    return;

send()
