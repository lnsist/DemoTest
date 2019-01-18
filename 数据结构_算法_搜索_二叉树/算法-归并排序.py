"""归并排序
把长度为n的输入序列分成两个长度为n/2的子序列
对这两个子序列分别采用归并排序
将两个排序好的子序列合并成一个最终的排序序列

将[未排序列表]递归分组, 一直分到最小个数(2个元素)列表,
然后对此子列表排序, 排序后对同一级别(2个元素)子列表排序,
同级子列表排序后合并, 变成4个元素子列表, 后又和同级别子列表排序,
递归分组减少元素, 合并分组增加元素,
一直循环直到最后剩下完整的列表

date: 18-12-29 下午8:35
"""


def merge_sort(sort_list):
    """递归分组"""

    # 递归结束条件, 列表长度 小于等于 1
    if len(sort_list) <= 1:
        # 返回列表
        return sort_list
    # 中间下标
    num = len(sort_list) // 2
    # 左边分组
    left = merge_sort(sort_list[:num])
    # 右边分组
    right = merge_sort(sort_list[num:])
    # 合并左右分组
    return merge(left, right)


def merge(left, right):
    """合并分组

    :param left: 左列表
    :param right: 右列表
    :return:
    """

    # 左右下标
    l, r = 0, 0
    # 结果列表
    result = []
    # 循环, 直到左右下标 大于等于 左右分组长度
    while l < len(left) and r < len(right):
        # 如果左分组元素 小于等于 右分组元素
        if left[l] <= right[r]:
            # 结果列表 追加 左分组元素
            result.append(left[l])
            # 左下标 + 1
            l += 1
        else:
            # 结果列表 追加 右分组元素
            result.append(right[r])
            # 右下标 + 1
            r += 1
    # 循环结束, 将左右分组列表剩下的元素, 直接追加到结果列表中
    result += left[l:]
    result += right[r:]
    # 返回结果列表
    return result


lst = [54, 26, 93, 17, 77, 31, 44, 55, 20]
sorted_list = merge_sort(lst)
print(sorted_list)
