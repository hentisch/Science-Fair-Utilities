from pandas.core.reshape.concat import concat
import matplotlib as plt
from PushshiftIO import PushshiftIO
import pandas as pd
import numpy as np
import sys
from tqdm import tqdm
trials = int(sys.argv[1])
accounts = []
try:
    open("final_results.csv", "r")
except FileNotFoundError:

    print("Getting Random Users")
    subjects = PushshiftIO.get_random_users(trials)
    print(subjects)
    dataMatrix = []
    dataMatrix.append(["User", "Comment Karma", "Submission Karma", "Total Words", "Total Characters (not including spaces)"])

    print("Getting Data For Selected Users")
    for x, y, z in tqdm(subjects):
        print(x)
        content = PushshiftIO.get_all_user_content(x)
        words_list = content.split(" ")
        character_count = 0
        for a in words_list:
            character_count += len(a)
        user_statistics = [x, y, z, len(words_list), character_count]
        dataMatrix.append(user_statistics)
    for x in dataMatrix:
        print(x)
    final_data = pd.DataFrame(dataMatrix)
    final_data.to_csv("final_results.csv")
    print("Done!")