"""
    MySQL业务类, 增删改查
date: 18-10-18 上午8:59
"""

import pymysql

# 数据库地址
SQL_HOST = "localhost"
# 数据库端口
SQL_PORT = 3306
# 用户
SQL_USER = "root"
# 密码
SQL_PASSWORD = "123456"
# 指定数据库
SQL_DB = "db_test"


class MySQL(object):
    """
        MySQL业务类, 增删改查
    """

    def __init__(self, host=SQL_HOST, port=SQL_PORT, user=SQL_USER, password=SQL_PASSWORD, db=SQL_DB):
        """
            初始化 -- 数据库连接
        :param host: 数据库地址
        :param port: 数据库端口
        :param user: 用户
        :param password: 密码
        :param db: 指定数据库
        """
        # 连接数据库
        self.db = pymysql.connect(host=host, port=port, user=user, password=password, db=db, charset="utf8")
        # 数据库游标
        self.cursor = self.db.cursor()

    def insert_data(self, table, data):
        """
            插入数据
        如:
            table="t_t1"
            data={"id": 1, "name": "张三", "age": 20}
        :param table: 表名 -- 需要插入数据的表
        :param data: 数据 -- 字典
        :return:
        """
        # 判断传入参数类型 -- 是否字典类型
        if not isinstance(data, dict):
            # 抛出异常
            raise TypeError("传入的数据不是字典类型")
        # 获取k集合, -- (k1, k2, k3, k4...)
        keys = ",".join(data.keys())
        # 获取v集合 -- (k1, k2, k3, k4...)
        values = ",".join(["%s"] * len(data))
        # 格式化sql语句
        sql = "insert into %(table)s (%(keys)s) values(%(values)s)" % ({"table": table, "keys": keys, "values": values})
        # 捕获异常
        try:
            # 游标执行sql语句
            self.cursor.execute(sql, tuple(data.values()))
            # 输出提示
            print("添加数据 -- 成功")
            # 事务提交
            self.db.commit()
        except pymysql.MySQLError as e:
            # 输出提示
            print("添加数据 -- 失败")
            # 输出错误提示
            print(e)
            # 事务回滚
            self.db.rollback()

    def remove_data(self, table, data_id):
        """
            逻辑删除 -- 根据ID修改其状态为删除
        如:
            table="t_t1"
            data_id=1
        :param table: 表名 -- 需要修改数据的表
        :param data_id: 数据ID
        :return:
        """
        # 格式化sql语句
        sql = "update %(table)s set state = 1 where id = %(id)s" % ({"table": table, "id": data_id})
        # 捕获异常
        try:
            # 游标执行sql语句
            self.cursor.execute(sql)
            # 输出提示
            print("删除数据 -- 成功")
            # 事务提交
            self.db.commit()
        except pymysql.MySQLError as e:
            # 输出提示
            print("删除数据 -- 失败")
            # 输出异常提示
            print(e)
            # 事务回滚
            self.db.rollback()

    def update_data(self, table, data):
        """
            修改数据
        如:
            table="t_t1"
            data={"id": 1, "name": "张三", "age": 20}
        :param table: 表名 -- 需要修改数据的表
        :param data: 数据 -- 包括数据ID
        :return:
        """
        # 判断传入参数类型 -- 是否字典类型
        if not isinstance(data, dict):
            # 抛出异常
            raise TypeError("传入的数据不是字典类型")
        # 需要修改的数据
        k_v = []
        # 需要修改的数据ID
        data_id = ""
        # 循环数据, 格式化
        for k, v in data.items():
            # 如果是ID数据
            if k == "id":
                # 单独保存ID数据, 用以更新指定ID数据
                data_id = v
                # 进入下次循环
                continue
            # 追加数据
            k_v.append((k + "='" + str(v) + "'"))
        # 如果数据中未包含ID参数
        if not data_id:
            # 抛出异常
            raise ValueError("数据中未包含ID参数, 无法指定ID更新数据")
        # 格式化sql语句
        sql = "update %(table)s set %(k_v)s where id = %(id)s" % ({"table": table, "k_v": ",".join(k_v), "id": data_id})
        # 捕获异常
        try:
            # 游标执行sql语句 -- 传入参数
            self.cursor.execute(sql)
            # 输出提示
            print("修改数据 -- 成功")
            # 事务提交
            self.db.commit()
        except pymysql.MySQLError as e:
            # 输出提示
            print("修改数据 -- 失败")
            # 输出异常提示
            print(e)
            # 事务回滚
            self.db.rollback()

    def select_data(self, table, field="*", condition=""):
        """
            查询数据
        如:
            field="id, name, age"
            condition="id='1' and state='0'"
        :param table: 表名 -- 需要查询数据的表
        :param field: 自定义查询字段, 默认查询全部字段
        :param condition: 自定义查询条件, 默认无查询条件
        :return: 查询结果
        """
        # sql语句
        sql = "select %(field)s from %(table)s " % ({"field": field, "table": table})
        # 如果有查询条件
        if condition:
            # 拼接sql语句
            sql += " where " + condition
        try:
            # 游标执行sql语句
            self.cursor.execute(sql)
            # 获取所有执行结果
            result = self.cursor.fetchall()
            # 返回查询结果
            return list(result)
        except pymysql.MySQLError as e:
            # 输出提示
            print("查询数据 -- 失败")
            # 输出异常提示
            print(e)
