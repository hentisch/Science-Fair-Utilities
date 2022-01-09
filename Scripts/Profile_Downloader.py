from re import sub
from PushshiftIO import PushshiftIO
import sys
from tqdm import tqdm
from Drive_API_Wrapper import Drive
from Karma_Correlation_Finder import Stats_File_Creator
from After_Time_Hash_Creator import get_hash_line

def main():
    try:
        stats_file = open(sys.argv[2], "a")
        print(sys.argv)
    except IndexError:
        try:
            stats_file = open("karma-length_stats.csv", "r")
            stats_file = open("karma-length_stats.csv", "a")
        except FileNotFoundError:
            print("No file found, creating new file")
            stats_file = open("karma-length_stats.csv", "w")
            stats_file.writelines("User,Comment Karma,Submission Karma,Total Words,Total Characters (not including spaces)\n")

    gdrive = Drive()
    profile_count = int(sys.argv[1])
    print("getting past files...")
    previous_accounts = set([x[:-4] for x in gdrive.list_file_names()])
    duplicate_accounts = 0
    checksum_string = ""
    checksum_backup = open("checksum_backup.csv", "w")

    print("Getting Random Users")
    subjects = PushshiftIO.get_random_users(profile_count)
    print("Getting Data For Selected Users")
    for x, y, z in tqdm(subjects):
        if not (x in previous_accounts):
            content = PushshiftIO.get_all_user_content(x)
            file_text = f"{x} {y} {z} \n {content}"
            gdrive.add_file(f"{x}.txt", file_text)
            stats_file.writelines(Stats_File_Creator.get_line(file_text))
            checksum_string += get_hash_line(file_text, x)
            checksum_backup.writelines(get_hash_line(file_text, x))
        else:
            duplicate_accounts += 1
    try:
        csv_id = gdrive.get_csv_id()
        checksum_string = gdrive.read_file(csv_id) + checksum_string
        gdrive.rewrite_file(csv_id, checksum_string)
    except IndexError:
        gdrive.add_file("checksums.csv", checksum_string)
    checksum_backup.writelines("success\n")
    print(f"Done! In total, {profile_count - duplicate_accounts} users were added.")

if __name__ == "__main__":
    main()
