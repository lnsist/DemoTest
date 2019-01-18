"""单链表
-- 是链表中最简单的一种形式, 它的每个节点包含两个域, 一个信息域( 元素域 ) 和一个链接域,
这个链接指向链表中下一节点数据, 而最后一个节点的链接域则是指向一个空值

date: 18-12-25 下午8:27
"""


class Node(object):
    """链表节点"""

    def __init__(self, item):
        """初始化
        :param item: 数据
        """
        # 数据
        self.item = item
        # 下节点链接
        self.next = None


class SingleLinkList(object):
    """单链表"""

    def __init__(self):
        """初始化"""
        # 链表头
        self.__head = None

    # 获取链表是否为空
    def is_empty(self):
        """获取链表是否为空"""
        return not self.__head

    # 获取链表⻓度
    def length(self):
        """获取链表长度"""

        # 获取链表头数据 -- 游标
        cur = self.__head
        # 累计数量 -- 默认为0
        count = 0
        # 循环游标不为空
        while cur:
            # 累加数量
            count += 1
            # 获取下节点链接
            cur = cur.next
        # 返回累计数量
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
        print(*str_list, sep=" ---> ")

    # 链表头部添加元素
    def add(self, item):
        """链表头部添加元素
        要将原链表头引用的链接赋值给新的节点,
        然后赋值聊表头新节点引用
        :param item: 新节点数据
        """
        # 实例化新节点
        node = Node(item)
        # 获取现链表头的链接引用
        node.next = self.__head
        # 更新链表头为新节点引用
        self.__head = node

    # 链表尾部添加元素
    def append(self, item):
        """链表尾部添加元素
        判断如果链表为空, 直接赋值新节点为链表头
        否则, 获取链表头数据, 循环获取下节点链接, 直到下节点链接为空的节点,
        即, 获取到尾节点, 将新节点赋值给尾节点的链接区
        :param item: 新节点数据
        """

        # 实例化新节点数据
        node = Node(item)
        # 判断如果链表为空
        if self.is_empty():
            # 直接赋值为链表头
            self.add(node)
        else:
            # 获取链表头数据 -- 游标
            cur = self.__head
            # 根据链表头循环获取下一节点, 直到获取到尾节点
            while cur.next:
                # 获取下节点链接
                cur = cur.next
            # 循环结束后, node的下一节点为空, 进行赋值
            cur.next = node

    # 指定位置添加元素
    def insert(self, pos, item):
        """指定位置添加元素 -- 保序
        判断, 如果指定位置小于等于0, 直接调用add添加至链表头
        判断, 如果指定位置大于等于链表长度, 直接调用append链表尾节点添加元素
        否则, 获取链表头, 循环直到指定位置, 插入新节点, 指定位置前节点链接换为新节点,
        新节点的链接为指定位置前节点的原链接
        :param pos: 指定位置
        :param item: 新节点数据
        """
        # 如果指定位置小于等于0
        if pos <= 0:
            # 添加至链表头
            self.add(item)
        # 如果指定位置大于等于链表总长度
        elif pos >= self.length():
            # 添加至链表尾
            self.append(item)
        # 指定位置正常, 则进行数据插入
        else:
            # 实例化新节点
            node = Node(item)
            # 初始化循环次数
            count = 0
            # 获取链表头数据 -- 游标
            cur = self.__head
            # 循环累计循环次数, 直到等于指定位置
            while count != (pos - 1):
                # 累加循环次数
                count += 1
                # 更新指定位置前一节点数据
                cur = cur.next
            # 新节点链接 赋值 前节点链接
            node.next = cur.next
            # 前节点链接 赋值 新节点
            cur.next = node

    # 删除节点
    def remove(self, item):
        """删除节点
        判断, 如果要删除的节点是链表头, 直接修改链表头链接指向下一节点
        否则, 循环判断当前节点数据是否等于删除节点数据, 如果是则将前节点链接指向删除节点的链接,
        删除节点引用为0, 系统会自动删除
        :param item: 要删除的节点数据
        """
        # 获取链表头数据 -- 游标
        cur = self.__head
        # 初始化前节点    
        prev = None
        # 循环 游标 下节点链接不为空
        while cur:
            # 如果当前 游标 数据 等于删除 删除节点数据
            if cur.item == item:
                # 如果前节点为空, 则当前游标是链表头
                if not prev:
                    # 链表头链接赋值为下下节点数据
                    self.__head = cur.next
                # 不是链表头数据
                else:
                    # 前节点链接 赋值 游标下一节点链接, 取消当前链接指向
                    prev.next = cur.next
                # 跳出循环
                break
            # 不相等, 继续循环
            else:
                # 当前游标赋值为 前节点
                prev = cur
                # 更新当前游标数据 为 下节点链接
                cur = cur.next

    # 查找节点是否存在
    def search(self, item):
        """查找节点是否存在
        获取链表头, 循环判断是否相等, 相等返回True, 循环结束返回False
        :param item: 查找节点的数据
        """
        # 获取链表头数据 -- 游标
        cur = self.__head
        # 循环, 游标不为空
        while cur:
            # 如果游标数据等于查找节点数据
            if cur.item == item:
                # 返回True
                return True
            # 更新游标为下节点链接
            cur = cur.next
        # 返回False
        return False


if __name__ == "__main__":
    ll = SingleLinkList()
    ll.add(1)
    ll.add(2)
    ll.append(3)
    ll.insert(1, 4)
    print("length:", ll.length())
    ll.show()
    print(ll.search(3))
    print(ll.search(5))
    ll.remove(1)
    print("length:", ll.length())
    ll.show()
