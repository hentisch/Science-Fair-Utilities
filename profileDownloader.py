from io import FileIO
import linecache
import requests
import json
from random import randint, random
from linecache import getline

def read_specific_line(file:FileIO, line_index:int) -> str:
    for i, line in enumerate(file):
        if i == line_index-1:
            return line

def get_random_user() -> str:
    with open("69M_reddit_accounts.csv", "r") as user_list: #this file is 69382539 lines long
        return read_specific_line(randint(1, 69382539), user_list).split(",")[1]

def get_user_comments(user: str) -> list: 
    url = f"https://api.pushshift.io/reddit/search/comment/?author={user}"
    request = requests.get(url)
    json_response = request.json()
    return json_response['data'] 

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

def main():
    """"
    userData = []
    while len(userData) <= 0:
        userData = get_user_submissions(get_random_user())
    print(userData)
    """
    with open("69M_reddit_accounts.csv", "r") as user_list:
        print("ehhhh")
        print(linecache.getline("69M_reddit_accounts.csv", 69382539))
    

if __name__ == "__main__":
    main()