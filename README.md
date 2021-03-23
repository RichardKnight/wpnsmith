# wpnsmith
Python script used to send text alerts when certain mods are being sold by the Gunsmith Banshee in Destiny, and accept responses indicating the list of needed mods should be updated.

## Depenencies

Several libraries must be installed for this script to run

```bash
pip install requests
pip install bs4
pip install imapclient
pip install pyzmail36
```

## Usage

This can be set up to run with Windows Task Scheduler with two separate batch files, which I have set to run at 11:30AM (rec) and 1:30PM (send).

```bash
wpnsmith_rec.bat
"Path where Python exe is stored\python.exe" "Path where Python script is stored\wpnsmith_rec.py" > logs_rec.txt

wpnsmith_send.bat
"Path where Python exe is stored\python.exe" "Path where Python script is stored\wpnsmith_send.py" > logs_send.txt
```

The respective logs files will show the day's mod name, as well has how many texts were sent/recieved.

The script expects that each modlist.txt within the current directory will follow a certain format. The naming convention uses two initals as a prefix to the file name and a 1-char code to indicate the carrier (i.e. 'azamodlist.txt').

The contents of the files start with the first line matching the phone number that correlates to the initials within the "guardian" list of tuples.

Subsequent lines should have the name of each mod that the player still needs, one per line.

Email credentials should be in an "emailcreds.txt" document within the directory, where the first line is the user name, and second line is the password.

Your mailbox service may indicate an insecure connection; security is not being taken into account for this script, as I created a standalone mailbox specifically for this project.

## Roadmap

* **Create a dependencies package**
* **Bungie API integration**
