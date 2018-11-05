"""
京东商城案例(课后作业)：
1. 需求：
做一个小的案例，通过用户的选择，管理商品类型表信息
效果图如下：
******************************
1. 所有类型
2. 查询类型
3. 新增类型
4. 删除类型
5. 更新类型
0. 退出选择
******************************
"""
import pymysql


# 京东商城数据库操作
class Jd_store(object):
    # 初始化
    def __init__(self):
        # 数据库连接
        self.db_connect = pymysql.connect(host="localhost", port=3306, db="db_jd", user="root", password="123456", charset="utf8")
        # 游标
        self.db_cursor = self.db_connect.cursor()

    # 关闭资源
    def __del__(self):
        self.db_close()

    def db_close(self):
        """关闭资源
        :return:
        """
        if self.db_cursor:
            # 关闭游标
            self.db_cursor.close()
        if self.db_connect:
            # 关闭事务
            self.db_connect.close()

    def db_insert(self, param):
        """增加数据
        :param param -- 数据库参数
        :return:
        """
        # sql 语句
        sql = "insert t_breed values(0, %s, 0)"
        # 数据库查询, 返回响应行数
        rows = self.db_cursor.execute(sql, param)
        # 输出信息
        print("成功新增 %d 条数据" % rows) if rows > 0 else print("新增数据失败")
        # 事务提交
        self.db_connect.commit()

    def db_update(self, param):
        """修改数据
        :param param -- 数据库参数
        :return:
        """
        # sql 语句
        sql = "update t_breed set type = %s where id = %s"
        # 数据库查询, 返回响应行数
        rows = self.db_cursor.execute(sql, param)
        # 输出信息
        print("成功更新 %d 条数据" % rows) if rows > 0 else print("更新数据失败")
        # 事务提交
        self.db_connect.commit()

    def db_delete(self, param):
        """删除数据
        :param param -- 数据库参数
        :return:
        """
        # sql 语句
        sql = "update t_breed set state = 1 where id = %s"
        # 数据库查询, 返回响应行数
        rows = self.db_cursor.execute(sql, param)
        # 输出信息
        print("成功删除 %d 条数据" % rows) if rows > 0 else print("删除数据失败")
        # 事务提交
        self.db_connect.commit()

    def db_select(self, param=None):
        """查询数据
        :param param -- 数据库参数
        :return: 查询到的数据
        """
        # sql 语句
        sql = "select * from t_breed"
        # 如果有参数
        if param:
            sql += " where type like %s"
            param = ["%%%s%%" % param[0]]
        # 数据库查询, 返回响应行数
        rows = self.db_cursor.execute(sql, param)
        # 统计数据
        print("成功查询 %d 条数据" % rows) if rows > 0 else print("查询数据失败")
        # 如果查询到数据
        if rows > 0:
            # 返回查询到的数据
            fetchall_return = self.db_cursor.fetchall()
            # 关闭资源
            self.db_close()
            return fetchall_return


def ui():
    """UI显示
    :return:
    """
    print("******************************\n"
          "1. 所有类型\n"
          "2. 查询类型\n"
          "3. 新增类型\n"
          "4. 删除类型\n"
          "5. 更新类型\n"
          "0. 退出选择\n"
          "******************************")


def main():
    # 京东数据库
    jd_store = Jd_store()
    while True:
        # UI
        ui()
        # 获取功能
        do_smoe = input("请输入需要操作的功能:")
        if do_smoe == "1":
            """查询所有"""
            all_select = jd_store.db_select()
            # 循环显示
            for item in all_select:
                print(item)
        elif do_smoe == "2":
            """模糊查询"""
            str_type = input("请输入需要查询的类型:")
            all_select = jd_store.db_select([str_type])
            # 循环显示
            for item in all_select:
                print(item)
        elif do_smoe == "3":
            """新增数据"""
            str_type = input("请输入需要新增的类型:")
            jd_store.db_insert([str_type])
        elif do_smoe == "4":
            """删除数据"""
            str_type = input("请输入需删除的ID:")
            jd_store.db_delete([str_type])
        elif do_smoe == "5":
            """更新数据"""
            str_type = input("请输入需要更新的ID:")
            new_type = input("请输入更新后的类型:")
            jd_store.db_update([new_type, str_type])
        elif do_smoe == "0":
            """退出系统"""
            again = input("确定要退出系统吗?(y/n)")
            if again.lower() == "y":
                print("已退出系统")
                break
        else:
            print("输入有误, 请重新输入")
            continue


if __name__ == '__main__':
    main()
