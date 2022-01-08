import hashlib
import sys #cli paramater is the number of files to split into
import os

def get_file_length(file_name:str) -> int:
    sum = 0
    with open(file_name, "r") as file:
        for line in file:
            sum += 1
    return sum 

def main():
    checksum_file = open("checksum.txt", "r")
    users_file = open("69M_reddit_accounts.csv", "r")

    hash = hashlib.sha256(users_file.read().encode('utf-8')).hexdigest()

    if hash == checksum_file.readlines()[0].split()[1]:
        print("Users file verified")
    else:
        print("Could not verify master file, please redownload")
        quit()

    users_file_length = get_file_length("69M_reddit_accounts.csv")
    if ((users_file_length - 2) % int(sys.argv[1][1:])) != 0:
        print("The number of lines in the file is not divisible by the number of files")
        quit()

    file_length = (users_file_length-2) // int(sys.argv[1][1:])

    file_arr = []
    for x in range(int(sys.argv[1][1:])):
        file_arr.append(open(f"/home/henry/Documents/Code/Open Source/Science-Fair-Utilities/Split_Reddit_Accounts/SplitFiles/Reddit_Accounts_{x}.txt", "w"))
        
    everythingString = ""
    with open("69M_reddit_accounts.csv", "r") as users_file:
        for i, line in enumerate(users_file):
            if i <= 2:
                everythingString += line + "\n"
            else:
                file_arr[ (i-2) // file_length ].writelines(line + "\n")

    for x in file_arr:
        x.close()
        
    checksum_dict = {}
    last_length = 0
    for i, x in enumerate(os.listdir(os.path.realpath("/home/henry/Documents/Code/Open Source/Science-Fair-Utilities/Split_Reddit_Accounts/SplitFiles/"))):
        checksum_dict[x] = hashlib.sha256(open("/home/henry/Documents/Code/Open Source/Science-Fair-Utilities/Split_Reddit_Accounts/SplitFiles/" + x, "r").read().encode('utf-8')).hexdigest()
        everythingString += open("/home/henry/Documents/Code/Open Source/Science-Fair-Utilities/Split_Reddit_Accounts/SplitFiles/" + x, "r").read()
        length = get_file_length("/home/henry/Documents/Code/Open Source/Science-Fair-Utilities/Split_Reddit_Accounts/SplitFiles/" + x)
        """
        if i > 0 and length != last_length:
            print("The files are not the same length")
            quit()
        """
        last_length = length

    if hash == hashlib.sha256(everythingString[:-3].encode('utf-8')).hexdigest():
        print("Checksum verified, database has been correctly split") 
    else:
        print("Checksum failed, this program has not correctly split the database")
        quit()
    
    with open("checksum.txt", "w") as checksum_file:
        for x in checksum_dict:
            checksum_file.writelines(f"{x} {checksum_dict[x]}\n")


if __name__ == "__main__":
    main()