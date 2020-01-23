# Use Case

Collection of web scrapers and scripts to get an aggregated list of birthdays over multiple web platforms. Also contains a script to display current birthdays on a daily base.

# Installation

install python3

pip3 install python-dateutil
pip3 install selenium

optional: create the plist file: 
    adjust the file setup/com.jr.birthday.notification.plist
    cp setup/com.jr.birthday.notification.plist ~/Library/LaunchAgents/
    chmod +rx ~/Library/LaunchAgents/com.jr.birthday.notification.plist
    launchctl load ~/Library/LaunchAgents/com.jr.birthday.notification.plist
    launchctl start ~/Library/LaunchAgents/com.jr.birthday.notification.plist


# Configuration

copy the config.py file and name the copy config_local.py. 
Store the relevant information in the config file and save.

# Run
## Run the crawler

for facebook:
    - python3 facebook.py 

for confluence:
    python3 confluence-pd.py

## Show birthday overview
to show the birthdays of the current and last two days:
    python3 notification.py
    make sure you configured your texteditor e.g.: "/Applications/Sublime\ Text.app/Contents/SharedSupport/bin/subl"