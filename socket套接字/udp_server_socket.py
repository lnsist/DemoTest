"""
    udp服务端
"""
import socket


def main():
    # 创建一个 网络通讯的 udp socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 绑定端口
    udp_socket.bind(("", 1688))
    while True:
        # 接收信息
        recv_data = udp_socket.recvfrom(1024)
        # 输入接收到的信息
        print("来自 %s 发送的信息: %s" % (recv_data[1], recv_data[0].decode("utf-8")))
        # 自动回复
        udp_socket.sendto("欢迎光临".encode("utf-8"), recv_data[1])
    # 关闭
    udp_socket.close()


if __name__ == '__main__':
    main()
