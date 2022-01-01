from pandas.core.reshape.concat import concat
import matplotlib as plt
from PushshiftIO import PushshiftIO
import pandas as pd
import numpy as np
trials = 0
accounts = []

finalData = pd.DataFrame(columns=["user", "karma", "Total Words", "Total Characters"])

subjects = PushshiftIO.get_random_users(trials)
dataMatrix = []

for x in subjects:
    content = PushshiftIO.get_user_comments(x) + " " + PushshiftIO.get_user_submissions(x)
    user_statistics = [x, len(content), len(content.split())]
    dataMatrix.append(user_statistics)

finalData.concat(dataMatrix)
finalData.to_csv("final_results.csv")

