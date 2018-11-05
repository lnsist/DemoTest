"""

date: 2018-09-22 10:51
"""
# gevent协程库
import gevent
# gevent打补丁库 -- 用以将原系统的耗时操作兼容gevent耗时操作
from gevent import monkey
import time


def fn():
    # 循环3次 -- 3秒
    for i in range(3):
        # 工作
        print("我工作1秒钟")
        # 耗时 1 秒
        time.sleep(1)


def main():
    # 打补丁, 让gevent兼容系统耗时操作
    monkey.patch_all()
    # 协程1
    g1 = gevent.spawn(fn)
    # 协程2
    g2 = gevent.spawn(fn)
    # 协程3
    g3 = gevent.spawn(fn)
    # 同时开启协程, 并阻塞主线程
    gevent.joinall([g1, g2, g3])


if __name__ == '__main__':
    main()
