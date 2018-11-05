"""
    模拟Django的对象-关系映射ORM, 使用元类
date: 18-10-12 下午7:57
"""


class Field(object):
    """
        字段类 -- 数据库中的字段, 属性名对应字段, 属性数据对应关系
        将2个参数拼接成 xx:yy 返回出去
    """

    def __init__(self, name, column_type):
        """
            实例初始化
        :param name: 名字
        :param column_type: 类型
        """
        self.name = name
        self.column_type = column_type

    def __str__(self):
        """
            将2个参数拼接成 name:column_type, 返回出去
        :return: name:column_type
        """
        return "<%s:%s>" % (self.__class__.__name__, self.name)


class StringField(Field):
    """
        字符串字段
    """

    def __init__(self, name):
        # 调用父类初始化, 类型 varchar(100)
        super(StringField, self).__init__(name, "varchar(100)")


class IntegerField(Field):
    """
        数值字段
    """

    def __init__(self, name):
        # 调用父类初始化, 类型 bigint
        super(IntegerField, self).__init__(name, "bigint")


class ModelMetaclass(type):
    """
        元类, 绑定对象-关系映射
    """

    def __new__(mcs, name, bases, attrs):
        """
            创建类
        :param name: 类名
        :param bases: 父类
        :param attrs: 属性
        :return: 创建后的类
        """
        # 类名 == Model
        if name == "Model":
            # 直接调用父类创建类
            return type.__new__(mcs, name, bases, attrs)
        # 输出提示
        print("当前类名:", name)
        # 创建 对象-关系 映射字典
        mappings = {}
        # 循环当前类的属性
        for k, v in attrs.items():
            # 如果属性是Field类
            if isinstance(v, Field):
                # 输出提示
                print("创建 对象-关系 映射: %s ==> %s" % (k, v))
                # 绑定 对象=关系
                mappings[k] = v
        # 循环保存好的 对象-关系
        for k in mappings.keys():
            # 删除原类中的属性
            attrs.pop(k)
        # 自定义 对象-关系 属性
        attrs["__mappings__"] = mappings
        # 自定义类名 = 表名
        attrs["__table__"] = name
        # 调用父类创建自定义后的类
        return type.__new__(mcs, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    """
        属性生成类
    """

    def __init__(self, **kwargs):
        # 调用父类初始化
        super(Model, self).__init__(**kwargs)

    def __getattr__(self, key):
        """
            get属性
        :param key: 键 -- 对象
        :return: 数据 -- 关系
        """
        # 捕获异常
        try:
            # 返回数据
            return self[key]
        except KeyError:
            # 抛出属性异常, 当前类中不存在此属性
            raise AttributeError("'Model' 类中没有此属性 '%s'" % key)

    def __setattr__(self, key, value):
        """
            set属性
        :param key: 键 -- 对象
        :param value: 值 -- 关系
        :return:
        """
        self[key] = value

    def save(self):
        """
            保存数据库
        :return:
        """
        # 字段
        fields = []
        # 数据
        args = []
        # 循环 对象-关系
        for k, v in self.__mappings__.items():
            # 添加字段,
            fields.append(v.name)
            # 添加数据
            args.append(getattr(self, k, None))
        # 拼接SQL语句, 转化args 确保所有数据都是字符串
        sql = "insert info %s (%s) values (%s)" % (self.__table__, ",".join(fields), ",".join([str(i) for i in args]))
        # 输出提示
        print("SQL:", sql)
        # 输出提示
        print("字段:", fields)
        # 输出提示
        print("数据:", args)


class User(Model):
    # 定义属性-字段
    id = IntegerField("id")
    name = StringField("username")
    email = StringField("email")
    password = StringField("password")

    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password


u = User(id=123456, name="小明", email="xiaoming@163.com", password="123456")
u.save()
