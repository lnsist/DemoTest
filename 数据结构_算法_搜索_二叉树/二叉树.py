"""二叉树创建和遍历
二叉树是每个节点最多只有两个子树的树结构, 通常子树被称为"左子树"和"右子树"

date: 18-12-29 下午10:17
"""


class Node(object):
    """节点类"""

    def __init__(self, data):
        """初始化"""

        # 自身数据
        self.data = data
        # 左节点
        self.l_child = None
        # 右节点
        self.r_child = None


class Queue(object):
    """队列"""

    def __init__(self):
        """初始化"""

        # 空列表
        self.__item = []

    def enqueue(self, data):
        """追加数据

        :param data: 数据
        :return:
        """
        self.__item.append(data)

    def dequeue(self):
        """移除数据"""

        return self.__item.pop(0)

    def is_empty(self):
        """获取队列是否为空"""

        return not self.__item


class BinaryTree(object):
    """二叉树"""

    def __init__(self):
        """初始化"""

        # 根节点
        self.__root = None

    # 插入一个节点, 注意在插入的过程当中必须保证完全二叉树的特征
    def add(self, data):
        """添加节点
        -- 如果二叉树为空, 则根节点赋值为新节点
        否则, 循环判断获取队列定部节点的左子树是否为空,
        如果是空, 则添加新节点,
        如果不为空, 则队列添加左子树节点,
        接着判断获取队列定部节点的右子树是否为空,
        如果是空, 则添加新节点,
        如果不为空, 则队列添加右子树节点,
        如此循环添加队列, 直到某个左(右)子树为空, 添加新节点为止,

        :param data: 节点数据
        :return:
        """

        # 实例化节点
        node = Node(data)
        # 如果二叉树为空
        if self.is_emtpy():
            # 当前根节点
            self.__root = node
            # 退出函数
            return
        # 实例化队列
        q = Queue()
        # 添加根节点
        q.enqueue(self.__root)

        # 死循环, 直到内部手动跳出循环
        while True:
            # 获取队列顶部节点 -- 一开始是根节点, 接着是 [左子树, 右子树, 左子树的左子树, 左子树的右子树, ....]
            root = q.dequeue()
            # 如果节点左子树点为空
            if not root.l_child:
                # 将新节点添加至此节点的左子树中
                root.l_child = node
                # 跳出函数
                return
            # 添加左子树节点
            q.enqueue(root.l_child)
            # 如果节点右子树为空
            if not root.r_child:
                # 将新节点添加至此节点的右子树中
                root.r_child = node
                # 跳出函数
                return
            # 添加右子树节点
            q.enqueue(root.r_child)

    # show(): 广度遍历（层次遍历）二叉树
    def show(self):
        """二叉树遍历
        -- 如果二叉树为空, 直接退出,
        否则, 循环打印二叉树, 从根节点开始, 逐个左(右)子树, 添加到队列中,
        每次获取顶部节点进行打印, 获取左(右)子树添加,
        """

        # 如果二叉树为空
        if self.is_emtpy():
            #
            return
        # 实例化队列
        q = Queue()
        # 初始化根节点
        q.enqueue(self.__root)
        # 循环, 直到节点为空
        while not q.is_empty():
            # 获取队列顶部节点
            root = q.dequeue()
            # 输出节点数据
            print(root.data)
            # 如果节点左子树不为空
            if root.l_child:
                # 队列追加左子树
                q.enqueue(root.l_child)
            # 如果节点右子树不为空
            if root.r_child:
                # 队列追加右子树
                q.enqueue(root.r_child)

    def is_emtpy(self):
        """获取二叉树是否为空"""

        return not self.__root

    # search(data): 广度遍历查找
    def search(self, data):
        """二叉树查找
        -- 如果二叉树为空, 直接退出,
        否则, 循环二叉树, 从根节点开始对比不相等的话, 逐个左(右)子树, 添加到队列中,
        每次获取顶部节点进行对比不相等的话, 获取左(右)子树添加,
        只有某个节点相等则跳出函数

        :param data: 查找数据
        :return:
        """
        # 如果二叉树为空
        if self.is_emtpy():
            #
            return False
        # 实例化队列
        q = Queue()
        # 初始化根节点
        q.enqueue(self.__root)
        # 如果队列不为空
        while not q.is_empty():
            # 获取队列顶部节点
            root = q.dequeue()
            # 如果节点数据 等于 查找数据
            if root.data == data:
                #
                return True
            # 如果节点左子树不为空
            if root.l_child:
                # 队列追加节点左子树
                q.enqueue(root.l_child)
            # 如果节点左子树不为空
            if root.r_child:
                # 队列追加节点左子树
                q.enqueue(root.r_child)
        #
        return False

    def get_root(self):
        """获取根节点"""
        return self.__root

    def delete(self):
        """清空二叉树"""
        self.__root = None


"""
          0
      1        2
   3     4  5     6
 7  8   9
"""


def preorder(root):
    """递归实现先序遍历
    先访问根节点, 然后递归使用先序遍历访问左子树, 再递归使用先序遍历访问右子树
    根节点->左子树->右子树
    0-9的二叉树
    先序遍历结果: 0 1 3 7 8 4 9 2 5 6
    """

    # 如果二叉树为空
    if not root:
        #
        return
    # 输出根节点
    print(root.data, end=" ")
    # 递归左子树
    preorder(root.l_child)
    # 递归右子树
    preorder(root.r_child)


def inorder(root):
    """递归实现中序遍历
    递归使用中序遍历访问左子树, 然后访问根节点, 最后再递归使用中序遍历访问右子树
    左子树->根节点->右子树
    0-9的二叉树
    中序遍历结果: 7 3 8 1 9 4 0 5 2 6
    """

    # 如果二叉树为空
    if not root:
        #
        return
    # 递归左子树
    inorder(root.l_child)
    # 输出根节点
    print(root.data, end=" ")
    # 递归右子树
    inorder(root.r_child)


def postorder(root):
    """递归实现后序遍历
    递归使用后序遍历访问左子树和右子树, 最后访问根节点
    左子树->右子树->根节点
    0-9的二叉树
    后序遍历结果: 7 8 3 9 4 1 5 6 2 0
    """

    # 如果二叉树为空
    if not root:
        #
        return
    # 递归左子树
    postorder(root.l_child)
    # 递归右子树
    postorder(root.r_child)
    # 输出根节点
    print(root.data, end=" ")


if __name__ == "__main__":
    # 实例化二叉树
    b = BinaryTree()

    # node1 = Node(0)
    # node2 = Node(1)
    # node3 = Node(2)
    #
    # b.root = node1
    # node1.l_child = node2
    # node1.r_child = node3
    #
    # node4 = Node(3)
    # node2.l_child = node4
    # node5 = Node(4)
    # node2.r_child = node5

    # print(b.root.data)
    # print(b.root.l_child.data)
    # print(b.root.r_child.data)
    # print(b.root.l_child.l_child.data)
    # print(b.root.l_child.r_child.data)

    for i in range(10):
        b.add(i)

    # b.show()

    # print(b.search(93))
    print("先序循环结果:", end=" ")
    preorder(b.get_root())
    print()

    print("中序循环结果:", end=" ")
    inorder(b.get_root())
    print()

    print("后序循环结果:", end=" ")
    postorder(b.get_root())
    print()

    b.delete()
