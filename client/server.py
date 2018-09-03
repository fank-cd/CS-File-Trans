# -*- coding: UTF-8 -*-

import socket
from time import ctime
import threading
import os
import hashlib
import time

tcp_ser_socket = socket.socket()
HOST = socket.gethostname()
PORT = 12345
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcp_ser_socket.bind(ADDR)
tcp_ser_socket.listen(5)
"""
print "等待连接"

while True:
    print '连接地址：', client_address
    if count is 0:
        tcp_client_socket.send('欢迎访问！')
    data = tcp_client_socket.recv(BUFSIZ)
    if not data:
        break
    tcp_client_socket.send(data)
    count += 1
tcp_client_socket.close()
tcp_ser_socket.close()
"""
socks = []


def get_md5_file():
    path = 'E:\\exercise project\\TCP_clientserver\\server'
    path_list = []
    file_md5 = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filepath in filenames:
            path_list.append(os.path.join(dirpath, filepath))

    #print path_list
    for i in range(len(path_list)):
        try:
            md5file = open(path_list[i], 'rb')
            file_md5.append(hashlib.md5(md5file.read()).hexdigest())
            md5file.close()
        except IOError:
            print "文件读取错误"

    print file_md5

def handle():

    while True:
        for s in socks:
            try:
                data = s.recv(BUFSIZ)
            except Exception, e:
                continue
            if not data:
                socks.remove(s)
                continue
            s.send('[%s]:%s' % (ctime(), data))


t = threading.Thread(target=handle)

if __name__ == '__main__':
    """
    t.start()
    print '我在%s线程中' % threading.current_thread().name
    print "waiting"
    while True:
        tcp_client_socket, client_address = tcp_ser_socket.accept()
        print client_address
        tcp_client_socket.setblocking(0)
        socks.append(tcp_client_socket)
    """
    get_md5_file()
