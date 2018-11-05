"""
    udp广播服务端
"""
import socket


def main():
    # 创建一个 网络通讯的 udp socket
    udp_broad_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 添加开启广播
    udp_broad_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
    while True:
        # 输入需要发送的广播
        send_data = input("请输入需要发送的广播信息(直接回车取消发送): ")
        if not send_data:
            break
        # 发送广播
        udp_broad_socket.sendto(send_data.encode("utf-8"), ("<broadcast>", 16898))

    # 关闭
    udp_broad_socket.close()

if __name__ == '__main__':
    main()
