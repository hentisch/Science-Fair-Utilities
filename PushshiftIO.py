import pandas
import requests
import json
import pandas
from random import randint
import numpy as np
import time
import random

class PushshiftIO:
    delay = 60 / requests.get("https://api.pushshift.io/meta").json()["server_ratelimit_per_minute"] + 1 #This is measured in requests per minute. Also, just for saftey, we run exactly 1 request under the posted limit 

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
            raw_value = PushshiftIO.read_specific_line(randint(1, 1000), user_list)
            return raw_value.split(",")[1], raw_value.split(",")[4], raw_value.split(",")[5]
            #this file is structured as id,name,created_utc,updated_on,comment_karma,link_karma\
            #return PushshiftIO.read_specific_line(randint(1, 69382539), user_list)
    
    @staticmethod
    def get_unique_array(length:int, max:int, min:int) -> np.array:
        numbers = np.random.randint(low=min, high=max, size=length)
        while len(np.unique(numbers)) < length:
            numbers = np.random.randint(low=min, high=max, size=length)
        print(numbers)
        return numbers
    
    @staticmethod
    def get_random_users(users:int) -> list:
        return [(x.split()[1], x.split()[4], x.split()[5]) for x in PushshiftIO.read_specific_lines(PushshiftIO.get_unique_array(length=users, max=1000, min=3), "/Volumes/Lexar/Git_Code/Science-Fair-Utilities/69M_reddit_accounts.csv") ]
        #69382539 should be the max

    @staticmethod
    def get_user_comments(user: str) -> list: 
        url = f"https://api.pushshift.io/reddit/search/comment/?author={user}"
        request = requests.get(url)
        json_response = request.json()
        time.sleep(PushshiftIO.delay)
        return [e["body"].strip("\n") for e in json_response['data']]

    @staticmethod
    def get_user_submissions(user: str) -> list: 
        url = f"https://api.pushshift.io/reddit/search/submission/?author={user}"
        request = requests.get(url)
        json_response = request.json()
        time.sleep(PushshiftIO.delay)
        return [(x["title"].strip("\n"), x["selftext"].strip("\n")) for x in json_response['data'] if x["is_self"] or len(x["selftext"]) > 300]
    
    @staticmethod
    def get_all_user_content(user: str) -> str:
        content = ""
        for x in PushshiftIO.get_user_submissions(user):
            content += x[0] + "\n" + x[1] + "\n"
        for x in PushshiftIO.get_user_comments(user):
            content += x + "\n"
        return content

if __name__ == "__main__":
    with open("content.txt", "w") as f:
        f.write(PushshiftIO.get_all_user_content(PushshiftIO.get_random_user()[0]))