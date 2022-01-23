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

def main():
    try:
        os.listdir(f"feature-matrices({sys.argv[2]}-gram)") # This just checks if the directory exists, TODO implment the tests to run on each matrix
        with open("distances.pickle", "rb") as f:
            print("Feature matrix found, loading...")
            raw_corpus = pkl.load(f)
    except FileNotFoundError:
        print("Feature matrices not found, creating...")
        try:
            os.mkdir(f"feature-matrices({sys.argv[2]}-gram)")
        except FileExistsError:
            pass
        current_progress = len(os.listdir(f"feature-matrices({sys.argv[2]}-gram)"))
        with tqdm(total=len(os.listdir(sys.argv[1])), initial=current_progress) as pbar:
            for i, x in enumerate(sorted(os.listdir(sys.argv[1]), key=lambda x: int(x[x.index("-"):]), reverse=True)):
                raw_corpus = delta.Corpus(sys.argv[1] + "/" + x, ngrams=2) #As this is the most computationally instensive step, we only want to do it once
                trimmed_corpus = raw_corpus.cull(1/3)
                with open(f"feature-matrices({sys.argv[2]}-gram)/distances-{i+1}.pickle", "wb") as f:
                    pkl.dump(trimmed_corpus, f)
                tqdm.update(1)
                print(x)
                pbar.update(1)
    except IndexError:
        print("Python3 imposterts_testing.py <path to directory> <ngram count> -c/none")
        quit()
    
    try:
        if sys.argv[3] == "-c":
            quit()
    except IndexError:
        pass

    #This corpus is, in practice, a pandas dataframe that we can view and manipulate
    culled_corpus = raw_corpus.cull(1/3)
    print(culled_corpus.shape)
    culled_corpus = truncate_collumns(culled_corpus, 100)
    print(culled_corpus.shape)
    print(culled_corpus.head(10))
    print("-----------------------------------------------------")
    distances = delta.functions.cosine_delta(culled_corpus) #NOTE COSINE DELTA IS THE DISTANCE, NOT THE SIMILARITY
    print(distances.shape)
    print(distances.head(n = 34))
    with open("results.csv", "w") as f:
        for x in distances.columns:
            if x[:4] != "#TS#":
                df = distances[x]
                df = df.sort_values(ascending=True)
                df.drop(x, inplace=True) #In our correlation matrix, the author will ALWAYS be the first column, as the distance between x and x is 0
                authors = list(df.index.values)
                print(authors.index("#TS#" + x))
if __name__ == "__main__":
    main()

#TS#