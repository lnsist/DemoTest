"""
基于TCP协议的服务端socket -- 多人聊天室
"""
import socket
import select

addr = ("", 1688)
# 对话输入
inputs = []
# 客户端名字
fd_name = {}


# 谁在聊天室
def who_in_room(w):
    name_list = []
    for k in w:
        name_list.append(w[k])

    return name_list


# tcp初始化
def conn():
    ss = socket.socket()
    ss.bind(addr)
    ss.listen(5)

    return ss


# 客户端访问
def new_coming(ss):
    # 获取客户端地址, 并生成一个对话socket
    client, add = ss.accept()
    # 欢迎
    print('欢迎你 %s %s' % (client, add))
    # 欢迎语句
    wel = "欢迎加入聊天室.\n请输入你的名字....."
    try:
        # 发送欢迎语句
        client.send(wel.encode("utf-8"))
        # 获取对方名字
        name = client.recv(1024).decode("utf-8")
        # 添加客户端
        inputs.append(client)
        # 添加客户端名字
        fd_name[client] = name
        # 返回当前聊天室内的姓名
        nameList = "已经有人在聊天室内, 他们名字是 %s" % (who_in_room(fd_name))
        client.send(nameList.encode("utf-8"))

    except Exception as e:
        print(e)


# 服务器运行
def server_run():
    # 初始化
    ss = conn()
    # 加入输出列表
    inputs.append(ss)
    # 无限循环, 聊天室
    while True:
        # 动态监听socket
        r, w, e = select.select(inputs, [], [])
        # 获取当前socket
        for temp in r:
            # 如果是服务器
            if temp is ss:
                # 进行添加新客户端
                new_coming(ss)
            else:
                # 获取聊天内容
                data = temp.recv(1024).decode("utf-8")
                if data:
                    # 拼接当前客户端发送的信息
                    data = "[%s]\n发送消息 : %s" % (fd_name[temp], data)
                else:
                    # 已退出聊天室
                    data = fd_name[temp] + ' 退出聊天室'
                    # 已下线
                    # 移除次客户端
                    inputs.remove(temp)
                    # 移除此客户端
                    del fd_name[temp]
                # 将接受到的消息发送给所有客户端
                for other in inputs:
                    # 不是服务器, 并且不是当前退出聊天室的socket
                    if other != ss:
                        try:
                            # 发送消息
                            other.send(data.encode("utf-8"))
                        except Exception as e:
                            print(e)


if __name__ == '__main__':
    server_run()
