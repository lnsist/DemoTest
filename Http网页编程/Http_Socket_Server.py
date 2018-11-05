"""Http服务器socket版

date: 2018-09-22 15:38
"""
import socket
import threading
import multiprocessing
import gevent
from gevent import monkey


# http服务器
class HttpServer(object):
    # 文件目录
    http_path = "./static"

    # 初始化
    def __init__(self):
        # gevent打补丁, 兼容系统
        monkey.patch_all()
        # 创建socket
        self.http_socket = socket.socket()
        # 设置端口复用
        self.http_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 设置端口
        self.http_socket.bind(("", 1688))
        # 监听
        self.http_socket.listen(128)

    # 服务器运行
    def start(self):
        # 等待访问
        print("等待客户端访问")
        # 死循环监听
        while True:
            # 获取访问客户端地址, 返回新的对话socket
            new_socket, client_addr = self.http_socket.accept()
            print("有新的客户端访问:", client_addr)
            # 单任务
            # self.send_http(new_socket)

            # 多线程
            # threading.Thread(target=self.send_http, args=(new_socket,)).start()

            # 多进程
            # multiprocessing.Process(target=self.send_http, args=(new_socket,)).start()
            # 多进程 -- 主线程的new_socket需要关闭
            # new_socket.close()

            # 多协程
            gv = gevent.spawn(self.send_http, new_socket)
            # 阻塞, 运行完后解阻塞
            gevent.joinall([gv])
        # 服务器socket关闭
        self.tcp_socket.close()

    @staticmethod
    def send_http(new_socket):
        # 获取访问而信息 -- 请求报文
        recv_data = new_socket.recv(1024 * 1024).decode("utf-8")
        # 判断浏览器是否关闭访问
        if not recv_data:
            print("浏览器已关闭")
            # 关闭socket
            new_socket.close()
            # 退出方法
            return
        # 输出请求报文
        print("请求报文:", recv_data)
        # 根据\r\n切割每一行信息
        recv_lines = recv_data.split("\r\n")
        # 初始化字典
        recv_dic = {}
        # 单独获取请求行
        request_line = recv_lines[0].split(" ")
        # 添加请求行字典信息
        # 请求方法
        recv_dic["method"] = request_line[0]
        # 请求路径
        recv_dic["request_path"] = request_line[1]
        # 协议版本
        recv_dic["http_version"] = request_line[2]
        # 除请求行, 循环每行信息, 封装字典
        for line in recv_lines[1:]:
            # 以 ":" 切割
            line_sl = line.split(":")
            # 拼接请求报文value
            value_sl = ""
            # 循环添加字典
            for sl in line_sl[1:]:
                value_sl += ":" + sl if len(value_sl) > 0 else sl
            # 以切割后下标 0 为字典 key, 下标1 为字典 value
            recv_dic[line_sl[0]] = value_sl
        print(recv_dic)
        # 发送响应报文
        HttpServer.send_response(new_socket, recv_dic)

    @staticmethod
    def send_response(new_socket, recv_dic):
        # 拼接响应报文
        # 响应行
        response_line = "HTTP/1.1 200 OK\r\n"
        # 响应头
        response_headers = 'Server: mini-webserver 1.0\r\n'
        response_headers += "Content-Type: text/html;charset=utf-8\r\n"
        # 获取请求路径, 判断是否404 拼接响应体
        request_path = recv_dic["request_path"]
        # 判断是否根目录, 拼接响应体文件
        if request_path == "/":
            # 访问index网页
            request_path = "/index.html"
        # 捕抓异常, 访问网页不存在, 404报错
        try:
            # 获取请求路径网页源代码
            with open(HttpServer.http_path + request_path, "rb") as f:
                response_body = f.read()
        except Exception as e:
            print(e)
            # 响应行, 404报错
            response_line = "HTTP/1.1 404 Not Found\r\n"
            # 响应体
            response_body = "<a href='http://www.douyu.com/directory/game/yz'><img src='images/404.jpg'/></a>" \
                .encode("utf-8")
        # 响应客户端, 返送消息
        new_socket.send((response_line + response_headers + "\r\n").encode("utf-8") + response_body)
        # 关闭回话socket -- 线程不能关闭socket
        new_socket.close()


def main():
    # 创建Http服务器
    http_server = HttpServer()
    # 启动Http服务器
    http_server.start()


if __name__ == '__main__':
    main()
