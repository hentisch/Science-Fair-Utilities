import pickle as pkl
import delta
import sys
import pandas as pd
from tqdm import tqdm
import os
from math import ceil
#http://dev.digital-humanities.de/ci/job/pydelta-next/Documentation/GettingStarted.html
def truncate_collumns(sheet, n:int):
    for i, x in enumerate(sheet.columns):
        if i+1 > n:
            sheet.drop(x, axis=1, inplace=True)
    return sheet

def crop_series(series, n:int):
    for i, x in enumerate(series):
        if i+1 > int:
            series.drop(x, axis=1, inplace=True)
    return series

def load_from_pickle(file:str):
    with open(file, "rb") as f:
        return pkl.load(f)

def get_int_in_str(seq:str):
    nums = [int(x) for x in seq if x.isdigit()]
    int_rep = 0
    for i, x in enumerate(reversed(nums)):
      int_rep += x*10**(i)
    return int_rep

def sort_feature_matrices(arr:list):
    return sorted(arr, key= lambda x: get_int_in_str(x), reverse=False)

def split(a, n):
    n = min(n, len(a))
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def main():
    #This block creates the feature matrices

    try:
        current_progress:list = os.listdir(f"feature-matrices({sys.argv[2]}-gram)")
    except FileNotFoundError:
        current_progress = []
        os.mkdir(f"feature-matrices({sys.argv[2]}-gram)")
    source_directory = sort_feature_matrices(os.listdir(sys.argv[1]))
    absent_corpera = [x for x in source_directory if get_int_in_str(x) not in [get_int_in_str(y) for y in current_progress]]

    if "-r" in sys.argv:
        absent_corpera.reverse()
    
    if "-s" in sys.argv:
        print(list((split(absent_corpera, int(sys.argv[sys.argv.index("-s") + 1])))))
        absent_corpera = list(split(absent_corpera, int(sys.argv[sys.argv.index("-s") + 1])))[int(sys.argv.index("-s") + 2)]

    for i, x in enumerate(tqdm(absent_corpera)):
        raw_corpus = delta.Corpus(sys.argv[1] + "/" + x, ngrams=int(sys.argv[2])) #As this is the most computationally instensive step, we only want to do it once
        relative_feature_matrix = raw_corpus.get_mfw_table(1000)
        with open(f"feature-matrices({sys.argv[2]}-gram)/features-{str(get_int_in_str(x))}.pickle", "wb") as f:
            pkl.dump(relative_feature_matrix, f)

    if "-f" in sys.argv:
        quit()

    #This block creats the distance matrices for each corpus
    try:
        os.listdir(f"distance-matrices/{sys.argv[2]}-gram")
    except FileNotFoundError:
        corpera = [load_from_pickle(f"feature-matrices({sys.argv[2]}-gram)/{x}") for x in sort_feature_matrices(os.listdir(f"feature-matrices({sys.argv[2]}-gram)"))]
        print("All dataframes loaded")
        
        print("Computing distances....")
        for x in ["distance-matrices", f"distance-matrices/{sys.argv[2]}-gram", f"distance-matrices/{sys.argv[2]}-gram/cosine_delta", f"distance-matrices/{sys.argv[2]}-gram/burrows"]:
            try:
                os.mkdir(x)
            except FileExistsError:
                pass
        
        for i, x in enumerate(tqdm(corpera)):
            with open(f"distance-matrices/{sys.argv[2]}-gram/cosine_delta/distances-{i+1}.pickle", "wb") as f:
                if "-c" in sys.argv:
                    distances = delta.functions.cosine_delta(truncate_collumns(x, int(sys.argv[sys.argv.index("-c")+1])))
                else:
                    distances = delta.functions.cosine_delta(x)
                pkl.dump(distances, f)
            with open(f"distance-matrices/{sys.argv[2]}-gram/burrows/distances-{i+1}.pickle", "wb") as f:
                if "-c" in sys.argv:
                    distances = delta.functions.burrows(truncate_collumns(x, int(sys.argv[sys.argv.index("-c")+1])))
                else:
                    distances = delta.functions.burrows(x)
                pkl.dump(distances, f)
        #Note that both of these measures are thsoe of DISTANCE, not similarity

        print("Distances computed!!!")
    
    if "-d" in sys.argv:
        quit()
    
    #This block does the actuall testing
    for x in ["experiment-results", f"experiment-results/{sys.argv[2]}-gram", f"experiment-results/{sys.argv[2]}-gram/cosine_delta",f"experiment-results/{sys.argv[2]}-gram/burrows"]:
        try:
            os.mkdir(x)
        except FileExistsError:
            pass
    
    distances_matrices_cosine = [pd.read_pickle(f"distance-matrices/{sys.argv[2]}-gram/cosine_delta/" + x) for x in sort_feature_matrices(os.listdir(f"distance-matrices/{sys.argv[2]}-gram/cosine_delta/"))]
    distances_matrices_burrows = [pd.read_pickle(f"distance-matrices/{sys.argv[2]}-gram/burrows/" + x) for x in sort_feature_matrices(os.listdir(f"distance-matrices/{sys.argv[2]}-gram/burrows/"))]

    with open(f"experiment-results/{sys.argv[2]}-gram/cosine_delta/results.csv", "w") as f:
        f.writelines("author,position,corpus\n")
        for p, c in enumerate(tqdm(distances_matrices_cosine)):
            for x in c.columns:
                if x[:4] != "#TS#":
                    df = c[x]
                    df = df.sort_values(ascending=True)
                    df.drop(x, inplace=True) #In our correlation matrix, the author will ALWAYS be the first column, as the distance between x and x is 0
                    authors = list(df.index.values)
                    f.writelines(f"{x},{ceil((authors.index('#TS#' + x)+2) / 2)},{p+1}\n")  
                    #We add one value to the index to account for the difference between counting systems, and then one to 
                    #account for the lost inital value, so we can divide by two, which is neccisary to consider each user
                    #as distinct and not 

    with open(f"experiment-results/{sys.argv[2]}-gram/burrows/results.csv", "w") as f:
        f.writelines("author,position,corpus\n")
        for p, c in enumerate(tqdm(distances_matrices_burrows)):
            for x in c.columns:
                if x[:4] != "#TS#":
                    df = c[x]
                    df = df.sort_values(ascending=True)
                    df.drop(x, inplace=True) #In our correlation matrix, the author will ALWAYS be the first column, as the distance between x and x is 0
                    authors = list(df.index.values)
                    f.writelines(f"{x},{ceil((authors.index('#TS#' + x)+2) / 2)},{p+1}\n")  
                    #We add one value to the index to account for the difference between counting systems, and then one to 
                    #account for the lost inital value, so we can divide by two, which is neccisary to consider each user
                    #as distinct and not 
if __name__ == "__main__":
    main()

#TS#