"""
基于TCP协议的客户端socket, 文件下载器
"""
import socket


# 接收信息
import threading


# 等待返回信息线程类
class TcpRecvThread(threading.Thread):
    def __init__(self, tcp_socket, file_name):
        self.tcp_socket = tcp_socket
        self.file_name = file_name

    def run(self):
        # 无限等待接收信息
        while True:
            # 等待接收信息
            recv_data = self.tcp_socket.recv(1024)
            # 如果返回的结果为空, 跳出循环
            if recv_data.decode("utf-8") == "False":
                print("%s 文件不存在, 请重新输入" % self.file_name)
                break
            # 结果不为空则写出此文件
            with open("/home/python/Desktop/" + self.file_name, "wb") as f:
                f.write(recv_data)
            # 提示成功
            print("文件 %s 已下载成功" % self.file_name)
            break


def main():
    # 创建基于网络通信的 TCP socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 请求连接
    tcp_socket.connect(("127.0.0.1", 1688))
    # 接收信息
    recv_data = tcp_socket.recv(1024)
    # 转码输出接收到的信息
    print("接收到的信息\n", recv_data.decode("utf-8"))
    while True:
        # 输入需要下载的文件名
        send_data = input("请输入需要下载的文件名(直接回车退出): ")
        # 如果输入的信息为空, 则跳出循环
        if not send_data:
            break
        # 转码发送信息
        tcp_socket.send(send_data.encode("utf-8"))
        # 创建等待返回信息线程
        my_thread = TcpRecvThread(tcp_socket, send_data)
        # 开启线程
        my_thread.run()

    # 关闭socket
    tcp_socket.close()

if __name__ == '__main__':
    main()
