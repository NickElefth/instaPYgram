"""
Data logger helper functions for 24Hours could so we avoid interruction with the same pic_href
"""
import json
import itertools
from datetime import datetime
import os

TIMESTAMP_DAY = 86400


def get_timestamp():
    timestamp = datetime.timestamp(datetime.now())
    return timestamp

def get_datetime():
    date_time = str(datetime.now()).split('.')[0]  # remove decimals from seconds
    date, time = date_time.split(' ')
    return date, time


def load_json_file(file_name):
    data = {}
    try:
        with open(file_name, "r+") as file:
            data = json.load(file)
    except FileNotFoundError:
        pass  # File does not exist
    return data


def gather_logged_hrefs():
    logged_data = load_json_file("instagramLogger.json")
    instagram_hrefs = [[href for href in hrefs] for hrefs in logged_data.values()]
    instagram_hrefs = list(itertools.chain.from_iterable(instagram_hrefs))
    return instagram_hrefs


def log_instagram_hrefs(list_of_pictures):
    """
    Stores links which we have already interacted withing the last 24h
    """
    data = load_json_file("instagramLogger.json")
    data = clean_up_old_data(data)
    with open("instagramLogger.json", "w+") as file:  
        data.update({get_timestamp() : list_of_pictures})
        json.dump(data, file)


def log_instagram_stats(likes, comments, new_following, hashtags, comments_list, current_followers, current_following):
    """
    Logs statistics of each run
    """
    data = load_json_file("instagramStats.json")
    if not data:
        data = []
    date, time = get_datetime()
    with open("instagramStats.json", "w+") as file:  
        data.append(
            {
                "Date": date,
                "Time": time,
                "New Likes": likes,
                "New Comments": comments,
                "New Following": new_following,
                "HashTags Used": hashtags,
                "Comments Used": comments_list,
                "Current Followers": current_followers,
                "Current Following": current_following,
            }
        )
        json.dump(data, file)


def clean_up_old_data(links_dict):
    """
    Clean up data which are older than 24h
    """
    expired_timestamps = []
    for timestamp in links_dict:
        if float(timestamp) < get_timestamp() - TIMESTAMP_DAY:
            expired_timestamps.append(timestamp)
    for timestamp in expired_timestamps:
        del links_dict[timestamp]
    return links_dict
