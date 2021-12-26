import pandas
import requests
import json
import pandas
from random import randint
import numpy as np

class PushshiftIO:

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
        return PushshiftIO.read_specific_lines(PushshiftIO.get_unique_array(length=users, max=69382539, min=3), "69M_reddit_accounts.csv") 

    @staticmethod
    def get_user_comments(user: str) -> list: 
        url = f"https://api.pushshift.io/reddit/search/comment/?author={user}"
        request = requests.get(url)
        json_response = request.json()
        return json_response['data'] 

    @staticmethod
    def get_user_submissions(user: str) -> list: 
        url = f"https://api.pushshift.io/reddit/search/submission/?author={user}"
        request = requests.get(url)
        json_response = request.json()
        return [ [x["title"].strip("\n"), x["selftext"].strip("\n")] for x in json_response['data']]

        """
        For submissions, the ["selftext"] field and ["title"] field are what return the socially relevent data. 
        The is_self field will retrurn true if the sumbssion doesetn link to anything, which can be really helpfull 
        for figuring out when a post is really just a reposted article from the internet
        """

