from Drive_API_Wrapper import Drive

def main():
    gdrive = Drive(folder_id="1tnhjKsh_wmRg1wsL0AABumsqzpfP76G-")

    try:
        with open("checksum_backup.csv", "r") as backup:
            backup_str = backup.read()
            print(backup_str.split("\n"))
            if backup_str.split("\n")[-2] == "success" and input("This upload appears to have been successful, please type y if you are SURE you would like to continue (not reccomended): ").lower() != "y":
                quit()
        csv_id = gdrive.get_csv_id()
        current_file = gdrive.read_file(csv_id)
        checksum_string = current_file + backup_str
        gdrive.rewrite_file(csv_id, checksum_string)

        final_check = gdrive.read_file(csv_id)
        if final_check == checksum_string:
            print("Success!")
        elif final_check != current_file:
            print("Upload failed, and the original file is not intact")
        else:
            print("Upload failed, however the original file is intact")
    except FileNotFoundError:
        raise FileNotFoundError("No backup file could be found")

if __name__ == "__main__":
    main()

