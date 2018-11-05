"""
基于TCP协议的服务端socket
"""
import socket


def main():
    # 创建基于网络通信的 TCP socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置端口复用性
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定端口
    tcp_socket.bind(("", 1688))
    # 设置队列最大值
    tcp_socket.listen(5)
    while True:
        # 开启监听, 并返回新的socket主要用于通信, 以及对方的地址
        new_socket, clien_addr = tcp_socket.accept()
        # 提示客户端请求
        print("有新的客户端请求, 来自-->", clien_addr)
        while True:
            # 获取信息
            recv_data = new_socket.recv(1024)
            # 判断客户端是否已下线
            if not recv_data:
                break
            # 转码输出获取到的信息
            print("接收到的信息:", recv_data.decode("utf-8"))
            # 自动回复
            new_socket.send("欢迎光临".encode("utf-8"))
        new_socket.close()
    tcp_socket.close()


if __name__ == '__main__':
    main()
