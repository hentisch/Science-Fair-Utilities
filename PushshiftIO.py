import requests
from random import randint
import numpy as np
import time
from tqdm import tqdm

class PushshiftIO:
    delay = 60 / (requests.get("https://api.pushshift.io/meta").json()["server_ratelimit_per_minute"] - 20) #This is measured in requests per minute. Due to many errors in real world use, this has been reduced to 100 requests per minute
    total_times_limited = 0
    print(delay)


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
        return [(x["title"].strip("\n"), x.get("selftext", "").strip("\n")) for x in json_response['data'] if x["is_self"] or len(x.get("selftext", "")) > 300]            
    
    @staticmethod
    def get_all_user_content(user: str) -> str:
        content = ""
        times_rate_limited = 0
        while len(content) <= 0:
            try:
                for x in PushshiftIO.get_user_submissions(user):
                    content += x[0] + "\n" + x[1] + "\n"
                for x in PushshiftIO.get_user_comments(user):
                    content += x + "\n"
                return content
            except Exception as e:
                PushshiftIO.total_times_limited += 1
                content = ""
                wait_time = 60 + (12**PushshiftIO.total_times_limited) #This will increase our wait time exponentially to avoid real rate-blocks
                PushshiftIO.delay += (0.2**PushshiftIO.total_times_limited)*0.2
                print("Unexpected rate limit, currently waiting for " + str(wait_time) + " seconds in order to avoid longer blockage. The request delay has also been increased to " + str(PushshiftIO.delay))
                print("The exact error produced was :" + str(e))
                time.sleep(wait_time) 
                times_rate_limited += 1

if __name__ == "__main__":
    """"
    with open("/Volumes/Lexar/Git_Code/Science-Fair-Utilities/content.txt", "w") as f:
        f.write(PushshiftIO.get_all_user_content(PushshiftIO.get_random_user()[0]))
    """