"""
    第三方平台验证服务 - 超级鹰
date: 18-10-10 上午10:27
"""
import requests
from hashlib import md5


class Chaojiying_Client(object):
    """
        第三方平台验证服务 - 超级鹰
    """

    def __init__(self, username, password, soft_id):
        """
            初始化属性
        :param username: 用户名
        :param password: 密码
        :param soft_id: 软件ID
        """
        # 用户名
        self.username = username
        # 密码转码
        password = password.encode('utf8')
        # 密码md5加密
        self.password = md5(password).hexdigest()
        # 软件ID
        self.soft_id = soft_id
        # 请求参数字典
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        # 请求头
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
            访问服务器, 提交验证码图片 和 验证类型
        :param im: 图片字节
        :param codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        :return 返回服务器的响应
        """
        # 请求参数
        params = {
            # 验证类型
            'codetype': codetype,
        }
        # 更新参数字典
        params.update(self.base_params)
        # 请求文件
        files = {'userfile': ('ccc.jpg', im)}
        # 服务器访问
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        # 返回服务器响应
        return r.json()

    def ReportError(self, im_id):
        """
            提交报错 - 如果返回的响应中, 验证码错误, 提交此错误, 返回用户分数
        :param im_id:报错题目的图片ID
        """
        # 请求参数
        params = {
            # 报错图片id
            'id': im_id,
        }
        # 跟新请求参数
        params.update(self.base_params)
        # 服务器访问
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        # 返回服务器响应
        return r.json()


if __name__ == '__main__':
    # 用户中心>>软件ID 生成一个替换 96001
    chaojiying = Chaojiying_Client('超级鹰用户名', '超级鹰用户名的密码', '96001')
    # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    im = open('a.jpg', 'rb').read()
    # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    print(chaojiying.PostPic(im, 1902))
