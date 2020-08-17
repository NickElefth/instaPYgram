from time import sleep
from random import randint
from selenium import webdriver
import creds
from instaPYgram import *
import argparse


def parse_args(args):
    hashtags, comments_list = [], []
    if (not args.comments or not args.hashtags) and args.hashtag_automation:
        print("For hashtag automation you have to provide a list of hashtags and a list of comments")
        exit(1)
    if args.comments:
        try:
            comments_list = args.comments.split(',')
            comments_list = [comment.strip() for comment in comments_list]
        except Exception:
            print("Incorrect formatting of comments. Please provide a comma seperated string")
            exit(1)
    if args.hashtags:
        try:
            hashtags = args.hashtags.split(',')
            hashtags = [tag.strip() for tag in hashtags]
        except Exception:
            print("Incorrect formatting of comments. Please provide a comma seperated string")
            exit(1)
    hashtag_args = {'hashtags': hashtags, 'comments': comments_list}
    return hashtag_args        
  
    
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--hashtags', action='store', help='Comma seperated string of hashtags')
    parser.add_argument('--comments',  action='store', help='Comma seperated string of comments')
    parser.add_argument('--hashtag-automation', action='store_true', help='Boolean value that starts automated liking, commenting and following pictures using hashtags')
    parser.add_argument('--find-unfollowers', action='store_true', help="Boolean value that outputs a list of unfollowers")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    hashtag_args = parse_args(args)
    insta_bot = InstaBot(creds.getUsername(), creds.getPassword())
    if args.find_unfollowers:
        insta_bot.get_unfollowers()
    if args.hashtag_automation:
        insta_bot.hashtag_automation(hashtag_args['hashtags'], hashtag_args['comments'])
    sleep(10)
    print("Instabot has finished.")
    insta_bot.end_session()


try:
    main()
except KeyboardInterrupt:
    print("Interrupted Execution")