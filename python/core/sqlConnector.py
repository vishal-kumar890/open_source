import apsw,threading
import os, traceback
import logging
from ..config import settings, UserError
from ..pdModels.dbModel import user_db
from celery import Celery


logger = logging.getLogger(__name__)

broker_url = settings.celery_url
celery_app = Celery('tasks', broker=broker_url, backend='redis://')

connector = {}

class sccCursor():
    def __init__(self, conn, dbtype, id):
        self.conn = conn
        self.dbtype = dbtype
        self.id = id

            
    def execute(self, query, args=tuple()):
        try:
            self.conn.execute(query, args)
        except Exception as ex:
            print(query)
            raise ex
        # new_query = query_parser(query, self.dbtype)
        # self.conn.execute(new_query, args)
        return self.conn
    

    def rollback(self,rollback_name):
        self.conn.execute(f"rollback to {rollback_name}")

    def rowcount(self):
        count_query = "SELECT CHANGES()"
        self.conn.execute(count_query)    
        return self.conn.fetchone()[0]
        
    def intermediate_commit(self):
        try:
            self.conn.execute("COMMIT")
            self.conn.execute("BEGIN")
        except Exception as ex:
            raise Exception(f"Error occured {ex}")
    
        
    

class sqlConnect():
    def __init__(self):
        db_model = user_db(**settings.dict())
        self.db_type = db_model.db_type
        self.cursor = get_mysql_cursor(db_model)
        self.db_id = db_model.db_id

    def __enter__(self): 
        try:
            self.cursor.execute("BEGIN")
        except apsw.SQLError:
            self.cursor.execute("ROLLBACK")
            self.cursor.execute("BEGIN")
        return sccCursor(self.cursor, self.db_type, self.db_id)


    def __exit__(self, exception_type, exception_value, traceback_val):
        if exception_type:
            logger.error(f"some error happened {self.db_id} {exception_type} {exception_value} {str(traceback_val)}")
            logger.error(f"{traceback.format_exc()}")
            try:
                self.cursor.execute("ROLLBACK")
            except:
                pass
            self.cursor.close()
            raise UserError(str(exception_value))
        else:
            self.cursor.execute("COMMIT")
            self.cursor.close()
            
            


def init_db(db_model):
    try:        
        if not os.path.isfile(db_model.db_name):
            raise UserError(f"DBFile Doesn't exists in system, {db_model.db_name}")

        conn = apsw.Connection(db_model.db_name)

        conn.setbusytimeout(12000)
        # conn.cursor().execute("PRAGMA temp_store =  MEMORY")
            
        return conn
    except:        
        raise UserError("DataBase Doesn't exists in system")
apsw.SQLITE_OPEN_URI


def get_mysql_cursor(db_model):
    tid = str(threading.get_ident())
    db_id = str(db_model.db_id)
    if db_id in connector and tid in connector[db_id]:
        connection = connector[db_id][tid]
        if connection:
            return connection.cursor()
        
    
    connection = init_db(db_model)

    if db_id in connector:
        connector[db_id][tid] = connection
    else:
        connector[db_id] = {tid: connection}
    
    return connection.cursor()
