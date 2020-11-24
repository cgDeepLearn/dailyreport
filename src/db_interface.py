# -*- coding: utf-8 -*-

import config
from utils import mysql_tools


class DBInterface(object):
    def __init__(self):
        self.db1_check = mysql_tools.MySQLEngine()
        self.db1_check.connect(db_host=config.db1_host,
                               db_port=config.db1_port,
                               db_user=config.db1_user,
                               db_pwd=config.db1_pwd,
                               db=config.db1_db)

        self.db2_check = mysql_tools.MySQLEngine()
        self.db2_check.connect(db_host=config.db2_host,
                               db_port=config.db2_port,
                               db_user=config.db2_user,
                               db_pwd=config.db2_pwd,
                               db=config.db2_db)


db_interface = DBInterface()

if __name__ == '__main__':
    pass
