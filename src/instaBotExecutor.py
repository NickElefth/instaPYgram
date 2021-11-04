from time import sleep
from random import randint
from selenium import webdriver
import creds
from instaPYgram import *
import argparse
# from graphData import produce_instapygram_report


def parse_args(args):
    hashtags, comments_list = [], []
    if args.number_to_unfollow:
        try:
            int(args.number_to_unfollow)
        except ValueError:
            print("Invalid value for'--number-to-unfollow'.Value should be an integer")
            exit(1)
    if (not args.comments or not args.hashtags) and args.hashtag_automation and not args.only_likes:
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
    parser.add_argument('--hashtags', action='store',
                        help='Comma seperated string of hashtags')
    parser.add_argument('--comments',  action='store',
                        help='Comma seperated string of comments')
    parser.add_argument('--hashtag-automation', action='store_true',
                        help='Boolean value that starts automated liking, commenting and following pictures using hashtags')
    parser.add_argument('--only-likes', action='store_true',
                        help='Boolean value that is passed with --hashtag-automation to only like pictures')
    parser.add_argument('--find-unfollowers', action='store_true',
                        help="Boolean value that outputs a list of unfollowers")
    parser.add_argument('--unfollow-unfollowers', action='store_true',
                        help="Searches and unfollows unfollowers")
    parser.add_argument('--number-to-unfollow', action="store",
                        help="Number of people to unfollow if not specified will try to unfollow every unfollower")
    parser.add_argument('--produce-report', action="store_true",
                        help="Displays InstaPYgram Report, Must run the InstaBot at least once to collect data")
    # parser.add_argument('--like-following-feed', action="store_true",
    #                     help="Like 50 images from following in your feed")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    bot_initialized = False
    hashtag_args = parse_args(args)
    if args.find_unfollowers or args.hashtag_automation or args.unfollow_unfollowers:
        insta_bot = InstaBot(creds.getUsername(), creds.getPassword(), args.only_likes)
        bot_initialized = True
    if args.find_unfollowers:
        insta_bot.get_unfollowers()
    if args.unfollow_unfollowers:
        insta_bot.unfollow_unfollowers(args.number_to_unfollow)
    if args.hashtag_automation:
        insta_bot.hashtag_automation(
            hashtag_args['hashtags'], hashtag_args['comments'])
    if args.produce_report:
        produce_instapygram_report()
    if bot_initialized:
        insta_bot.end_session()
        print("Instabot has finished.")

    # TODO
    # if args.like_following_feed:
    #     insta_bot.like_following_feed()


try:
    main()
except KeyboardInterrupt:
    print("Interrupted Execution")
