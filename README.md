# InstaPYgram 

* A simple python instagram Bot for gaining organic instagram followers *

## Prerequisites 

1) Python 3+
2) Selenium
3) geckodriver

## Quick Start

Currently there are two options available for the instaBotExecutor.py

1) Execute the instaBotExecutor.py with the --find-unfollowers option to retrieve a list of followers
2) Execute the instaBotExecutor.py with the --hashtag-automation option and pass a comma seperated string of comments and hashtags to run the Bot
3) Execute the instaBotExecutor.py with --unfollow-unfollowers option to find and unfollow unfollowers you can specify the number of unfollowers you would like to unfollow at the current execution using --number-to-unfollow arg
4) Change creds.py with your IG username and password

#### Example
'''
python instaBot.py --find-unfollowers --comments "Great post !, Cool post!" --hastags "exampletag, exampletag2"
'''

Feel free to suggest improvements!