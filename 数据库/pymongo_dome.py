"""
pymongo 对 MongoDB 进行 增删改查

date: 18-9-27 下午4:11
"""
import pymongo
from bson import ObjectId


def mongo_insert(collection):
    """
        mongo 添加数据
    :param collection: 具体的集合
    :return:
    """
    # 测试数据
    student1 = {
        "id": "20170101",
        "name": "Jordan",
        "age": 20,
        "gender": "m"
    }
    # 测试数据
    student2 = {
        "id": "20170102",
        "name": "Mike",
        "age": 21,
        "gender": "f"
    }
    # 添加 测试数据 -- 返回自动生成的ID    ---- 不推荐
    # result = collection.insert([student1, student2])

    # 添加 单条数据
    # result = collection.insert_one(student1)

    # 添加 多条数据
    result = collection.insert_many([student1, student2])
    # 输出返回结果
    print(result.inserted_ids)


def mongo_select(collection):
    """
        mongo 查询数据
    :param collection: 具体的集合
    :return:
    """
    # 根据 ID对象 获取数据
    # result = collection.find({"_id": ObjectId("5bac932419437b7d7ebbdecc")})

    # 查询一条数据
    # result = collection.find_one({"name", "Mike"})

    # 查询所有匹配的数据
    # results = collection.find({"age": 20})

    # 计数 -- 统计查询到的数据数量
    # count = collection.find().count()

    # 排序 -- 以 age 升序排列, 降序为 pymongo.DESCENDING
    # results = collection.find().sort("age", pymongo.ASCENDING)

    # 偏移 -- 忽略前面 2 个数据, 只获取之后的数据
    # results = collection.find().skip(2)

    # 截取 -- 只获取 2 个数据, 用于分页查询
    # results = collection.find().limit(2)

    # 参数为空查询所有数据
    results = collection.find()

    # 循环输出
    for result in results:
        # 输出数据
        print(result)


def mongo_update(collection):
    """
        mongo 更新数据
    :param collection: 具体的集合
    :return:
    """
    # 查询条件 -- 年龄大于20
    condition = {"age": {"$gt": 20}}
    # 先查询数据
    results = collection.find(condition)
    # 循环更新 -- 单个更新
    for result in results:
        # 更新数据
        result["age"] = 18
        # 根据查询条件, 更新数据, $set保存原有数据, 只更新修改部分
        collection.update_one(condition, {"$set": result})

    # 功能同上
    # collection.update_many(condition, {"$set": {"age": 18}})

    # 批量更新 -- 年龄 + 1
    # collection.update_many(condition, {"$inc": {"age": 1}})


def mongo_delete(collection):
    """
        删除数据
    :param coolection: 具体的集合
    :return:
    """
    # 删除一条数据, 返回删除行数
    result = collection.delete_one({"name": "Jordan"})
    # 输出删除行数
    print(result.deleted_count)

    # 批量删除数据, 年龄小于20
    result = collection.delete_many({"age": {"$lt": 20}})
    # 输出删除行数
    print(result.deleted_count)

    # 参数字典为空, 删除全部
    # result = collection.delete_many({})
    # 输出删除行数
    # print(result.deleted_count)


def main():
    # 创建连接对象
    client = pymongo.MongoClient(host="localhost")
    # 连接数据库
    db = client.db_test
    # 指定集合 -- 关系型数据库的表
    collection = db.t_test

    # 添加数据
    mongo_insert(collection)

    # 更新数据
    mongo_update(collection)

    # 删除数据
    mongo_delete(collection)

    # 查询数据
    mongo_select(collection)


if __name__ == '__main__':
    main()
