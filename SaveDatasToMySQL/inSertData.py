# -*- coding: utf-8 -*-

import MySQLdb


class InsertData(object):
    def __init__(self, host, name, password, database, table=None):
        self.conn = MySQLdb.connect(host, name, password, database)
        self.cursor = self.conn.cursor()

    def _showTables(self):
        show_sql = """show tables"""

        self.cursor.execute(show_sql)
        data = self.cursor.fetchall()
        return data

    def insertData(self, data):

        sql = """select column_name from information_schema.COLUMNS where table_name='{}'""".format(data["logkey"])
        table_name = data["logkey"]
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        index_list = [key[0] for key in results]

        if "lmh" not in data and "lmh" in index_list:
            index_num = index_list.index("lmh")
            index_list.pop(index_num)

        index_value_list = []
        for index in index_list:
            # if index == "dt":
            #     data[index] = str(data[index]).replace(" ", "-")

            if index in data:
                if not index.isdigit():
                    index_value_list.append("'%s'" % data[index])
                else:
                    index_value_list.append(data[index])
            else:
                data[index] = "NULL"
                index_value_list.append(data[index])
        print index_list
        print index_value_list

        # value_list = [value for value in index_value_list]
        insert_sql = """INSERT INTO %s (%s)
                      VALUES (%s)""" % (table_name, ",".join(index_list), ", ".join(index_value_list))

        try:
            self.cursor.execute(insert_sql)
            self.conn.commit()
        except Exception, e:
            print e
            self.conn.rollback()


    def myCallProc(self, *args):
        self.cursor.callproc('step1', args)
        self.cursor.execute("select @begintime, @endtime")
        #, @istruncatelog


# if __name__ == '__main__':
#     insert = InsertData(host="localHost", name="root", password="zhouxiaoxi", database="CNLog")
#     data = {"mac": "b0-e2-35-43-25-11",
#             "idfa": "868869028976982",
#             "agent": "500",
#             "type": "active",
#             "channel": "369",
#             "tryCount": "0",
#             "tryNums": "",
#             "os": "1",
#             "token": "dae338a753b8af6b4326c76e10ec13dc",
#             "logkey": "active",
#             "ip": "113.87.8.11",
#             "dt": "2017-08-11 03:00:44",
#             "ua": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; MI 4S MIUI/V8.2.1.0.LAJCNDL)",
#             "dev": "B0:E2:35:43:25:11,868869028976982",
#             "ptid": "1"}
#
#     tables = insert.insertData(data)

