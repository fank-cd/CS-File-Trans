# -*- coding: UTF-8 -*-

import socket
import threading
import os
import hashlib
import time
import struct

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

md5_path = 'E:\\exercise project\\TCP_clientserver\\server_md5.txt'
path = 'E:\\exercise project\\TCP_clientserver\\server'
path_list = []


def get_md5_file():

    file_md5 = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filepath in filenames:
            path_list.append(os.path.join(dirpath, filepath))

    # print path_list
    for i in range(len(path_list)):
        try:
            md5file = open(path_list[i], 'rb')
            file_md5.append(hashlib.md5(md5file.read()).hexdigest())
        except IOError:
            print "文件读取错误"
        finally:
            md5file.close()

    # print file_md5
    with open(md5_path, 'w') as f:
        for i in range(len(file_md5)):
            f.write(file_md5[i]+'\n')


def file_trans(sock, addr):
    file_number = len(path_list)
    print 'Accept new connection from %s:%s...' % addr
    sock.send('Welcome!')
    client_md5 = sock.recv(1024)
    # print client_md5

    with open(md5_path, 'rb') as md5:
        server_md5 = md5.read()
    # print server_md5
    if server_md5 != client_md5:
        print 2333
        sock.send('different')
        sock.send(str(file_number))
        while True:
            for i in range(file_number):
                if os.path.isfile(path_list[i]):
                    fileinfo_size = struct.calcsize('128sl')
                    fhead = struct.pack('128sl', os.path.basename(path_list[i]),
                                        os.stat(path_list[i]).st_size)
                    sock.send(fhead)
                    print 'client filepath: {0}'.format(path_list[i])

                    with open(path_list[i], 'rb') as fp:
                        while True:
                            data = fp.read(5120)
                            if not data:
                                print '{0} file send over...'.format(path_list[i])
                                break
                            sock.send(data)

            data = sock.recv(1024)
            time.sleep(1)

            if data == 'exit' or not data:
                break
    sock.close()
    print 'Connection from %s:%s closed.' % addr


if __name__ == '__main__':

    HOST = socket.gethostname()
    PORT = 12345
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    get_md5_file()
    tcp_ser_socket = socket.socket()
    tcp_ser_socket.bind(ADDR)
    tcp_ser_socket.listen(5)
    print '我在%s线程中' % threading.current_thread().name
    print "waiting"
    while True:
        tcp_client_socket, client_address = tcp_ser_socket.accept()
        t = threading.Thread(target=file_trans, args=(tcp_client_socket, client_address))
        t.start()
