#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
from DBUtils.PooledDB import PooledDB

from srf_log import logger


class MySQLEngine(object):
    '''
    mysql engine
    '''
    __tablename__ = None
    placeholder = '%s'

    def connect(self, **kwargs):
        '''
        mincached : 启动时开启的空连接数量(缺省值 0 意味着开始时不创建连接)
        maxcached: 连接池使用的最多连接数量(缺省值 0 代表不限制连接池大小)
        maxshared: 最大允许的共享连接数量(缺省值 0 代表所有连接都是专用的)如果达到了最大数量，被请求为共享的连接将会被共享使用。
        maxconnections: 最大允许连接数量(缺省值 0 代表不限制)
        blocking: 设置在达到最大数量时的行为(缺省值 0 或 False 代表返回一个错误；其他代表阻塞直到连接数减少)
        maxusage: 单个连接的最大允许复用次数(缺省值 0 或 False 代表不限制的复用)。当达到最大数值时，连接会自动重新连接(关闭和重新打开)
        '''
        db_host = kwargs.get('db_host', 'localhost')
        db_port = kwargs.get('db_port', 3306)
        db_user = kwargs.get('db_user', 'root')
        db_pwd = kwargs.get('db_pwd', '')
        db = kwargs.get('db', '')

        self.pool = PooledDB(pymysql, maxconnections=5, mincached=1, maxcached=5, blocking=True, host=db_host,
                             user=db_user, passwd=db_pwd, db=db, port=db_port, charset='utf8')

        logger.info('''connect mysql db_host:%s db_port:%d db_user:%s 
            db_pwd:%s db:%s''', db_host, db_port, db_user, db_pwd, db)

    @staticmethod
    def escape(string):
        pass

    def _check_parameter(self, sql_query, values, req_id=None):
        count = sql_query.count('%s')
        if count > 0:
            for elem in values:
                if not elem:
                    if req_id:
                        logger.debug('req_id:%s sql_query:%s values:%s check failed',
                                     req_id, sql_query, values)
                    return False
        return True

    def _execute(self, sql_query, values=[], req_id=None):
        '''
        每次都使用新的连接池中的链接
        '''
        if not self._check_parameter(sql_query, values):
            return
        conn = self.pool.connection()
        cur = conn.cursor()
        cur.execute(sql_query, values)
        conn.commit()
        conn.close()
        return cur

    def select(self, sql_query, values=[], req_id=None):
        sql_query = sql_query.replace('\n', '')
        while '  ' in sql_query:
            sql_query = sql_query.replace('  ', ' ')
        if not self._check_parameter(sql_query, values, req_id):
            return
        cur = self._execute(sql_query, values, req_id)
        for row in cur:
            yield row

    def execute(self, sql_query, values=[], req_id=None):
        sql_query = sql_query.replace('\n', '')
        while '  ' in sql_query:
            sql_query = sql_query.replace('  ', ' ')
        cur = self._execute(sql_query, values)


sql_engine = MySQLEngine()

if __name__ == '__main__':
    pass
    # sql = 'select * from user_base where id > %s';
    # values = [10]
    # sql_engine.connect(db_host='localhost', db_port=3306, db_user='root', db_pwd='', 
    #     db='yingzhongtong_rc_jing')
    # for row in sql_engine.select(sql, values):
    #     print row
