"""
    udp广播客户端
"""
import socket


def main():
    # 创建一个 用于广播网络通讯的 udp socket
    udp_broad_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 添加开启广播
    udp_broad_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
    # 绑定端口
    udp_broad_socket.bind(("", 16898))
    # 接受广播, 并显示广播信息
    while True:
        recv_data, addr = udp_broad_socket.recvfrom(1024)
        print("接收到的广播信息:", recv_data.decode("utf-8"))
    # 关闭
    udp_broad_socket.close()

if __name__ == '__main__':
    main()
