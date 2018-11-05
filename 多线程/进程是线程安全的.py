"""进程是线程安全的
因为他的机制问题, 数据不共享, 只能通过消息队列传递数据,
然而也是因为消息队列的特性, 消息唯一,
如进程A 发送消息消息队列有消息, 进程B 获取消息后, 消息队列中就没有消息了,
从而不会存在多个进程同时拥有同一数据进行操作

date: 2018-09-18
"""
import threading
import multiprocessing

t_num = 0


def fn1(n, queue):
    q_num = get_queue(queue)
    for i in range(n):
        q_num += 1
    put_queue(queue, q_num)


def put_queue(queue, q_num):
    queue.put(q_num)


def get_queue(queue):
    return queue.get()


def main():
    # t1 = threading.Thread(target=fn1, args=(1000000,))
    # t2 = threading.Thread(target=fn1, args=(1000000,))
    #
    # t1.start()
    # t2.start()
    #
    # t1.join()
    # t2.join()

    queue = multiprocessing.Queue(5)
    put_queue(queue, t_num)
    p1 = multiprocessing.Process(target=fn1, args=(1000000, queue))
    p2 = multiprocessing.Process(target=fn1, args=(1000000, queue))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("最终结果:", get_queue(queue))


if __name__ == '__main__':
    main()
