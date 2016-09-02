import sys
from framework.storage.mysql import MySQL
from framework.storage.mysql_pool import MySQLPool
from multiprocessing import Pool
from pprint import pprint

sql_file_name = sys.argv[1]
try:
    pool_id = sys.argv[2]
except IndexError:
    pool_id = MySQLPool.MAIN
    
pool = MySQL.get_pool(pool_id)

try:
    num_threads = sys.argv[3]
except IndexError:
    num_threads = None


def get_query_string(file_name):
   with open('sql/' + file_name) as data_file:
       return data_file.read()
   
 
def get_query_runner(pool, query_str):
    # bind pool and query string to a function
    # that can make a query per shard id  
    def run_one_query(shard_id):
        shard = pool.get_shard(shard_id)
        query_res = shard.query(query_str, None, True)
        shard.close() 
        return query_res
    
    return run_one_query
    

run_one_query = get_query_runner(pool, get_query_string(sql_file_name) ) 

res = []
with Pool(num_threads) as p:
    res = p.map(run_one_query, range(pool.get_num_shards()))



pprint(res)
