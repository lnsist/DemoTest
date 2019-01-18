"""单向循环链表
-- 单链表的一个变形, 链表中最后的节点的链接不再是None, 而指向链表头节点

date: 18-12-28 下午9:37
"""


class Node(object):
    """节点"""

    def __init__(self, item):
        self.item = item
        self.next = None


class SinCycLinkedList(object):
    """单向循环链表"""

    def __init__(self):
        """初始化"""

        # 链表头数据
        self.__head = None

    # 获取链表是否为空
    def is_empty(self):
        """获取链表是否为空"""
        return not self.__head

    # 获取链表的⻓度
    def length(self):
        """获取链表的长度"""

        # 如果链表为空
        if self.is_empty():
            # 返回0
            return 0
        # 获取链表头数据 -- 游标
        cur = self.__head
        # 累计长度 -- 默认为1, 因为只有1个元素时也不会进入循环
        count = 1
        # 循环, 直到游标下节点 等于 链表头 -- 尾节点
        while cur.next != self.__head:
            # 累加长度
            count += 1
            # 游标 赋值为 下节点
            cur = cur.next
        # 返回长度
        return count

    # 遍历展示链表
    def show(self):
        """遍历展示链表"""

        # 如果链表为空, 不进行打印
        if self.is_empty():
            return
        # 获取链表头数据 -- 游标
        cur = self.__head
        # 打印数据列表 -- 默认有初始值, 因为只有1个元素时, 循环也不会进入
        str_list = [cur.item]
        # 循环, 直到游标下节点 等于 链表头 -- 尾节点
        while cur.next != self.__head:
            # 游标 赋值为 下节点
            cur = cur.next
            # 打印数据列表添加数据 -- 直接设置为下节点的元素, 因为默认已添加第一个元素
            str_list.append(cur.item)
        # 格式化打印
        print(*str_list, sep=" ---> ")

    # 链表添加头节点
    def add(self, item):
        """链表添加头节点
        -- 如果链表为空, 链表头 赋值为 新节点,
        新节点的下节点 赋值为 链表头,
        否则, 循环获取链表尾节点的下节点 赋值为 新节点,

        :param item: 新节点数据
        :return:
        """

        # 实例化新节点
        node = Node(item)
        # 如果节点为空
        if self.is_empty():
            # 链表头 赋值为 新节点
            self.__head = node
            # 新节点的下节点 赋值为 链表头
            node.next = self.__head
        #
        else:
            # 获取链表头数据 -- 游标
            cur = self.__head
            # 循环, 知道游标的下节点 等于 链表头 -- 尾节点
            while cur.next != self.__head:
                cur = cur.next
            # 新节点的下节点 赋值为 原链表头
            node.next = self.__head
            # 尾节点的下节点 赋值为 新节点
            cur.next = node
            # 链表头 赋值为 新节点
            self.__head = node

    # 链表添加尾节点
    def append(self, item):
        """链表添加尾节点
        -- 如果链表为空, add添加至头节点,
        否则, 循环链表, 获取尾节点, 将尾节点的下节点 赋值为 新节点,
        新节点的下节点 赋值为 链表头,

        :param item: 新节点数据
        :return:
        """

        # 实例化新节点
        node = Node(item)
        # 如果链表为空
        if self.is_empty():
            # 调用add添加头节点
            self.add(node)
        #
        else:
            # 获取链表头数据 -- 游标
            cur = self.__head
            # 循环 直到游标下节点 等于 链表头 -- 尾节点
            while cur.next != self.__head:
                # 游标 赋值为 下节点
                cur = cur.next
            # 原尾节点的下节点 赋值为 新节点
            cur.next = node
            # 新节点的下节点 赋值为 链表头
            node.next = self.__head

    # 在指定位置添加节点
    def insert(self, pos, item):
        """在指定位置添加节点
        -- 如果 指定位置 小于等于 0, 调用add添加头节点,
        如果 指定位置 大于等于 链表航渡, 调用append添加尾节点,
        否则, 循环链表, 获取指定位置的上节点


        :param pos:
        :param item:
        :return:
        """

        # 如果指定位置 小于等于 0
        if pos <= 0:
            # 调用add添加头节点
            self.add(item)
        # 如果指定位置 大于等于 链表长度
        elif pos >= self.length():
            # 调用append添加尾节点
            self.append(item)
        #
        else:
            # 实例化新节点
            node = Node(item)
            # 获取链表头数据 -- 游标
            cur = self.__head
            # 累计位置
            count = 0
            # 循环, 直到累计位置 等于 指定位置的上节点
            while count != (pos - 1):
                # 累加位置
                count += 1
                # 游标 赋值为 下节点
                cur = cur.next
            # 新节点的下节点 赋值为 游标的原下节点
            node.next = cur.next
            # 游标下节点 赋值为 新节点
            cur.next = node

    # 删除一个节点
    def remove(self, item):
        """删除节点
        -- 循环链表,获取删除节点 和 删除节点的上节点, 如果删除节点 等于 链接头, 则循环链表, 获取尾节点,
        将链接头 赋值为 原链接头的下节点, 尾节点 赋值为 新链接头,
        否则, 普通节点, 则将删除节点的上节点 赋值为 删除节点的下节点,
        循环结束, 如果删除节点 等于 尾节点, 如果链表只有一个元素, 将链接头清空,
        否则, 将删除节点的上节点 赋值为 链表头,
        主要将删除节点的引用减少为0, 系统自动回收

        :param item:
        :return:
        """

        # 如果链表为空
        if self.is_empty():
            return
        # 获取链表头数据 -- 游标
        cur = self.__head
        # 游标上节点
        prev = None
        # 循环 直到游标下节点 等于 链表头
        while cur.next != self.__head:
            # 如果 游标 等于 删除节点
            if cur.item == item:
                # 如果 游标 等于 链接头
                if cur == self.__head:
                    # 获取链表头 -- 尾节点游标
                    rear = self.__head
                    # 循环 直到尾节点游标 等于 尾节点
                    while rear.next != self.__head:
                        # 尾节点游标 赋值为 下节点
                        rear = rear.next
                    # 链接头 赋值为 原链接头的下节点
                    self.__head = self.__head.next
                    # 尾节点下节点 赋值为 链接头
                    rear.next = self.__head
                # 不是链接头
                else:
                    # 游标上节点 赋值为 游标下节点
                    prev.next = cur.next
                # 退出函数
                return
            #
            else:
                # 上节点 赋值为 游标
                prev = cur
                # 游标 赋值为 下节点
                cur = cur.next
        # 循环结束, 如果尾节点 等于 删除节点
        if cur.item == item:
            # 如果 游标 等于 链接头
            if cur == self.__head:
                # 清空链接头
                self.__head = None
            #
            else:
                # 游标上节点 赋值为 游标下节点
                prev.next = self.__head

    # 查找节点是否存在
    def search(self, item):
        """查找节点是否存在
        -- 循环链表逐个判断数据是否相等
        如果链表只有一个元素, 则不会进入循环, 需再此判断数据是否相等

        :param item: 查找的节点数据
        :return:
        """

        # 如果链表为空
        if self.is_empty():
            return False
        # 获取链表头数据 -- 游标
        cur = self.__head
        # 循环 直到游标下节点 等于 链表头
        while cur.next != self.__head:
            # 如果游标 等于 查找节点
            if cur.item == item:
                # 返回True
                return True
            # 游标 赋值为 下节点
            cur = cur.next
        # 循环结束 或 未进入循环, 手动判断数据是否相等, 如果相等
        if cur.item == item:
            # 返回True
            return True
        # 返回 False
        return False


if __name__ == '__main__':
    ll = SinCycLinkedList()
    ll.add(1)
    ll.add(2)
    ll.append(3)
    ll.insert(2, 4)
    ll.insert(4, 5)
    ll.insert(0, 6)
    print("length:", ll.length())
    ll.show()
    print(ll.search(3))
    print(ll.search(100))
    ll.remove(1)
    print("length:", ll.length())
    ll.show()
