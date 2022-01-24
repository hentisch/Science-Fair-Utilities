from copyreg import pickle
import pickle as pkl
import delta
import sys
import pandas as pd
from tqdm import tqdm
import os
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

def main():
    #This block creates the feature matrices
    complete_features = False

    try:
        files = os.listdir(f"feature-matrices({sys.argv[2]}-gram)") # This just checks if the directory exists, TODO implment the tests to run on each matrix
        complete_features = len(files) == len(sys.argv[1])
    except FileNotFoundError:   
        pass
    except IndexError:
        print("Python3 imposterts_testing.py <path to directory> <ngram count> -c/none")
        quit()

    if not complete_features:
        print("Feature matrices not found, creating...")
        try:
            os.mkdir(f"feature-matrices({sys.argv[2]}-gram)")
        except FileExistsError:
            pass

        current_progress = os.listdir(f"feature-matrices({sys.argv[2]}-gram)")
        source_directory = os.listdir(sys.argv[1])
        absent_corpera = [x for x in source_directory if get_int_in_str(x) not in [get_int_in_str(y) for y in current_progress]]

        for i, x in enumerate(absent_corpera):
            raw_corpus = delta.Corpus(sys.argv[1] + "/" + x, ngrams=int(sys.argv[2])) #As this is the most computationally instensive step, we only want to do it once
            trimmed_corpus = raw_corpus.cull(1/3)
            with open(f"feature-matrices({sys.argv[2]}-gram)/features-{i+1+min(absent_corpera, key= lambda x: get_int_in_str(x))}.pickle", "wb") as f:
                pkl.dump(trimmed_corpus, f)
    
    if "-c" in sys.argv:
        quit()

    #This block creats the distance matrices for each corpus
    try:
        os.listdir(f"distance-matrices/{sys.argv[2]}-gram")
    except FileNotFoundError:
        corpera = [load_from_pickle(f"feature-matrices({sys.argv[2]}-gram)/{x}") for x in sort_feature_matrices(os.listdir(f"feature-matrices({sys.argv[2]}-gram)"))]
        print("All dataframes loaded")
        
        print("Computing distances....")
        for x in ["distance-matrices", f"distance-matrices/{sys.argv[2]}-gram"]:
            try:
                os.mkdir(x)
            except FileExistsError:
                pass
        
        for i, x in enumerate(tqdm(corpera)):
            with open(f"distance-matrices/{sys.argv[2]}-gram/distances-{i+1}.pickle", "wb") as f:
                distances = delta.functions.cosine_delta(x)
                pkl.dump(distances, f)
        
        print("Distances computed!!!")
    
    distances_matrices = []
    for x in sort_feature_matrices(os.listdir(f"distance-matrices/{sys.argv[2]}-gram")):
        distances_matrices.append(load_from_pickle(f"distance-matrices/{sys.argv[2]}-gram/{x}"))
    with open("results.csv", "w") as f:
        f.writelines("author,position,corpus")
        for p, c in enumerate(distances_matrices):
            for x in c.columns:
                if x[:4] != "#TS#":
                    df = distances[x]
                    df = df.sort_values(ascending=True)
                    df.drop(x, inplace=True) #In our correlation matrix, the author will ALWAYS be the first column, as the distance between x and x is 0
                    authors = list(df.index.values)
                    f.writelines(f"{x},{authors.index('#TS#' + x)},")
    """
    with open("results.csv", "w") as f:
        for x in distances.columns:
            if x[:4] != "#TS#":
                df = distances[x]
                df = df.sort_values(ascending=True)
                df.drop(x, inplace=True) #In our correlation matrix, the author will ALWAYS be the first column, as the distance between x and x is 0
                authors = list(df.index.values)
                print(authors.index("#TS#" + x))
    """
if __name__ == "__main__":
    main()

#TS#