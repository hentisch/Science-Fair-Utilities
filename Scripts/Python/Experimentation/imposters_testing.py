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
    raw_corpus = delta.Corpus(sys.argv[1], ngrams=2)
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
    for i, x in enumerate(distances.columns):
        if x[0][:4] != "#TS#":
            df = distances[x]
            df.sort_index(inplace=True, ascending=True)
            print(df.head(n=10))
            quit()
if __name__ == "__main__":
    main()

#TS#