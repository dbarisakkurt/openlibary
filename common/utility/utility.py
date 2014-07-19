import os
import ntpath


class FileOperation(object):
    @staticmethod
    def getFileSize(file_path):
        """Takes an absolute path of a file and returns its size in KB"""
        if os.path.isfile(file_path):
            size=os.path.getsize(file_path)
            if size<=1024:
                return 1.00
            kilo_size=size/1024.0
            return "{0:.2f}".format(kilo_size)
        else:
            return -1

    @staticmethod
    def getFileName(file_path):
        """return the file name of a given file path"""
        if os.path.isfile(file_path):
            return ntpath.basename(file_path)
        else:
            raise Exception("Error occured. This is not a file.")
    
    @staticmethod    
    def getCurrentFilesDirectoryName():
        """return the directory name of this file"""
        return os.path.dirname(os.path.realpath(__file__))

    @staticmethod
    def getFileType(file_name):
        """return file type of a given file name or path"""
        extension = os.path.splitext(file_name)[1][1:].lower()
        return extension

    @staticmethod
    def getFileDirectory(file_path):
        """return the directory name of a given file path"""
        if os.path.isfile(file_path):
            return os.path.dirname(os.path.realpath(file_path))
        else:
            raise Exception("Error occured. This is not a file.")
        
        
def getDropboxAppKeyAndSecret():
    """return the app key and app secret of dropbox from the file"""
    file_name='dropbox.txt'
    output=''
    with open(file_name, 'r') as my_file:
        output = my_file.read()
    key_list=output.split('|')
    return key_list