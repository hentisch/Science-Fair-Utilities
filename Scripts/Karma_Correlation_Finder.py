import sys
from tqdm import tqdm
import os
from Drive_API_Wrapper import Drive

#This file will take all of the txt files in the directory and create the spreadsheet from that
class Stats_File_Creator:
        @staticmethod
        def get_line(content:str):
                body = content[content.index("\n") + 1:]
                x, y, z = content[:content.index("\n")].split(" ")[0], content[:content.index("\n")].split(" ")[1], content[:content.index("\n")].split(" ")[2]
                words_list = body.split()
                return (x + "," + str(y) + "," + str(z) + "," + str(len(words_list)) + "," + str(len(body.replace("\n", ""))) + "\n")

def main():
        gdrive = Drive(folder_id="1tnhjKsh_wmRg1wsL0AABumsqzpfP76G-")

        with open("final_results.csv", "w") as final_results:
                print(gdrive.list_file_ids())
                print(gdrive.list_file_names())
                final_results.writelines("User,Comment Karma,Submission Karma,Total Words,Total Characters (not including spaces)\n")
                for id in tqdm(gdrive.list_file_ids()):
                        content = gdrive.read_file(id)
                        final_results.writelines(Stats_File_Creator.get_line(content))
        print("Done!")

if __name__ == "__main__":
        main()