from tqdm import tqdm
from Drive_API_Wrapper import Drive
from hashlib import sha256

def main():
    gdrive = Drive()

    with open("checksums.csv", "w") as checksum_file:
        for n, id in gdrive.list_files():
            checksum = sha256(gdrive.read_file(id)).hexdigest()
            checksum_file.writeline(f"{n},{checksum}")
        checksum_file.close()
    
    print("Done!")