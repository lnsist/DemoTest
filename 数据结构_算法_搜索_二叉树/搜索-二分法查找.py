"""二分法搜索
又称折半查找, 优点是比较次数少, 查找速度快, 平均性能好,
缺点只能查找有序表, 适用于不经常变动且查找频繁的有序列表,
原理: 每次查找时都是对列表的中间进行对比, 如果小(大)于则查左(右)边子列表的中间值,
一直进行折半的查找, 直到查找到为止, 或子列表不存在了则查找失败不存在

date: 18-12-29 下午9:31
"""


def binary_search(search_list, item):
    """非递归实现 -- 二分法搜索

    :param search_list: 搜索的列表
    :param item: 搜索数据
    :return:
    """

    # 开始下标
    start = 0
    # 结束下标
    end = len(search_list) - 1
    # 循环, 直到开始下标 大于 结束下标
    while start <= end:
        # 获取中间值
        midpoint = (start + end) // 2
        # 中间值 和 搜索数据 对比, 如果一致
        if search_list[midpoint] == item:
            # 返回True
            return True
        # 如果 搜索数据 小于 中间值
        elif item < search_list[midpoint]:
            # 结束下标 赋值为 当前中间值的上一个元素
            end = midpoint - 1
        #
        else:
            # 开始下标 赋值为 当前中间值的下一个元素
            start = midpoint + 1
    # 返回False
    return False


def binary_search_recursive(search_list, item):
    """递归 -- 二分法搜索

    :param search_list: 搜索的列表
    :param item: 搜索数据
    :return:
    """
    # 开始下标
    start = 0
    # 结束下标
    end = len(search_list) - 1
    # 循环, 直到开始下标 大于 结束下标
    while start <= end:
        # 获取中间值
        midpoint = (start + end) // 2
        # 中间值 和 搜索数据 对比, 如果一致
        if search_list[midpoint] == item:
            # 返回True
            return True
        # 如果 搜索数据 小于 中间值
        elif item < search_list[midpoint]:
            # 结束下标 赋值为 当前中间值的上一个元素
            end = midpoint - 1
            return binary_search_recursive(search_list[:end], item)
        #
        else:
            # 开始下标 赋值为 当前中间值的下一个元素
            start = midpoint + 1
            return binary_search_recursive(search_list[start:], item)
    #
    return False




testlist = [0, 1, 2, 8, 13, 17, 19, 32, 42, ]
print(binary_search(testlist, 3))
print(binary_search(testlist, 13))
print(binary_search_recursive(testlist, 3))
print(binary_search_recursive(testlist, 13))
