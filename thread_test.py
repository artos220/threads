import threading
from random import random
from time import sleep

BUFFER_LEN = 10
msg_buffer = []
cv = threading.Condition()


def get_msg():
    return int(random()*10)


def make_an_item_available(msg):
    msg_buffer.append(msg)


def slot_is_available():
    if len(msg_buffer) < BUFFER_LEN:
        return True


# Produce one item
def produce():
    with cv:
        while not slot_is_available():
            cv.wait()
        make_an_item_available(get_msg())
        cv.notify()


def an_item_is_available():
    if len(msg_buffer):
        return True


def get_an_available_item():
    return msg_buffer.pop(0)


# Consume one item
def consume():
    with cv:
        while not an_item_is_available():
            cv.wait()
        get_an_available_item()
        cv.notify()


def loop_consume():
    while True:
        consume()
        print(f'- buffer {len(msg_buffer)}: {msg_buffer}')
        sleep(random()+1)


def some_produce():
    for i in range(100):
        produce()
        print(f'+ buffer {len(msg_buffer)}: {msg_buffer}')
        sleep(random())


c = threading.Thread(target=loop_consume)
c.start()

p = threading.Thread(target=some_produce)
p.start()

c2 = threading.Thread(target=loop_consume)
c2.start()

p2 = threading.Thread(target=some_produce)
p2.start()
