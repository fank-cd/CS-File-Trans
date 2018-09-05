#_*_coding:utf-8_*_

import socket
import hashlib
import os
import struct
import sys

md5_path ='E:\\exercise project\\TCP_clientserver\\client_md5.txt'


def get_md5_file():
    path = 'E:\\exercise project\\TCP_clientserver\\client'
    path_list = []
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
    file_path = 'E:\\exercise project\\TCP_clientserver\\client\\'

    server_address = ('localhost', 1000)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(server_address)
    print 'connecting to %s port %s' % server_address

    print '%s: sending "%s"' % (s.getsockname(), "hello")
    s.send("hello")

    data = s.recv(1024)
    print('%s: received "%s"' % (s.getsockname(), data))
    if data == "hello":
        get_md5_file()
        with open(md5_path, 'rb') as md5:
            client_md5 = md5.read()

        server_md5 = s.recv(1024)
        if client_md5 != server_md5:
            s.send("DIFF")
            file_number = s.recv(1024)
            print(file_number)
            fileinfo_size = struct.calcsize('128sl')
            loop_count = 0
            while True:
                for i in range(int(file_number)):
                    # print i
                    buf = s.recv(fileinfo_size)
                    if buf:
                        filename, filesize = struct.unpack('128sl', buf)
                        fn = filename.strip('\00')
                        new_filename = os.path.join(file_path + fn)
                        print 'file new name is {0}, filesize is {1}'.format(new_filename,
                                                                             filesize)
                        recvd_size = 0  # 定义已接收文件的大小

                        with open(new_filename, 'wb') as fp:
                            print 'start receiving...'
                            while not recvd_size == filesize:
                                if filesize - recvd_size > 5120:
                                    data = s.recv(5120)
                                    recvd_size += len(data)
                                else:
                                    data = s.recv(filesize - recvd_size)
                                    recvd_size = filesize
                                fp.write(data)
                        loop_count += 1
                        print "done"
                        # break
                if loop_count == int(file_number):
                    break
    if not data:
        print('closing socket', s.getsockname())
        # s.close()
