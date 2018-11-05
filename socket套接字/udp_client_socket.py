"""
    udp客户端
"""
import socket


def main():
    # 创建一个 网络通讯的 udp socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 录入需要发送的信息
    str_data = input("请输入需要发送的信息: ").encode("utf-8")
    # 发送信息
    udp_socket.sendto(str_data, ("127.0.0.1", 1688))
    # 接受信息
    recv_data = udp_socket.recvfrom(1024)[0].decode("utf-8")
    # 输出接受的信息
    print("接受到的信息:", recv_data)
    # 关闭
    udp_socket.close()


if __name__ == '__main__':
    main()
