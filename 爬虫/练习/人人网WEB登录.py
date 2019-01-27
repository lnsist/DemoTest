"""WEB端人人网登录
TODO: 未完成, WEB端的密码加密未实现
人人网进入登陆界面后, 会自动访问后台获取rKey,
这个rKey登陆的时候需要携带,
登陆接口需要uniqueTimestamp参数, 值是js脚本生成拼接的的时间戳


# 人人网rKey接口
rKey_url = "http://login.renren.com/ajax/getEncryptKey"
# 人人网登陆接口
login_url = "http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp=2019052223167"

人人网登陆请求体
email: 13318766890
icode:
origURL: http://www.renren.com/home
domain: renren.com
key_id: 1
captcha_type: web_login
password: 5df45d04afea612b298d9eb9a69d8d46f02ffbefde45a6841d1c8dc180b36b0f
rkey: 15b278a5ab08b5f892df83c257aaa1a1
f:

@Date    : 2019-01-25 21:56
@Author  : lnsist
"""
import requests
import js2py


class RenRenLoginSpider(object):
    def __init__(self):
        """人人网登陆爬虫 初始化"""
        # 获取rkey接口
        self.rKey_url = "http://login.renren.com/ajax/getEncryptKey"
        # 人人网登陆接口
        self.login_url = "http://www.renren.com/ajaxLogin/login?1=1&uniqueTimestamp={}"
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36"
        }
        self.session = requests.session(headers=self.headers)

    def get_page_form_url(self, url, data=None, headers=None):
        """根据url获取请求响应

        :param url: url
        :param data: 请求体
        :param headers: 请求头
        :return: 返回请求响应
        """
        # 如果有请求体, post请求体
        if data:
            # 发送请求
            response = requests.post(url=url, data=data, headers=headers)
        # 没有请求体
        else:
            # 发送请求
            response = requests.get(url=url, headers=headers)
        # 返回请求响应
        return response

    def get_uniqueTimestamp(self):
        # js脚本
        js_str = """
        var s = new Date;
        var e = "" + s.getFullYear() + s.getMonth() + s.getDay() + s.getHours() + s.getSeconds() + s.getUTCMilliseconds();
        """
        # 实例js2py 初始化环境
        context = js2py.EvalJs()
        # 执行js脚本
        context.execute(js_str)
        # 返回拼接的时间戳
        return context.e

    def get_encrypt_password(self):
        # js脚本
        js_str = """
        function n(i) {
            for (var t = new Array, n = i.length, o = 0; n > o; )
                t[o] = i.charCodeAt(o),
                o++;
            for (; t.length % T.chunkSize != 0; )
                t[o++] = 0;
            var s, r, a, l = t.length, c = "";
            for (o = 0; l > o; o += T.chunkSize) {
                for (a = new d,
                s = 0,
                r = o; r < o + T.chunkSize; ++s)
                    a.digits[s] = t[r++],
                    a.digits[s] += t[r++] << 8;
                var u = T.barrett.powMod(a, T.e)
                  , g = 16 == T.radix ? p(u) : f(u, T.radix);
                c += g + " "
            }
            return c.substring(0, c.length - 1)
        }
        var pw = n(b)
        """
        # 实例js2py 初始化环境
        context = js2py.EvalJs()
        # 执行js脚本
        context.execute(self.load_js_from_url("http://s.xnimg.cn/a89037/nx/apps/login/login.js"))
        # 设置
        context.a = ""
        # 设置密码
        context.b = "a1234567890"
        # 执行js脚本
        context.execute(js_str)
        # 返回拼接的时间戳
        return context.pw

    def load_js_from_url(self, url):
        """根据url获取js脚本

        :param url: url
        :return: js脚本
        """
        # 请求访问获取js脚本
        js_str = self.get_page_form_url(url=url, headers=self.headers).content.decode()
        # 返回js脚本
        return js_str

    def run(self):

        # 请求获取rKey
        rKey_url_response = self.get_page_form_url(url=self.rKey_url, headers=self.headers)
        # 获取时间戳
        uniqueTimestamp = self.get_uniqueTimestamp()
        # 拼接生成login_url
        self.login_url = self.login_url.format(uniqueTimestamp)
        # 组合请求体
        data = {
            "email": "13318766890",
            "icode": "",
            "origURL": "http://www.renren.com/home",
            "domain": "renren.com",
            "key_id": "1",
            "captcha_type": "web_login",
            "password": self.get_encrypt_password(),
            "rkey": rKey_url_response.content.decode(),
            "f": ""
        }
        # 发送登陆请求
        # login_response = self.get_page_form_url(url=self.login_url, data=data, headers=self.headers)


if __name__ == '__main__':
    renren = RenRenLoginSpider()
    renren.run()
