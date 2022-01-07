from tqdm import tqdm
from Drive_API_Wrapper import Drive
from hashlib import sha256

def main():
    gdrive = Drive(folder_id="1tnhjKsh_wmRg1wsL0AABumsqzpfP76G-")
    file_str = ""
    for n, id in gdrive.list_files():
        checksum = sha256(gdrive.read_file(id).encode('utf-8')).hexdigest()
        file_str += (f"{n},{checksum} \n")
    gdrive.add_file("checksums.txt", file_str)
    print("Done!")

if __name__ == "__main__":
    main()