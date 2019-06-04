# -*- coding:utf-8 -*-

import itertools

class Connection:
    mysql = __import__('mysql.connector')

    def __init__(self, host, user = None, password = None, schema = None):

        if type(host) is not str:
            config = host
            host = config['host']
            user = config['user']
            password = config['password']
            schema = config['schema']

        self.conn = self.mysql.connector.connect(host=host, user=user, passwd=password, database=schema)
        self.db = self.conn.cursor(dictionary=True)
        self.db.execute("SET NAMES utf8mb4;")

    def get_sql(self, sql):
        self.db.execute(sql)
        return self.db.fetchall()

    def get_sql_with_placeholder(self, sql, data):
        self.db.execute(sql, data)
        return self.db.fetchall()

    def insert_sql_with_placeholder(self, sql, data):
        self.db.execute(sql, data)
        last_id = self.db.lastrowid
        self.conn.commit()
        return last_id

    def update_sql(self, sql):
        self.db.execute(sql)
        self.conn.commit()

    def update_sql_with_placeholder(self, sql, data):
        self.conn.start_transaction()
        results = self.db.execute(sql, data, multi=True)
        for cur in results:
            pass
        self.conn.commit()
        
    def delete_sql_with_placeholder(self, sql, data):
        self.db.execute(sql, data)
        self.conn.commit()

    def delete_sql(self, sql):
        self.db.execute(sql)
        self.conn.commit()

    def insert_sql(self, sql):
        self.db.execute(sql)
        lastID = self.db.lastrowid
        self.conn.commit()
        return lastID

    def get(self, table):
        self.db.execute("SELECT * FROM " + table)
        return self.db.fetchall()

    def getRow(self, table):
        self.db.execute("SELECT * FROM " + table + " LIMIT 1")
        return self.db.fetchone()


    def insert(self, table, data):
        sql = ("INSERT INTO " + table + ""
              " (`" + "`,`".join(data) + "`)"
              " VALUES (%(" + ")s, %(".join(data) + ")s) ")
        self.db.execute(sql, data)
        lastID = self.db.lastrowid
        self.conn.commit()
        return lastID

    def update(self, table, data, where):
        sql = ("UPDATE " + table +
                " SET " + ', '.join(['%s = %%(%s)s' % (key, key) for (key, value) in data.items()]) +
               " WHERE " + where)
        self.db.execute(sql, data)
        self.conn.commit()

    def exec(self, sql, data):
        self.db.execute(sql, data)
        lastID = self.db.lastrowid
        self.conn.commit()
        return lastID
        
    def close(self):
        self.db.close()
        self.conn.close()


    def __str__(self):
        return 'OK'

