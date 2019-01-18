"""双向链表
-- 一种更复杂的链表, 每个节点有2个连接: 一个指向上节点, 一个指向下节点,
首节点的上节点为空, 尾节点的下节点为空

date: 18-12-27 下午9:06
"""


class Node(object):
    """双向链表节点"""

    def __init__(self, item):
        """初始化"""

        # 几点数据
        self.item = item
        # 下节点链接
        self.next = None
        # 上节点链接
        self.prev = None


class DLinkList(object):
    """双向链表"""

    def __init__(self):
        """初始化"""

        # 链表头
        self.__head = None

    # 获取链表是否为空
    def is_empty(self):
        """链表是否为空, 链表头状态取反"""
        return not self.__head

    # 获取链表⻓度
    def length(self):
        """获取链表长度"""

        # 获取链表头
        cur = self.__head
        # 累计长度
        count = 0
        # 循环, 直到游标下节点链接为空
        while cur:
            # 累加长度
            count += 1
            # 当前游标赋值为下节点
            cur = cur.next
        # 返回链表长度
        return count

    # 遍历展示链表
    def show(self):
        """遍历展示链表"""

        # 获取链表头数据 -- 游标
        cur = self.__head
        # 打印数据列表
        str_list = []
        # 循环, 直到游标下节点链接为空
        while cur:
            # 添加打印数据列表数据
            str_list.append(cur.item)
            # 当前游标赋值下节点数据
            cur = cur.next
        # 换行
        print(*str_list, sep=" --->")

    # 链表添加头节点
    def add(self, item):
        """链表添加头节点
        -- 链表头添加数据, 原链表头下节点链接赋值给新节点的下节点链接,
        下节点的上节点链接 和 现在链表头下节点链接 指向 新节点

        :param item: 新节点数据
        """

        # 实例化新节点
        node = Node(item)
        # 如果链表为空
        if self.is_empty():
            # 链表头赋值
            self.__head = node
        #
        else:
            # 新节点的下节点 赋值为 原链表头的下节点
            node.next = self.__head
            # 新节点下节点的上节点 赋值为 新节点
            node.next.prev = node
            # 现在链表头下节点 赋值为 新节点
            self.__head = node

    # 链表添加尾节点
    def append(self, item):
        """链表添加尾节点
        -- 查找到当前链表的尾节点,
        将尾节点的下节点赋值为新节点,
        新节点的上节点赋值为原尾节点

        :param item:
        :return:
        """

        # 初始化新节点
        node = Node(item)
        # 如果链表为空
        if self.is_empty():
            # 直接添加链表头数据
            self.add(item)
        #
        else:
            # 获取链表头数据 -- 游标
            cur = self.__head
            # 循环, 直到游标下节点为空
            while cur.next:
                # 当前游标 赋值为 下节点
                cur = cur.next
            # 游标下节点 赋值为 新节点
            cur.next = node
            # 新节点的上节点 赋值为 游标
            node.prev = cur

    # 指定位置添加
    def insert(self, pos, item):
        """指定位置添加数据
        -- 判断, 如果指定位置小于等于0, 链表添加头节点
        判断, 如果指定位置大于等于链表长度, 链表添加尾节点
        否则, 将指定位置上节点原下节点的上节点指向 新节点,
        新节点的下节点指向 指定位置上节点的原下节点,
        指定位置上节点的下节点指向 新节点,
        新节点的上节点指向 指定位置的上节点,

        :param pos: 指定位置
        :param item: 新节点数据
        :return:
        """

        # 如果指定位置小于等于0
        if pos <= 0:
            # 链表添加头节点
            self.add(item)
        # 如果指定位置大于等于 链表长度
        elif pos >= self.length():
            # 链表添加尾节点
            self.append(item)
        # 
        else:
            # 实例化新节点
            node = Node(item)
            # 获取链表头数据 -- 游标
            cur = self.__head
            # 累计位置
            count = 0
            # 循环, 知道累计位置 等于 指定位置的上节点
            while count != (pos - 1):
                # 累加位置
                count += 1
                # 游标 赋值为 下节点
                cur = cur.next
            # 游标原下节点的上节点 赋值为 新节点
            cur.next.prev = node
            # 新节点的下节点 赋值为 游标原下节点
            node.next = cur.next
            # 游标的下节点 赋值为 新节点
            cur.next = node
            # 新节点的上节点 赋值为 游标
            node.prev = cur

    # 删除节点
    def remove(self, item):
        """根据节点数据删除节点
        -- 如果删除的节点是链表头, 将链表头赋值为删除节点的下节点, 并将其上节点清空,
        否则, 将删除节点的上节点的下节点 赋值为 删除节点的下节点,
        删除节点的下节点的上节点 赋值为 删除节点的上节点,
        删除节点引用为0, 自动自动回收

        :param item: 节点数据
        :return:
        """

        # 获取链表头数据 -- 游标
        cur = self.__head
        # 循环, 知道游标为空
        while cur:
            # 如果游标数据 等于 删除节点数据
            if cur.item == item:
                # 如果 游标 等于 链表头
                if cur == self.__head:
                    # 链表头 赋值为 删除节点的下节点
                    self.__head = cur.next
                    # 如果链表头不为空
                    if self.__head:
                        # 链表头的上节点清空
                        self.__head.prev = None
                # 不是链表头
                else:
                    # 游标上节点的下节点 赋值为 删除节点的下节点
                    cur.prev.next = cur.next
                    # 如果删除节点的下节点不为空
                    if cur.next:
                        # 删除节点的下节点的上节点 赋值为 删除节点的上节点
                        cur.next.prev = cur.prev
                # 跳出循环
                break
            #
            else:
                # 游标 赋值为 下节点
                cur = cur.next

    # 查找节点是否存在
    def search(self, item):
        """查找节点是否存在
        根据链表头, 循环链表, 判断链表中是否存在此数据

        :param item: 查找的数据
        :return:
        """

        # 获取链表头数据 -- 游标
        cur = self.__head
        # 循环, 直到游标为空
        while cur:
            # 如果游标数据 等于 查找数据
            if cur.item == item:
                # 返回True
                return True
            # 游标 赋值为 下节点
            cur = cur.next
        # 返回False
        return False


if __name__ == '__main__':
    ll = DLinkList()
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
