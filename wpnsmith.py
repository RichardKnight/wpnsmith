# wpnsmith.py - sends a text alert when Banshee is selling a mod that isn't in Collections

import requests     #   Used to access vendor website
import bs4          #   Used to pull HTML of vendor inventory
import smtplib      #   Used to send emails as texts
import imapclient   #   Used to check for any replies
import pyzmail      #   Used to parse received emails
from apscheduler.schedulers.blocking import BlockingScheduler

# Scheduler used to set speficic times for the rec() and send() functions to run
sch = BlockingScheduler()

# List of tuples in the following format: (PhoneNumber, 2-char .txt file prefix and carrier char)
guardian = [('8885551111','aza'), ('8885552222','bya'), ('8885553333','cxc')]

# Dictionary used for faster lookup by phone number
prefix = dict(guardian)
domain = {
    'a': '@mms.att.net',
    'c': '@mms.cricketwireless.net'
}

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

### This function searches for the daily Banshee mod among the available modlist.txt files
###     and sends a text if the mod is listed as not owned.
def send():
    # Connect to SMTP to send emails
    smtpConn = smtplib.SMTP('smtp.email.com', 587)
    smtpConn.ehlo()
    smtpConn.starttls()
    smtpConn.login('mailbox@email.com', 'PASSWORD')
    
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
                    smtpConn.sendmail('wpnsmthb44@gmail.com', recipient, message)
                    
                    # Increment number of text notifications sent
                    sent += 1
         
        # If file cannot be opened, skip the rest of the function
        except: 
            modsNeeded = []
        
    # Disconnect from SMTP
    smtpConn.quit()
    
    print("Notifications sent: %d" %sent)
    
    return;

### This function scrubs the TodayInDestiny site for vendor inventories and returns the daily Banshee mod
def getMod():
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

  ### Scrape site for Banshee's daily mod
    # Isolate vendor cards
    vendors = soup.findAll('div', class_='vendorCardContainer')
    
    # Search through cards for Banshee-44
    for v in vendors:
        if v.find('p', class_='vendorCardHeaderName').string == "Banshee-44":
            # Isolate the "Material Exchange" portion of the vendor card
            exchange = v.find('div', identifier='category_materials_exchange')
            
            # Separate into individual items
            items = exchange.findAll('div', class_='vendorInventoryItemContainer')
            
            # Obtain the names of each item
            itemNames = [i.find('p', class_='itemTooltip_itemName').string for i in items]

    # Convert modName from bs4 NavigableString to a string
    #   The mod in question is always second in the list
    modName = "".join(map(str, itemNames[1]))

    return modName;

# Schedule job to check for a response 30 minutes before refresh
sch.add_job(lambda: rec(), 'cron', hour=11, minute=30)

# Schedule job to check Banshee's inventory after refresh
sch.add_job(lambda: send(), 'cron', hour=13, minute=30)

sch.start()

