"""
基于TCP协议的客户端socket
"""
import socket


def main():
    # 创建基于网络通信的 TCP socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 请求连接
    tcp_socket.connect(("127.0.0.1", 1688))
    # 输入需要发送的信息
    send_data = input("请输入需要发送的信息: ")
    # 转码发送信息
    tcp_socket.send(send_data.encode("utf-8"))
    # 接收信息
    recv_data = tcp_socket.recv(1024)
    # 转码输出接收到的信息
    print("接收到的信息:", recv_data.decode("utf-8"))
    # 关闭socket
    tcp_socket.close()


if __name__ == '__main__':
    main()
