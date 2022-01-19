from ast import arg
import sys
import os
from tqdm import tqdm
import random

def file_length(file_path:str, mode:str="character") -> int:
    with open(f"{sys.argv[3]}/{file_path}", "r") as f:
        if mode == "character":
            return len(f.read())
        elif mode == "word":
            return len(f.read().split())
        else:
            raise ValueError("mode must be either 'character' or 'word'")

def main():
    try:
        if sys.argv[1] == "-c":
            mode = "character"
        elif sys.argv[1] == "-w":
            mode = "word"
        else:
            print(f"Could not recognize mode \"{sys.argv[1]}\", defaulting to 'character'")
            mode = "character"
        element_limit = int(sys.argv[2]) #we want to run this first so that any index error is detected before the file is opened
        all_files = os.listdir(sys.argv[3])
    except IndexError:
        print("Python3 Local_Corpus_Preperation.py -c/w <minimum_count> <path to directory>")
    except FileNotFoundError:
        print(f"Could not find directory {sys.argv[2]}")

    for x in tqdm(all_files):
        if x[-3:] != "txt" or file_length(x, mode) < element_limit:
            os.remove(f"{sys.argv[3]}/{x}")
        else:
            with open(f"{sys.argv[3]}/{x}", "r") as f:
                content = f.read()
                units = [i for i in content.split("\n") if i != ""] 
                units.pop(0) #This is the heading line with name, comment karma and submission karma

                test_set = "" #This will be the smaller, genuine element we are trying to verify authorship of
                refrence_set = "" #This will be the set for which each user will be "competing" to match

                while len(test_set.split()) < len(content.split())*0.25: #TODO implement this to also work with characters if you seleect the -c flag
                    element = random.randint(0, len(units) - 1)
                    test_set += units[element] + "\n\n"
                    units.pop(element)
                for u in units:
                    refrence_set += u + "\n\n"
            with open(f"{sys.argv[3]}/{x}", "w") as f:
                f.write(refrence_set)      
            with open(f"{sys.argv[3]}/#TS#{x}", "w") as f:
                f.write(test_set)

if __name__ == "__main__":
    main()