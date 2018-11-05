"""简单的http服务器，每次浏览器请求都会返回 "register.html"的内容

date: 2018-09-21 16:08
"""
import socket


def main():
    # 创建tcp socket服务端
    tcp_socket = socket.socket()
    # 设置端口复用
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 绑定端口
    tcp_socket.bind(("", 1688))
    # 监听
    tcp_socket.listen(128)
    # 死循环监听
    while True:
        # 获取客户端地址 和返回通信socket
        new_socket, client_addr = tcp_socket.accept()
        # 新客户端访问提示
        print("有新的客户访问, 地址为:", client_addr)
        # 只要有请求就返回"register.html"的内容
        # 获取网页内容
        with open("register.html", "rb") as f:
            # 拼接响应报文
            # 响应行
            response_line = "HTTP/1.1 200 OK\r\n"
            # 响应头
            response_headers = "Server: mini-webserver 1.0\r\n"
            response_headers += "Content-Type: text/html;charset=utf-8\r\n"
            response_headers += "Major: python\r\n"
            # 空行
            response_split = "\r\n"
            # 响应体
            response_body = f.read()

            # 拼接响应报文
            response_data = response_line + response_headers + response_split
            # 发送响应报文 -- 网页内容
            new_socket.send(response_data.encode("utf-8") + response_body)
    # 关闭连接 -- 短连接
    new_socket.close()
    # 监听socket关闭
    tcp_socket.close()


if __name__ == '__main__':
    main()
