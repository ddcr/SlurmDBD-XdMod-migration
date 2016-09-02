from framework.storage.mysql import MySQL
from pprint import pprint

class MySQLTest:
    
    @staticmethod
    def run():
        id = MySQL.next_id()
        shard = MySQL.get(id)
        
        result = shard.query("SELECT 2")
        
        pprint(result)
        
        result2 = shard.multi_query("SELECT 1 ",[(),(),(),()]);
        
        pprint(result2)

