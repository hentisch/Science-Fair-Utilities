from ast import arg
import sys
import os
from tqdm import tqdm

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
        character_limit = int(sys.argv[2]) #we want to run this first so that any index error is detected before the file is opened
        all_files = os.listdir(sys.argv[3])
    except IndexError:
        print("Python3 Local_Corpus_Preperation.py -c/w <minimum_count> <path to directory>")
    except FileNotFoundError:
        print(f"Could not find directory {sys.argv[2]}")

    for x in tqdm(all_files):
        if x[-3:] != "txt" or file_length(x, mode) < character_limit:
            os.remove(f"{sys.argv[3]}/{x}")
        else:
            with open(f"{sys.argv[3]}/{x}", "r") as f:
                content = f.read()
            with open(f"{sys.argv[3]}/{x}", "w") as f:
                f.write(content[content.index("\n")+1:])

if __name__ == "__main__":
    main()