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
    
    def rewrite_file(self, id, content):
        file = self.drive.CreateFile({'id': id})
        file.SetContentString(content)
        file.Upload()

    def delete_file(self, id:str):
        file = self.drive.CreateFile({'id': id})
        file.Trash()
        file.UnTrash()
        file.Delete()
    
    def list_file_names(self, txt_only = True) -> list:
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % self.folder_id}).GetList()
        return [x["title"] for x in file_list if x["title"][-3] == "txt" or not txt_only]
    
    def list_file_ids(self, txt_only=True) -> list:
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % self.folder_id}).GetList()
        return [x["id"] for x in file_list if x["title"][-3:] == "txt" or not txt_only]
    
    def list_files(self, txt_only=True) -> list:
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % self.folder_id}).GetList()
        return [ (x["title"], x["id"]) for x in file_list if x["title"][-3:] == "txt" or not txt_only]
    
    def list_files_debug(self) -> list:
        return self.drive.ListFile({'q': "'%s' in parents and trashed=false" % self.folder_id}).GetList()
    
    def read_file(self, id) -> str:
        file = self.drive.CreateFile({'id': id})
        return file.GetContentString()

    def get_csv_id(self) -> str:
        file_list = self.drive.ListFile({'q': "'%s' in parents and trashed=false" % self.folder_id}).GetList()
        return [x["id"] for x in file_list if x["title"][-3:] == "csv"][0]

if __name__ == "__main__":
    gdrive = Drive(folder_id="1tnhjKsh_wmRg1wsL0AABumsqzpfP76G-")
    print(gdrive.list_file_names())
