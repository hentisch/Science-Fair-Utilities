from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class Drive:

    def __init__(self, folder_id:str = "1OMT-9fS3y3uuc-9WVGs6lYf-83fKbcFE") -> None:
        self.gauth = GoogleAuth()
        self.gauth.CommandLineAuth()
        self.folder_id = folder_id
        #This whole proccess will force the user to login with Google O-Auth
        self.drive = GoogleDrive(self.gauth) 
    
    def add_file(self, title:str, content:str) -> None:
        file1 = self.drive.CreateFile({'title': title, 'parents': [{'id': self.folder_id}]})  # Create GoogleDriveFile instance with title 'Hello.txt'.
        #TODO figure out a more dynamic way to do file paths from PyDrive
        file1.SetContentString(content) # Set content of the file from given string.
        file1.Upload()
    
    def list_files(self) -> list:
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % self.folder_id}).GetList()
        return [x["originalFilename"] for x in file_list]

if __name__ == "__main__":
    cool = Drive()
    print(len(cool.list_files()))