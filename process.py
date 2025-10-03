import asyncio

from api.index import create_index
from api.query import search, multisearch


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