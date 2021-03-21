# wpnsmith
Python script used to send text alerts when certain mods are being sold by the Gunsmith Banshee in Destiny, and accept responses indicating the list of needed mods should be updated.

## Requirements

Several libraries must be installed for this script to run

```bash
pip install requests
pip install bs4
pip install imapclient
pip install pyzmail36
pip install apscheduler
```

The script expects that each modlist.txt will follow a certain format. The naming convention uses two initals as a prefix to the file name (i.e. 'azmodlist.txt').

The contents of the files start with the first line matching the phone number that correlates to the initials within the "guardian" list of tuples.

Subsequent lines should have the name each mod that the player still needs, one per line.

## Usage

In both the send() and rec() methods, the mailbox credentials need to be entered along with the appropriate IMAP and SMTP information for the mail service.

Your mailbox service may indicate an insecure connection; security is not being taken into account for this script, as I created a standalone mailbox specifically for this project.

## Roadmap

- This script uses APScheduler to run the functions before and after the daily reset, but I plan on moving each function into a separate file and running them individually using Windows Task Scheduler.

- This currently only works with AT&T phone numbers, which will be updated at a future date. 
