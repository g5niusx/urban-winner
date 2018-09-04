import sqlite3


# 数据库操作
class DBHandler(object):

    def __init__(self, db_name):
        self.db_name = db_name
        pass

    # 初始化表
    def init_table(self):
        connect = sqlite3.connect(self.db_name)
        connect_cursor = connect.cursor()
        connect_cursor.execute('create table if not exists tbl_url (url varchar(200))')
        connect_cursor.close()
        connect.commit()
        print('数据库创建完毕...')

    # 将一个地址插入到数据库
    def insert(self, _url):
        _connect = sqlite3.connect(self.db_name)
        _connect_cursor = _connect.cursor()
        sql = 'insert into tbl_url (url) values (\'%s\')' % _url
        _connect_cursor.execute(sql)
        _connect_cursor.close()
        _connect.commit()
        print('[%s]插入到数据库成功!' % _url)

    # 获取已经爬取到的地址
    def select_has_insert(self):
        _connect = sqlite3.connect(self.db_name)
        _connect_cursor = _connect.cursor()
        _result = _connect_cursor.execute('select * from tbl_url')
        fetchall = _connect_cursor.fetchall()
        _connect_cursor.close()
        _connect.commit()
        return fetchall
