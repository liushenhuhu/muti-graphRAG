import asyncio
import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from api.index import create_database, create_index, get_database_list, delete_database
from api.query import search,multisearch
from api.file import upload_local_file, delete_file_with_list,get_file_list
from concurrent.futures import ProcessPoolExecutor 
app = Flask(__name__)
CORS(app,origins='*')
load_dotenv()

executor = ProcessPoolExecutor(max_workers=10) 

def create_index_process(*args): 
    try:
        rs = asyncio.run(create_index(*args))
    except Exception as e:
        print(e)
        raise SystemExit(0) 
    return rs

def local_search_process(*args): 
    try:
        rs = asyncio.run(search(*args))
    except Exception:
        raise SystemExit(0)
    return rs
def multi_local_search_process(*args): 
    try:
        rs = asyncio.run(multisearch(*args))
    except Exception:
        raise SystemExit(0)
    return rs

@app.route('/')
def index():
    """
    返回可调用工具列表
    """
    routes = []
    for rule in app.url_map.iter_rules():
        if 'static' in rule.endpoint:
            continue
        routes.append(str(rule))

    # 返回JSON格式的路由信息
    return jsonify(routes)

@app.route('/',methods = ['GET'])
def get_db_list():
    """
    获取所有数据库名称
    """
    return jsonify(get_database_list())

@app.route('/create_database',methods = ['POST'])
def create_db():
    """
    创建并初始化数据库
    """
    database_name = request.json.get('database_name')

    return jsonify(create_database(database_name))

@app.route('/delete_database',methods = ['POST'])
def delete_db():
    """
    删除数据库
    """
    database_name = request.json.get('database_name')

    return jsonify(delete_database(database_name))

@app.route('/list_file',methods = ['POST'])
def get_files():
    """
    获取数据库下文件列表
    """
    database_name = request.json.get('database_name')
    return jsonify(get_file_list(database_name))

@app.route('/upload_file',methods = ['POST'])
def upload_files():
    """
    上传文件（实质为获取本地或公档文件并转换为txt存入数据库）
    """
    database_name = request.json.get('database_name')
    file_dir = request.json.get('file_dir') if 'file_dir' in request.json else None
    file_list = request.json.get('file_list') if 'file_list' in request.json else None
    window_size = request.json.get('window_size') if 'window_size' in request.json else None
    print(file_list)
    return jsonify(upload_local_file(dir_path=file_dir,file_list=file_list,database_name=database_name,window_size=window_size))

@app.route('/delete_file',methods = ['POST'])
def delete_files():
    """
    批量删除文件
    输入为数据库名称和文件名称
    """
    database_name = request.json.get('database_name')
    file_list = request.json.get('file_list')
    if not isinstance(file_list, list):
        return 'input should be list'
    return jsonify(delete_file_with_list(file_list, database_name))

@app.route('/create_graph',methods = ['POST'])
def create_graph(): 
    """
    指定数据库建立图谱
    """
    begin =datetime.datetime.now()
    try:
        database_name = request.json.get('database_name')
        future = executor.submit(create_index_process, database_name)
        result = future.result()
    except Exception as e:
        print(e)
        return jsonify('failed,please try again')
    end =datetime.datetime.now()
    return jsonify('success, spend time:'+str(end-begin))

@app.route('/quick_create_graph',methods = ['POST'])
def quick_create_graph():
    """
    创建数据库+上传数据+创建图谱
    """
    begin =datetime.datetime.now()
    try:
        database_name = request.json.get('database_name')
        file_dir = request.json.get('file_dir') if 'file_dir' in request.json else None
        file_list = request.json.get('file_list') if 'file_list' in request.json else None
        window_size = request.json.get('window_size') if 'window_size' in request.json else None
    
        create_database(database_name)
        upload_local_file(dir_path=file_dir,file_list=file_list,database_name=database_name,window_size=window_size)
        future = executor.submit(create_index_process, database_name) 
        result = future.result()
    except Exception as e:
        print(e)
        return jsonify('failed,please try again')
    end =datetime.datetime.now()
    return jsonify('success, spend time:'+str(end-begin))

@app.route('/local_search',methods = ['POST'])
def local_search():
    database_name = request.json.get('database_name')
    query = request.json.get('query')
    
    if isinstance(database_name,list):
        future = executor.submit(multi_local_search_process, database_name,query) 
    else:
        future = executor.submit(local_search_process, database_name,query) 
    result = future.result()
    for key in result[1].keys():
        result[1][key] = result[1][key].to_dict(orient='records')
    return jsonify({'content':result[0],
                    'source':result[1]})


# @app.route('/local_search_stream',methods = ['POST'])
# def local_search_stream():
#     request.json.get('database_name')
#     return jsonify()
# @app.route('/global_search',methods = ['POST'])
# def global_search():
#     request.json.get('database_name')
#     return jsonify()
# @app.route('/global_search_stream',methods = ['POST'])
# def global_search_stream():
#     request.json.get('database_name')
#     return jsonify()
# @app.route('/prompt_tuning',methods = ['POST'])
# def prompt_tuning():
#     request.json.get('database_name')
#     return jsonify()

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5001,threaded = True) # graphrag未知原因无法多线程

