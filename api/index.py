import sys
import threading
sys.path.insert(0,'D:\yangliu\python_project\graphRAG')
from multiprocessing import Process
import asyncio
import os
from pathlib import Path
from graphrag.api.index import build_index
from graphrag.config.load_config import load_config

import shutil
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH')
TEMPLATE_PATH = os.getenv('TEMPLATE_PATH')
TIKTOKEN_PATH = os.getenv('TIKTOKEN_PATH')
def create_database(database_name:str):
    
    if os.path.exists(os.path.join(DATABASE_PATH,database_name)):
        return "database already exist"
    # 复制目录及其所有内容
    shutil.copytree(TEMPLATE_PATH, os.path.join(DATABASE_PATH,database_name))
    return 'success'

async def create_index(database_name:str):
    os.environ['TIKTOKEN_CACHE_DIR'] = r'D:\yangliu\python_project\graphRAG\openai_api\tiktoken'
    root_path = os.path.join(DATABASE_PATH,database_name)
    if not os.path.exists(root_path):
        return "database not exist"
    os.chdir(root_path)
    try:
        await build_index(config=load_config(root_dir=Path(root_path)))
        return 'success'
    except Exception as e:
        raise e
    

def get_database_list():
    database_name_list = os.listdir(DATABASE_PATH)
    return database_name_list
def delete_database(database_name):
    root_path = os.getenv('DATABASE_PATH')
    del_path = os.path.join(root_path, database_name)
    if not os.path.exists(del_path):
        return 'unknown path:'+del_path
    shutil.rmtree(del_path)
    return 'success'

if __name__ == '__main__':
    # create_database('数字人2000')
    # os.environ['TIKTOKEN_CACHE_DIR'] = r'D:\yangliu\python_project\graphRAG\openai_api\tiktoken'
    asyncio.run(create_index('security_manager')) 
