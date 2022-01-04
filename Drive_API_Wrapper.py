from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class Drive:

    def __init__(self) -> None:
        self.gauth = GoogleAuth()
        self.gauth.CommandLineAuth()
        #This whole proccess will force the user to login with Google O-Auth
        self.drive = GoogleDrive(self.gauth) 
    
    def add_file(self, title:str, content:str) -> None:
        file1 = self.drive.CreateFile({'title': title, 'parents': [{'id': "1UAU1DdvV9QiFV8GY1MOT0jL-NJiz-XlL"}]})  # Create GoogleDriveFile instance with title 'Hello.txt'.
        #TODO figure out a more dynamic way to do file paths from PyDrive
        file1.SetContentString(content) # Set content of the file from given string.
        file1.Upload()

if __name__ == "__main__":
    cool = Drive()