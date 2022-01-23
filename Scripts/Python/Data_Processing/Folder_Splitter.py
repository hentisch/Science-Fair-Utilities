import os
import sys
from math import ceil
from tqdm import tqdm
import shutil as sh

def main():
    try:
        source_dir = sys.argv[1]
        split_dir = sys.argv[2]
        folder_len = int(sys.argv[3])
        print(f"Source directory: {source_dir}, split directory: {split_dir}, folder length: {folder_len}")
    except IndexError:
        print("Python3 Folder_Splitter.py <source_dir> <split_dir> <folder_len>")
        quit()
    users = []
    
    for file in os.listdir(source_dir):
        if file[:4] != "#TS#":
            users.append(file)
    
    for n in range(ceil(len(users)/folder_len)):
        os.mkdir(f"{split_dir}/corpus-{n+1}")

    for i, user in enumerate(tqdm(users)):
        sh.copyfile(f"{source_dir}/{user}", f"{split_dir}/corpus-{i//folder_len + 1}/{user}")
        sh.copyfile(f"{source_dir}/#TS#{user}", f"{split_dir}/corpus-{i//folder_len + 1}/#TS#{user}")

if __name__ == "__main__":
    main()