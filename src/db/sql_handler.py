import pyodbc
from src.db.db_functions import *


class SQLHandler:

    class __SQLHandler:

        def _init_(self):
            self.setProductionDb()

        def setProductionDb(self):
            try:
                self.server = '172.16.245.73' # Write here Ofek's IP IN just4visitors (and disable firewall)
                self.db_name = 'ecommerce'
                self.user_id = 'ecosql'
                self.password = 'ecosql'
                self.conn = 'DRIVER={SQL Server};SERVER=' + self.server + ';DATABASE=' \
                            + self.db_name + ';UID=' + self.user_id + ';PWD=' + self.password
            except Exception as e:
                print(e)

        def setTestDb(self):
            try:
                self.server = '172.16.0.75' # Write here Ofek's IP IN just4visitors (and disable firewall)
                self.db_name = 'test_ecommerce'
                self.user_id = 'test'
                self.password = 'test'
                self.conn = 'DRIVER={SQL Server};SERVER=' + self.server + ';DATABASE=' \
                            + self.db_name + ';UID=' + self.user_id + ';PWD=' + self.password
            except Exception as e:
                print(e)

        def update(self, update_operation):
            cnxn = pyodbc.connect(self.conn)
            cursor = cnxn.cursor()
            cursor.execute(update_operation)
            cnxn.commit()
            cnxn.close()

        def select_from_db(self, sql):
            cnxn = pyodbc.connect(self.conn)
            cursor = cnxn.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            arr = []
            while row:
                arr.append(row)
                row = cursor.fetchone()
            cnxn.commit()
            cnxn.close()
            return arr

    instance = None

    @staticmethod
    def get_instance():
        if not SQLHandler.instance:
            SQLHandler.instance = SQLHandler.__SQLHandler()
        return SQLHandler.instance
