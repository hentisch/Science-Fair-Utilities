import pickle as pkl
import delta
import sys

def main():
    try:
        with open(sys.argv[3], "wb") as f:
            corpus = delta.Corpus(sys.argv[1], ngrams=int(sys.argv[2]))
            trimmed_corpus = corpus.cull(1/3)
            pkl.dump(trimmed_corpus)
    except IndexError:
        print("Python3 create_single_feature_matrix.py <path to corpus> <ngram count> <final file>")
        quit()

if __name__ == "__main__":
    main()
    