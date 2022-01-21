from csv import excel
import delta
import sys
import pandas as pd
#http://dev.digital-humanities.de/ci/job/pydelta-next/Documentation/GettingStarted.html
def truncate_collumns(sheet, n:int):
    for i, x in enumerate(sheet.columns):
        if i+1 > n:
            sheet.drop(x, axis=1, inplace=True)
    return sheet

def main():
    try:
        raw_corpus = pd.read_csv("distances.csv", index_col=0)
    except FileNotFoundError:
        raw_corpus = delta.Corpus(sys.argv[1], ngrams=2) #As this is the most computationally instensive step, we only want to do it once
        raw_corpus.to_csv("distances.csv")
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