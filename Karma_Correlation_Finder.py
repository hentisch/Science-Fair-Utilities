import sys
from tqdm import tqdm
import os
#This file will take all of the txt files in the directory and create the spreadsheet from that
try:
    open("final_results.csv", "r")
except FileNotFoundError:
    with open("final_results.csv", "w") as final_results:
        final_results.writelines("User,Comment Karma,Submission Karma,Total Words,Total Characters (not including spaces)\n")
        user_files = os.listdir(sys.argv[1])
        for f in tqdm(user_files):
            with open(sys.argv[1] + f, "r") as user_file:
                print(f"Currently working on: {sys.argv[1]}{f}")
                content = user_file.read()
                body = content[content.index("\n") + 1:]
                x, y, z = content[:content.index("\n")-1].split(" ")[0], content[:content.index("\n")-1].split(" ")[1], content[:content.index("\n")-1].split(" ")[2]
                #print(body)
                #print(x, y, z)
                #print(content[:content.index("\n")-1])
                #FIXME THIS SHIT IS EMPTY
                words_list = content.split()
                final_results.writelines(x + "," + str(y) + "," + str(z) + "," + str(len(words_list)) + "," + str(len(content)-len(words_list)) + "\n")
                user_file.close()
        print("Done!")

#max.txt