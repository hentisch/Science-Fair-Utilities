from PushshiftIO import PushshiftIO
import sys
from tqdm import tqdm
trials = int(sys.argv[1])
accounts = []
try:
    open("final_results.csv", "r")
except FileNotFoundError:
    print("Getting Random Users")
    subjects = PushshiftIO.get_random_users(trials)
    with open("final_results.csv", "w") as final_results:
        final_results.writelines("User,Comment Karma,Submission Karma,Total Words,Total Characters (not including spaces)\n")
        print("Getting Data For Selected Users")
        for x, y, z in tqdm(subjects):
            content = PushshiftIO.get_all_user_content(x)
            words_list = content.split()
            character_count = 0
            for a in words_list:
                character_count += len(a)
            final_results.writelines(x + "," + str(y) + "," + str(z) + "," + str(len(words_list)) + "," + str(character_count) + "\n")
        print("Done!")