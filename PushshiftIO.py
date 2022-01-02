import pandas
import requests
import json
import pandas
from random import randint
import numpy as np
import time
import random

class PushshiftIO:

    current_requests = 0
    current_minute = 0
    rate_limit = requests.get("https://api.pushshift.io/meta").json()["server_ratelimit_per_minute"] - 1 #This is measured in requests per minute. Also, just for saftey, we run exactly 1 request under the posted limit 

    @staticmethod
    def get_minute() -> int:
        return int(time.time() / 60)

    @staticmethod
    def check_rate() -> bool:
        if PushshiftIO.get_minute() > PushshiftIO.current_minute:
            PushshiftIO.current_requests = 0
            PushshiftIO.current_minute = PushshiftIO.get_minute()
        return PushshiftIO.current_requests < PushshiftIO.rate_limit
    
    @staticmethod
    def update_request_count():
        if PushshiftIO.get_minute() > PushshiftIO.current_minute:
            PushshiftIO.current_minute = PushshiftIO.get_minute()
            PushshiftIO.current_requests = 1
        else:
            PushshiftIO.current_requests += 1

    @staticmethod
    def read_specific_line(line_index:int, file) -> str:
        for i, line in enumerate(file):
            if i == line_index-1:
                return line
    
    @staticmethod
    def read_specific_lines(line_indexes:list, file) -> list:
        print("reading lines")
        with open(file, 'r') as f:
            lines = []
            maximum = max(line_indexes)
            for i, line in enumerate(f):
                if (i+1) in line_indexes:
                    lines.append(line.strip())
                if (i+1) > maximum:
                    return lines
            return lines

    @staticmethod
    def get_random_user() -> str:
        with open("69M_reddit_accounts.csv", "r") as user_list: #this file is 69382539 lines long
            return PushshiftIO.read_specific_line(randint(1, 69382539), user_list)
    
    @staticmethod
    def get_unique_array(length:int, max:int, min:int) -> np.array:
        numbers = np.random.randint(low=min, high=max, size=length)
        while len(np.unique(numbers)) < length:
            numbers = np.random.randint(low=min, high=max, size=length)
        print(numbers)
        return numbers
    
    @staticmethod
    def get_random_users(users:int) -> list:
        return PushshiftIO.read_specific_lines(PushshiftIO.get_unique_array(length=users, max=1000, min=3), "/Volumes/Lexar/Git_Code/Science-Fair-Utilities/69M_reddit_accounts.csv") #69382539 should be the max

    @staticmethod
    def get_user_comments(user: str) -> list: 
        url = f"https://api.pushshift.io/reddit/search/comment/?author={user}"
        print(url)
        request = requests.get(url)
        json_response = request.json()
        return [e["body"].strip("\n") for e in json_response['data']]

    @staticmethod
    def get_user_submissions(user: str) -> list: 
        url = f"https://api.pushshift.io/reddit/search/submission/?author={user}"
        print(url)
        request = requests.get(url)
        json_response = request.json()
        return [ (x["title"].strip("\n"), x["selftext"].strip("\n")) for x in json_response['data']]

        """
        For submissions, the ["selftext"] field and ["title"] field are what return the socially relevent data. 
        The is_self field will retrurn true if the sumbssion doesetn link to anything, which can be really helpfull 
        for figuring out when a post is really just a reposted article from the internet
        """

print("Current Rate Limit: " + str(PushshiftIO.rate_limit))

while True:
    if PushshiftIO.check_rate():
        PushshiftIO.update_request_count()
        time.sleep(random.random())
    print(PushshiftIO.current_requests)