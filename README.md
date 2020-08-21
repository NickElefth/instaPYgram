# InstaPYgram

* A simple python instagram Bot for gaining organic instagram followers *

## Functionality

1) Find Unfollowers
2) Unfollow unfollowers
3) Specify number of unfollowers to unfollow
4) Search for posts using hashtags
5) Like, Comment, Follow users
6) Randomly select a comment based on the list of comments you supplied
7) Only follow users which have less than 1500 followers
8) Log interacted posts so that the bot won't comment more than once on one pic
9) Log Instagram stats at each bot execution
    Stats include:
        * Date of execution
        * Time of execution
        * New InstaBot likes
        * New InstaBot Comments
        * New InstaBot Following
        * Hashtags Used
        * Comments Used
        * Current Followers at the time of execution
        * Current Following at the time of execution
10) Produces report of analytics gathered over executions

## Prerequisites

1) Python 3+
2) Selenium
3) geckodriver
4) Firefox Browser
5) pandas

## Quick Start

Currently there are two options available for the instaBotExecutor.py

1) Execute the `instaBotExecutor.py` with the `--find-unfollowers` option to retrieve a list of followers
2) Execute the `instaBotExecutor.py` with the `--hashtag-automation` option and pass a comma seperated string of comments and hashtags to run the bot, if you want to just like the hashtag related images, pass the `--only-likes` flag
3) Execute the `instaBotExecutor.py` with `--unfollow-unfollowers` option to find and unfollow unfollowers. You can specify the number of unfollowers you would like to unfollow at the current execution using `--number-to-unfollow` arg
4) Change `creds.py` with your IG username and password
5) Execute the `instaBotExecutor.py` with the `--produce-report` to get a stats report. You need to run the bot at least once to collect data

#### Example
```
python3 instaBotExecutor.py --hashtag-automation --comments "Great post, Cool post guys, This is awesome. I would totally recommend you to others, Fantastic post! Keep up the good work, Incredible work we absolutely love it" --hashtags "webdeveloper, code"
```

#### Note

If you are using the latest version of Python3 then to install prerequisties please use `pip3 install` and `python3 instaBot.py ...` otherwise use `python` and `pip`

Use it wisely :)
Happy farming!

Feel free to suggest improvements!