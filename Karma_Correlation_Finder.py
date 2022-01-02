from pandas.core.reshape.concat import concat
import matplotlib as plt
from PushshiftIO import PushshiftIO
import pandas as pd
import numpy as np
import sys
trials = 2 #sys.argv[1]
accounts = []
try:
    open("final_results.csv")
except FileNotFoundError:

    subjects = PushshiftIO.get_random_users(trials)
    dataMatrix = []
    dataMatrix.append(["user", "comment_karma", "submission_karma", "Total Words", "Total Characters (not including spaces)"])

    for x in subjects:
        content = PushshiftIO.get_all_user_content(x)
        words_list = content.split(" ")
        character_count = 0
        for x in words_list:
            character_count += len(x)
        user_statistics = [x[0], x[4], x[5], len(words_list), character_count]
        dataMatrix.append(user_statistics)

    final_data = pd.DataFrame(dataMatrix)
    final_data.to_csv("final_results.csv")
