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


def load_json_file():
    data = {}
    try:
        with open("instagramLogger.json", "r+") as file:
            data = json.load(file)
            data = clean_up_old_data(data)
    except FileNotFoundError:
        pass  # File does not exist
    return data


def gather_logged_hrefs():
    logged_data = load_json_file()
    instagram_hrefs = [[href for href in hrefs] for hrefs in logged_data.values()]
    instagram_hrefs = list(itertools.chain.from_iterable(instagram_hrefs))
    return instagram_hrefs


def log_instagram_hrefs(list_of_pictures):
    data = load_json_file()
    with open("instagramLogger.json", "w+") as file:  
        data.update({get_timestamp() : list_of_pictures})
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

