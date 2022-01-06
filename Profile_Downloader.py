from re import sub
from PushshiftIO import PushshiftIO
import sys
from tqdm import tqdm
from Drive_API_Wrapper import Drive

google_drive_storage = Drive()
profile_count = int(sys.argv[1])
previous_accounts = set([x[:-4] for x in google_drive_storage.list_files()])
duplicate_accounts = 0

print("Getting Random Users")
subjects = PushshiftIO.get_random_users(profile_count)
print("Getting Data For Selected Users")
for x, y, z in tqdm(subjects):
    if not (x in previous_accounts):
        content = PushshiftIO.get_all_user_content(x)
        google_drive_storage.add_file(f"{x}.txt", f"{x} {y} {z} \n {content}")
    else:
        duplicate_accounts += 1
print(f"Done! In total, {profile_count - duplicate_accounts} users were added.")