import sys
import os
from tqdm import tqdm

writing_length = {}
with open(sys.argv[1], "r") as lengths_file:
    raw_data = lengths_file.readlines()
    for x in raw_data:
        user_attributes = x.split(",")
        writing_length[user_attributes[0]] = user_attributes[3]

def add_lengths(original_file:str, corpus):
    with open(original_file, "r") as data_file:
        raw_data = data_file.readlines()
        raw_data[0] = raw_data[0][:-1] + ",writing_length" + "\n"
        for i, x in enumerate(raw_data[1:]):
            try:
                raw_data[i+1] = x[:-1] + "," + writing_length[x.split(",")[0]] + "\n"
            except KeyError:
                with open(corpus + "/" + x.split(",")[0] + ".txt", "r") as f:
                    words = len(f.read().split())
                    raw_data[i+1] = x[:-1] + "," + str(words) + "\n"
        
    with open(original_file + "results_with_length.csv", "w") as data_file:
        data_file.writelines(raw_data)

def main():
    if "-r" in sys.argv:
        for x in tqdm(os.walk(sys.argv[2])):
            try:
                if x[2][0].endswith(".csv"):
                    add_lengths(x[0]+ "/" + x[2][0], sys.argv[3])
            except IndexError:
                pass
    else:
        try:
            add_lengths(sys.argv[2], sys.argv[3])
            print("Done!")
        except IndexError:
            print("Usage: python3 words_adder.py <lengths_file> <data_file> <corpus_file>")

if __name__ == "__main__":
    main()