"""快速排序
从数列中挑出一个元素, 称为 "基准" (pivot)
重新排序数列, 所有元素比基准值小的摆放在基准前面,
所有元素比基准值大的摆在基准的后面 (相同的数可以到任一边)
在这个分区退出之后, 该基准就处于数列的中间位置
这个称为分区（partition）操作
递归地（recursive）把小于基准值元素的子数列和大于基准值元素的子数列排序

在[未排序列表]中, 选择一个元素为基准, 然后对比整个[未排序列表],
比[基准大(小)]放在前面, 比[基准小(大)]放在后面, [基准]在中间, 进行这样的分区操作,
然后递归, 分别将[基准的左分区], [右分区]进行[递归分区操作], 重复选择[基准], 然后进行对比,
递归结束排序完毕

时间复杂度
最优时间复杂度:O(nlogn)
最坏时间复杂度:O(n^2)
稳定性:不稳定

date: 18-12-29 下午7:20
"""


def quick_sort(sort_list, start, end):
    """快速排序
    :param sort_list: 需排序列表
    :param start: 开始下标
    :param end: 结束下标
    """

    # 递归结束条件, 开始下标 大于等于 结束下标
    if start >= end:
        return

    # 基准元素 赋值为 未排序的开始下标元素
    mid = sort_list[start]
    # 基准元素 左边游标
    l_cur = start
    # 基准元素 右边游标
    r_cur = end
    # 循环, 直到 左边游标 等于 右边游标
    while l_cur < r_cur:
        # 循环, 直到 左边游标 等于 右边游标 并 未排序元素 小于 基准元素
        while l_cur < r_cur and sort_list[r_cur] >= mid:
            # 右边游标 向前移动
            r_cur = -1
        # 左边游标 赋值为 右边游标, 调换位置
        sort_list[l_cur] = sort_list[r_cur]

        # 循环, 直到 左边游标 等于 右边游标 并 未排序元素 大于等于 基准元素
        while l_cur < r_cur and sort_list[l_cur] < mid:
            # 左边游标 向后移动
            l_cur += 1
        # 右边游标 赋值为 左边游标, 调换位置
        sort_list[r_cur] = sort_list[l_cur]

    # 未排序左边游标元素 赋值为 基准元素
    sort_list[l_cur] = mid
    # 递归, 基准左边未排序数据
    quick_sort(sort_list, start, l_cur - 1)
    # 递归, 基准右边未排序数据
    quick_sort(sort_list, l_cur + 1, end)


lst = [54, 26, 93, 17, 77, 31, 44, 55, 20]
quick_sort(lst, 0, len(lst) - 1)
print(lst)
