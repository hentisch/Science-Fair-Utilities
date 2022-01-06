import json
from json.decoder import JSONDecodeError
from os import error, wait
import requests
from random import randint
import numpy as np
import time
from tqdm import tqdm


class PushshiftIO:
    delay = 60 / (requests.get("https://api.pushshift.io/meta").json()["server_ratelimit_per_minute"] - 20) #This is measured in requests per minute. Due to many errors in real world use, this has been reduced to 100 requests per minute
    total_times_limited = 0


    @staticmethod
    def read_specific_line(line_index:int, file) -> str:
        for i, line in enumerate(file):
            if i == line_index-1:
                return line
    
    @staticmethod
    def read_specific_lines(line_indexes:list, file, show_output=True) -> list:
        with open(file, 'r') as f:
            lines = []
            maximum = max(line_indexes)
            if show_output:
                with tqdm(total=maximum) as pbar:
                    for i, line in enumerate(f):
                        if (i+1) in line_indexes:
                            lines.append(line.strip())
                        if (i+1) > maximum:
                            return lines
                        pbar.update(1)
            else:
                for i, line in enumerate(f):
                    if (i+1) in line_indexes:
                        lines.append(line.strip())
                    if (i+1) > maximum:
                        return lines
            return lines

    @staticmethod
    def get_random_user() -> str:
        with open("69M_reddit_accounts.csv", "r") as user_list: #this file is 69382539 lines long
            raw_value = PushshiftIO.read_specific_line(randint(2, 69382539), user_list)
            return raw_value.split(",")[1], raw_value.split(",")[4], raw_value.split(",")[5]
            #this file is structured as id,name,created_utc,updated_on,comment_karma,link_karma\
            #return PushshiftIO.read_specific_line(randint(1, 69382539), user_list)
    
    @staticmethod
    def get_unique_array(length:int, max:int, min:int) -> np.array:
        numbers = np.random.randint(low=min, high=max, size=length*2)
        while len(np.unique(numbers)) < length:
            numbers = np.random.randint(low=min, high=max, size=length*2)
        return np.random.permutation(np.unique(numbers))[:length]
    
    @staticmethod
    def get_random_users(users:int) -> list:
        return [(x.split(',')[1], x.split(',')[4], x.split(',')[5]) for x in PushshiftIO.read_specific_lines(PushshiftIO.get_unique_array(length=users, max=69382539, min=2), "69M_reddit_accounts.csv")]
        #69382539 should be the max

    @staticmethod
    def get_user_comments(user: str) -> list: 
        #TODO: Please implement these to crawl back through a users history and get EVERYTHING they have posted that way
        #Also, based on testing the returned results are limited to 100 despite what documentation says
        results = 101 
        content = []
        last_time = 0
        try:
            while results >= 100:
                url = f'https://api.pushshift.io/reddit/search/comment/?author={user}&frequency="second"&metadata=true&sort=asc&size=100&fields=body,created_utc&after={last_time}'
                request = requests.get(url)
                if request.status_code != 429:
                    try:
                        json_response = request.json()
                    except ValueError:
                        time.sleep(PushshiftIO.delay)
                        continue
                else:
                    PushshiftIO.total_times_limited += 1
                    wait_time = 60 + (12**PushshiftIO.total_times_limited)
                    PushshiftIO.delay += (0.2**PushshiftIO.total_times_limited)*0.2
                    print(f"Unexpected rate limit, currently waiting for {wait_time} seconds in order to avoid longer blockage. The request delay has also been increased to {PushshiftIO.delay}")
                    time.sleep(wait_time)
                    continue
                last_time = json_response["data"][-1]["created_utc"]
                content +=  [e["body"].strip("\n") for e in json_response['data']]
                results = json_response['metadata']['total_results']
                time.sleep(PushshiftIO.delay)
            return content
        except IndexError:#if there is no data then last entry will be empty
            return []

    @staticmethod
    def get_user_submissions(user: str) -> list:
        results = 101
        content = []
        last_time = 0
        try:
            while results >= 100:
                url = f'https://api.pushshift.io/reddit/search/submission/?author={user}&frequency="second"&metadata=true&sort=asc&size=100&fields=title,selftext,is_self,created_utc&after={last_time}'
                request = requests.get(url)
                if request.status_code != 429:
                    try:
                        json_response = request.json()
                    except ValueError:
                        time.sleep(PushshiftIO.delay)
                        continue
                else:
                    PushshiftIO.total_times_limited += 1
                    wait_time = 60 + (12**PushshiftIO.total_times_limited)
                    PushshiftIO.delay += (0.2**PushshiftIO.total_times_limited)*0.2
                    print(f"Unexpected rate limit, currently waiting for {wait_time} seconds in order to avoid longer blockage. The request delay has also been increased to {PushshiftIO.delay}")
                    time.sleep(wait_time)
                    continue
                last_time = json_response["data"][-1]["created_utc"]
                content += [(x["title"].strip("\n"), x.get("selftext", "").strip("\n")) for x in json_response['data'] if x["is_self"] or len(x.get("selftext", "")) > 300]            
                results = json_response['metadata']['total_results']
                time.sleep(PushshiftIO.delay)
            return content
        except IndexError: 
            return []
    @staticmethod
    def get_all_user_content(user: str) -> str:
        content = ""
        for x in PushshiftIO.get_user_submissions(user):
            content += x[0] + "\n" + x[1] + "\n\n"
        for x in PushshiftIO.get_user_comments(user):
            content += x + "\n\n"
        return content


if __name__ == "__main__":
    """"
    with open("/Volumes/Lexar/Git_Code/Science-Fair-Utilities/content.txt", "w") as f:
        f.write(PushshiftIO.get_all_user_content(PushshiftIO.get_random_user()[0]))
    """