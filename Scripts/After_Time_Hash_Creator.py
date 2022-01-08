from tqdm import tqdm
from Drive_API_Wrapper import Drive
from hashlib import sha256

def get_hash_line(content:str, name:str)-> str:
    return (f"{name},{sha256(content.encode('utf-8')).hexdigest()}\n")

def main():
    gdrive = Drive()
    file_str = ""
    print("Getting current list of files")
    for n, id in tqdm(gdrive.list_files()):
        checksum = sha256(gdrive.read_file(id).encode('utf-8')).hexdigest()
        file_str += (f"{n},{checksum} \n")
    gdrive.add_file("checksums.csv", file_str)
    print("Done!")

if __name__ == "__main__":
    main()