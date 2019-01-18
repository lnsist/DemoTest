"""希尔排序
选择一个增量序列t1, t2, …, tk, 其中ti>tj, tk=1；
按增量序列个数k, 对序列进行k 趟排序；
每趟排序, 根据对应的增量ti, 将待排序列分割成若干长度为m 的子序列, 
分别对各子表进行直接插入排序。仅增量因子为1 时, 整个序列作为一个表来处理, 表长度即为整个序列的长度

将[未排序列表]进行按步长划分[区域], [各个区域]自行两两对比排序,
[各个区域]排序完毕, 循环[减少步行], 直到最后[步行为1],
则整个列表逐个对比排序

最优时间复杂度:根据步⻓序列的不同而不同
最坏时间复杂度:O(n^2)
稳定性:不稳定

date: 18-12-29 下午8:12
"""


def shell_sort(sort_list):
    """希尔排序"""

    # 获取长度
    sort_list_length = len(sort_list)
    # 步长 为 长度的一半
    gap = sort_list_length // 2
    # 循环, 直到步长 小于等于 0
    while gap > 0:
        # 循环 步长 到 列表长度
        for i in range(gap, sort_list_length):
            # copy j
            j = i
            # 循环 直到 j 小于 步长 并 未排序列表下一步长元素 等于 当前 未排序元素
            while j >= gap and sort_list[j - gap] > sort_list[j]:
                # 调换位置
                sort_list[j - gap], sort_list[j] = sort_list[j], sort_list[j - gap]
                # j 赋值为 下一步长
                j -= gap
        # 步长 再除以 2
        gap = gap // 2

lst = [54, 26, 93, 17, 77, 31, 44, 55, 20]
shell_sort(lst)
print(lst)