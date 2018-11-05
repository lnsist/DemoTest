"""
    mini_web框架, TCP -- 协程
date: 18-10-9 下午4:51
"""
import socket
import gevent
from gevent import monkey

# mini_web
from Http网页编程 import mini_frame


class MiniWeb(object):
    # 文件目录
    http_path = "./static"

    #

    # 初始化
    def __init__(self):
        # gevent打补丁, 兼容系统
        monkey.patch_all()
        # 创建socket
        self.http_socket = socket.socket()
        # 设置端口复用
        self.http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 帮顶端口
        self.http_socket.bind(("", 1688))
        # 监听
        self.http_socket.listen(128)

    def start(self):
        """
            启动服务器
        :return:
        """
        # 输出提示
        print("开启服务器, 等待客户端访问")
        # 死循环监听
        while True:
            # 客户端访问
            new_socket, client_addr = self.http_socket.accept()
            # 输出提示
            print("有新的客户端访问:", client_addr)
            # 多协程
            gevent.joinall([gevent.spawn(self.send_http, new_socket)])

    @staticmethod
    def send_http(new_socket):
        """
            发送响应 -- 真正和客户端交互
        :return:
        """
        # 模拟创建, 方便快捷提示
        # new_socket = socket.socket()
        # 等待请求并解码
        recv_data = new_socket.recv(1024 * 1024).decode("utf-8")
        # 判断是否关闭访问
        if not recv_data:
            # 输出提示
            print("客户端已断开访问")
            # 关闭socket
            new_socket.close()
            # 退出方法
            return
        # 输出请求报文
        print("客户端请求报文:", recv_data)
        # 解析请求报文, 初始化字典
        recv_dic = {}
        # \r\n切割信息
        recv_lines = recv_data.split("\r\n")
        # 获取请求行
        request_line = recv_lines[0].split(" ")
        # 字典添加信息, 请求方法
        recv_dic["method"] = request_line[0]
        # 请求路径
        recv_dic["request_path"] = request_line[1]
        # 协议版本
        recv_dic["http_version"] = request_line[2]
        # 循环获取请求头信息, 除去第一行
        for line in recv_lines[1:]:
            # 以 ":" 切割
            line_sl = line.split(":")
            # 拼接请求报文
            value_sl = ""
            # 第一个是key, 之后的是values, key只有一个, values有多个需要拼接
            for sl in line_sl[1:]:
                # 拼接
                value_sl += ":" + sl if len(value_sl) > 0 else sl
            # 添加至字典中
            recv_dic[line_sl[0]] = value_sl
        # 发送响应报文
        MiniWeb.send_response(new_socket, recv_dic)

    @staticmethod
    def send_response(new_socket, recv_dic):
        # 获取请求路径, 判断是否404 拼接响应体
        request_path = recv_dic["request_path"]
        # 判断是否根目录, 拼接响应体文件
        if request_path == "/":
            # 访问index网页
            request_path = "/index.html"

        # 如果是动态数据, 交给web框架操作 -- 后缀为.html即为动态数据
        if request_path.endswith(".html"):
            # 传递网址
            env = {"PATH_INFO": request_path}
            # 动态数据
            status, response_body = mini_frame.main(env)
        else:
            # 静态数据
            status, response_body = MiniWeb.static_data(request_path)

        # 拼接响应报文, 响应行
        response_line = "HTTP/1.1 " + status + "\r\n"
        # 响应头
        response_headers = 'Server: mini-webserver 1.0\r\n'
        response_headers += "Content-Type: text/html;charset=utf-8\r\n"

        # 响应客户端, 返送消息
        new_socket.send((response_line + response_headers + "\r\n").encode("utf-8") + response_body)
        # 关闭回话socket -- 线程不能关闭socket
        new_socket.close()

    @staticmethod
    def static_data(request_path):
        """
            静态数据返回
        :param request_path:
        :return:
        """
        # 状态码
        status = " 200 OK"
        # 捕抓异常, 访问网页不存在, 404报错
        try:
            # 获取请求路径网页源代码 -- 可能会是图片, 需要二进制读取文件
            with open(MiniWeb.http_path + request_path, "rb") as f:
                response_body = f.read()
        except Exception as e:
            print(e)
            # 响应行, 404报错
            status = "404 Not Found"
            # 响应体
            response_body = "<a href='http://www.douyu.com/directory/game/yz'><img src='images/404.jpg'/></a>".encode(
                "utf-8")
        return status, response_body


def main():
    # 创建Http服务器
    mini_web = MiniWeb()
    # 启动Http服务器
    mini_web.start()


if __name__ == '__main__':
    main()
