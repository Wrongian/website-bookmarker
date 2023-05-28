import shutil
from resources import app
import os.path
import hashlib

def backup():
    backup_path = app.config["BACKUP_FOLDER"]
    db_path = app.config["DB_LOCATION"] 
    max_backups = app.config["NUM_BACKUPS"]
    num_files = num_files_in_directory(backup_path)
    if os.path.exists(db_path):
        if num_files >= max_backups:
            #if too many backups, remove the oldest one
            list_of_files = os.listdir(backup_path)
            #get all the backups
            full_path = [backup_path+"/{0}".format(x) for x in list_of_files]
            #get the oldest file
            oldest_file = min(full_path, key=os.path.getctime)
            #remove it
            os.remove(oldest_file)
        #filename is sha1 hash of the file
        file_name = hash_file(db_path) + ".db" 
        #copy the db file
        shutil.copyfile(db_path,backup_path +"/" + file_name)
             
    else:
        print("DB not found, proceeding to not backup")

    
        
def restore_backup():
    pass

def num_files_in_directory(dir_path):
    count = 0
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path,path)):
            count+=1
    return count

def hash_file(file_path):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(file_path,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()
