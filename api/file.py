import os
from pathlib import Path
import sys

sys.path.insert(0,'D:\yangliu\python_project\graphRAG')
from tools.file_excutor import extract_local_file_list
from dotenv import load_dotenv
load_dotenv()
DATABASE_PATH = os.getenv('DATABASE_PATH')

def get_file_list(database_name:str):
    root_path = os.path.join(DATABASE_PATH, database_name)
    if not os.path.exists(root_path):
        return 'unknown database:' + database_name
    input_path = os.path.join(root_path,'input')
    file_name_list = [Path(i).stem for i in os.listdir(input_path)]
    return file_name_list

def upload_local_file(dir_path = None, file_list = None, database_name:str = None,window_size = None):
    if file_list == None:
        file_list = os.listdir(dir_path)
 
        file_list = [os.path.join(dir_path,i) for i in file_list]

    return extract_local_file_list(file_path_list=file_list, database_name=database_name, window_size=window_size)

def delete_file_with_list(file_list, database_name):
    
    input_path = os.path.join(DATABASE_PATH, database_name, 'input')
    for file_name in file_list:
        del_path = os.path.join(input_path, file_name)
        if os.path.isfile(del_path):
            os.remove(del_path)
        else:
            return 'invalid path:' + del_path
    return 'success'

if __name__ == '__main__':
    url = r''
    # file_list = [r'D:\yangliu\data\nikon老师傅\08 FX67S2-RF-FUNC-A10-E1.pdf']
    rs = upload_local_file(dir_path=url,database_name='security_manager')
    print(rs)