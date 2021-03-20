# wpnsmith.py - sends a text alert when Banshee is selling a mod that isn't in Collections

import requests     #   Used to access vendor website
import bs4          #   Used to pull HTML of vendor inventory
import re           #   Used to search with a regex for the correct container in the HTML
import smtplib      #   Used to send emails as texts
import imapclient   #   Used to check for any replies
import pyzmail      #   Used to parse received emails
from apscheduler.schedulers.blocking import BlockingScheduler

# Scheduler used to set speficic times for the rec() and send() functions to run
sch = BlockingScheduler()

# List of tuples in the following format: (PhoneNumber, .txt file prefix)
guardian = [('8885551111','az'), ('8885552222','by'), ('8885553333','cx')]

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
                
                try:
                    with open(file, 'r') as modList:
                        # Generate list of needed mods
                        modsNeeded = [line.casefold() for line in modList]
                # If file isn't found, create an empty list for modsNeeded
                except:
                    modsNeeded = []
                
                # Determine today's mod in a variable to accomodate for case and new lines
                modName = get_Mod().casefold() + '\n'
                
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
    return;

### This function searches for the daily Banshee mod among the available modlist.txt files
###     and sends a text if the mod is listed as not owned.
def send():
    # Connect to SMTP to send emails
    smtpConn = smtplib.SMTP('smtp.email.com', 587)
    smtpConn.ehlo()
    smtpConn.starttls()
    smtpConn.login('mailbox@email.com', 'PASSWORD')
    
    # Loop through each modlist file
    for g in guardian:
        # Open appropriate text file
        file = g[1] + 'modlist.txt'
        
        try:
            with open(file, 'r') as modList:
                # Generate list of needed mods
                modsNeeded = [line.casefold() for line in modList]
                
                # Determine today's mod
                modName = get_Mod()
                
                # Search for the daily mod in the list of needed mods, accomodating for case and new lines
                if (modName.casefold()+'\n') in modsNeeded:
                    # Send text/email
                    message = 'Guardian. Just a heads up. I have the ' + modName + ' mod in stock today. It\'s not in your collection. Send me a "$" to let me know if you pick it up, and I\'ll cross it off for ya.'
                    recipient = modsNeeded[0] + "@mms.att.net"
                    smtpConn.sendmail('mailbox@email.com', recipient, message)
        # If file cannot be opened, skip the rest of the function
        except: 
            modsNeeded = []
        
    # Disconnect from SMTP
    smtpConn.quit()
    return;

### This function scrubs the TodayInDestiny site for vendor inventories and returns the daily Banshee mod
def get_Mod():
    # Request vendor website
    url = 'https://www.todayindestiny.com/vendors'
    res = requests.get(url)

    # Check for error
    try:
        res.raise_for_status()
    except:
        print("Cannot reach vendor site!!")
        return;

    # Pull site HTML
    soup = bs4.BeautifulSoup(res.text, "html.parser")

    # Pull Banshee's daily mod CSS path
    cssPath = 'div.vendorCardContainer:nth-child(7) > div:nth-child(2) > div:nth-child(4) > div:nth-child(2) > div:nth-child(2)'
    elems = soup.select(cssPath)

    # Convert CSS Path to string
    rawInfo = "".join(map(str, elems))

    # Search for mod name with a non-greedy regex
    #   between <p class="itemTooltip_itemName"> and </p><p class="itemTooltip_itemType">
    modName = re.search('<p class="itemTooltip_itemName">(.*?)</p><p class="itemTooltip_itemType">', rawInfo).group(1)
    
    return modName;

# Schedule job to check for a response 30 minutes before refresh
sch.add_job(lambda: rec(), 'cron', hour=11, minute=30)

# Schedule job to check Banshee's inventory after refresh
sch.add_job(lambda: send(), 'cron', hour=13, minute=30)

sch.start()

