#!/usr/bin/env python
# coding:utf-8

import select
import socket
import Queue
import hashlib
import os
import struct
import time
path_list = []
md5_path = 'E:\\exercise project\\TCP_clientserver\\server_md5.txt'


def get_md5_file():
    path = 'E:\\exercise project\\TCP_clientserver\\server'
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


if __name__ == '__main__':
    print("正在更新md5值")
    get_md5_file()
    with open(md5_path, 'rb') as md5:
        server_md5 = md5.read()
    print("md5 is \n%s" % server_md5)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)

    server_address = ('localhost', 1000)
    print('starting up on %s port %s' % server_address)
    server.bind(server_address)
    server.listen(5)
    inputs = [server, ]
    outputs = []
    message_queues = {}

    while inputs:
        print('waiting for the next event')
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for s in readable:

            if s is server:
                connection, client_address = s.accept()
                print('new connection from', client_address)
                connection.setblocking(False)
                inputs.append(connection)

                message_queues[connection] = Queue.Queue()

            else:
                data = s.recv(1024)
                if data:
                    print('received [%s] from %s' % (data, s.getpeername()))
                    message_queues[s].put(data)
                    if data == "hello":
                        message_queues[s].put(server_md5)
                    if data == "DIFF":
                        print("The server files is different from client.ready to trans files")
                        file_number = len(path_list)
                        print("The files number is %d" % file_number)
                        s.send(str(file_number))

                        while True:
                            for i in range(file_number):
                                if os.path.isfile(path_list[i]):
                                    fileinfo_size = struct.calcsize('128sl')
                                    fhead = struct.pack('128sl', os.path.basename(path_list[i]),
                                                        os.stat(path_list[i]).st_size)
                                    s.send(fhead)
                                    print 'client filepath: {0}'.format(path_list[i])

                                    with open(path_list[i], 'rb') as fp:
                                        while True:
                                            data = fp.read(5120)
                                            if not data:
                                                print '{0} file send over...'.format(path_list[i])
                                                break
                                            s.send(data)

                            data = s.recv(1024)
                            time.sleep(1)

                    if s not in outputs:
                        outputs.append(s)
                else:
                    print('closing', client_address, 'after reading no data')
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()

                    del message_queues[s]
        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except Queue.Empty:
                print('output queue for', s.getpeername(), 'is empty')
                outputs.remove(s)
            else:
                print('sending "%s" to %s' % (next_msg, s.getpeername()))
                s.send(next_msg)
        for s in exceptional:
            print('handling exceptional condition for', s.getpeername() )
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()

            del message_queues[s]
