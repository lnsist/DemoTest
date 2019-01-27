"""人人网移动登陆

@Date    : 2019-01-26 16:44
@Author  : lnsist
"""

import requests
import json
import js2py


class RenrenLoginSpider(object):
    """人人网移动登陆爬虫

    """

    def __init__(self):
        """初始化"""

        # 实例化session对象
        self.session = requests.session()
        # 给session设置请求头
        self.session.headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Mobile Safari/537.36"
        }
        # 登录的URL
        self.clog_url = 'http://activity.renren.com/livecell/ajax/clog'
        # rkey的URL
        self.rkey_url = 'http://activity.renren.com/livecell/rKey'
        # 创建执行js的环境
        self.context = js2py.EvalJs()

    def get_data_from_url(self, url, data=None):
        """发送请求, 获取二进制数据"""

        # 如果请求体为空 -- get请求
        if data is None:
            # 发送get请求, 获取响应
            response = self.session.get(url)
        # 请求体不为空 -- post请求
        else:
            # 发送post请求, 获取响应
            response = self.session.post(url, data=data)
        # 返回请求响应
        return response.content

    def load_js_from_url(self, url):
        """通过URL执行js,也就是加载js"""

        # 根据url获取js脚本
        js = self.get_data_from_url(url).decode()
        # js环境添加js脚本
        self.context.execute(js)

    def run(self):
        # 发送rkey请求, 获取加密需要使用的数据
        result = self.get_data_from_url(self.rkey_url)
        # 解析数据
        n = json.loads(result)['data']

        # 使用js2py创建js的执行环境
        # 让js执行环境加载相关js的文件
        self.load_js_from_url('http://s.xnimg.cn/a85738/wap/mobile/wechatLive/js/RSA.js')
        self.load_js_from_url('http://s.xnimg.cn/a85738/wap/mobile/wechatLive/js/BigInt.js')
        self.load_js_from_url('http://s.xnimg.cn/a86836/wap/mobile/wechatLive/js/celllog.js')
        self.load_js_from_url('http://s.xnimg.cn/a85738/wap/mobile/wechatLive/js/Barrett.js')
        # 给js执行环境设置需要的数据
        self.context.t = {
            'phoneNum': '13318766890',
            'password': 'a1234567890'}
        # 设置rKey数据
        self.context.n = n
        # 生成登录数据js代码
        js = """
                t.password = t.password.split("").reverse().join(""),
                setMaxDigits(130);
                var o = new RSAKeyPair(n.e,"",n.n)
                , r = encryptedString(o, t.password);
                t.password = r,
                t.rKey = n.rkey
            """

        # 执行js, 获取发送登录需要的数据
        self.context.execute(js)
        # 获取js执行后的数据
        print(self.context.t)
        # 设置data发送登陆请求
        result = self.get_data_from_url(self.clog_url, data=self.context.t.to_dict())
        # 解析响应
        result = json.loads(result)
        # 　输出
        print(result)
        # 使用登录的session访问其他资源
        data = self.get_data_from_url('http://activity.renren.com/myprofile')
        print(data.decode())


if __name__ == '__main__':
    rrls = RenrenLoginSpider()
    rrls.run()
