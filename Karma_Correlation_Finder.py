from PushshiftIO import PushshiftIO
import pandas as pd
import numpy as np
trials = 10000
accounts = []

with open("69M_reddit_accounts.csv", "r") as user_list:
    for i in range(trials):
        accounts.append(PushshiftIO.read_specific_line(randint(1, 69382539), user_list))
value = PushshiftIO.get_random_users(10000)
print(value)