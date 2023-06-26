import traceback, threading, apsw, os

connector = {}


class UserError(Exception):
    message: str

    def __init__(self, msg):
        self.message = msg


class sqlConnect():
    def __init__(self, db_model: str):
        self.cursor = get_cursor(db_model)
        self.db_id = db_model

    def __enter__(self):
        self.cursor.execute("begin")
        return sccCursor(self.cursor, self.db_id)

    def __exit__(self, exception_type, exception_value, traceback_val):
        if exception_type:
            print(f"some error happened {exception_type} {exception_value} {str(traceback_val)}")
            traceback.print_exc()
            self.cursor.execute("ROLLBACK")
            self.cursor.close()
        else:
            try:
                self.cursor.execute("COMMIT")
                self.cursor.close()
            except apsw.CursorClosedError:
                pass
            except Exception as ex:
                print(f"again error occured {ex}")
                self.cursor.close()
                raise Exception(f"Error occured {ex}")


class sccCursor():
    def __init__(self, conn, id):
        self.conn = conn
        self.id = id

    def execute(self, query, args=tuple()):
        try:
            self.conn.execute(query, args)
        except Exception as ex:
            print(query)
            raise ex
        return self.conn

    def intermediate_commit(self):
        try:
            self.conn.execute("COMMIT")
            self.conn.execute("BEGIN")
        except Exception as ex:
            raise Exception(f"Error occured {ex}")

    def checkTableExists(self, tablename):
        query = f'select 1 from [{tablename.lower()}]'
        try:
            self.conn.execute(query)
        except:
            return False
        return True


def get_cursor(db_model):
    tid = threading.get_ident()
    if db_model in connector and tid in connector[db_model]:
        connection = connector[db_model][tid]
        return connection.cursor()

    connection = init_db(db_model)

    if db_model in connector:
        connector[db_model][tid] = connection
    else:
        connector[db_model] = {tid: connection}
    return connection.cursor()


def init_db(db_model):
    if not os.path.isfile(db_model):
        raise UserError("DBFile Doesn't exists in system")
    conn = apsw.Connection(db_model)
    conn.setbusytimeout(12000)
    conn.cursor().execute("PRAGMA journal_mode=WAL")
    return conn


def remove_connection_object(id):
    tid = threading.get_ident()
    if id in connector:
        if tid in connector[id]:
            conn = connector[id][tid]
            conn.close()
        del connector[id][tid]
