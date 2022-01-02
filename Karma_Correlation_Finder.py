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
    dataMatrix.append(["user", "karma", "Total Words", "Total Characters"])

    for x in subjects:
        #content = PushshiftIO.get_user_comments(x) + " " + PushshiftIO.get_user_submissions(x)
        content = ""
        for y in PushshiftIO.get_user_comments(x):
            content += y
            content += " "
        for y in PushshiftIO.get_user_submissions(x):
            content += y[0].strip() 
            content += " "
            content += y[1].strip()
            content += " "
        user_statistics = [x, len(content), len(content.split())]
        dataMatrix.append(user_statistics)

    final_data = pd.DataFrame(dataMatrix)
    final_data.to_csv("final_results.csv")
