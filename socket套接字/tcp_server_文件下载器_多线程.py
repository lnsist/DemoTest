"""
基于TCP协议的服务端socket, 文件下载器
"""
import socket
import threading


# 我的socket线程
class MySocketThread(threading.Thread):
    def __init__(self, new_socket, client_addr):
        super().__init__
        self.new_socket = new_socket
        self.client_addr = client_addr

    # 根据文件名查询文件并返回
    @staticmethod
    def find_file_name(file_name):
        # 捕捉异常, 是否存在此文件
        try:
            # 查询是否存在此文件名
            with open(file_name, "r") as f:
                # 返回内容
                print("请求下载的文件名为:", file_name)
                return f.read()
        # 异常处理
        except Exception as e:
            print("不存在此文件:", file_name)
            print(e)
            return "False"

    def run(self):
        # 无限回复, 直到客户端关闭
        while True:
            # 等待接收信息
            new_recv = self.new_socket.recv(1024)
            # 判断内容为空则跳出循环, 结束通讯
            if not new_recv:
                # 退出提示
                print("通讯已结束, socket已关闭")
                # socket关闭
                self.new_socket.close()
                break
            # 转码获取文件名
            file_name = new_recv.decode("utf-8")
            # 查询文件并发送
            self.new_socket.send(self.find_file_name(file_name).encode("utf-8"))


def main():
    # 初始化socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定端口
    tcp_socket.bind(("", 1688))
    # 设置端口复用
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # 开启监听
    tcp_socket.listen(5)
    # 无限等待接受信息
    while True:
        # 等待客户端访问
        new_socket, client_addr = tcp_socket.accept()
        # 访问通知
        print("有新的客户端访问:", client_addr)
        # 自动回复, 文件列表
        data_str = """欢迎光临, 文件下载服务器....
服务器现有文件有以下列表:
A.txt
B.txt
C.txt
D.txt
E.txt
请回复需要下载的文件名
"""
        new_socket.send(data_str.encode("utf-8"))

        my_s_t = MySocketThread(new_socket, client_addr)
        my_s_t.run()


if __name__ == '__main__':
    main()
