# -*- coding: UTF-8 -*-
# 文件名：client.py
import socket
import hashlib
import os
import struct

s = socket.socket()
host = socket.gethostname()
port = 12345
file_path = 'E:\\exercise project\\TCP_clientserver\\client\\'
md5_path ='E:\\exercise project\\TCP_clientserver\\client_md5.txt'

def get_md5_file():
    md5_path = 'E:\\exercise project\\TCP_clientserver\\client_md5.txt'
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


def file_trans():

    s.connect((host, port))
    print s.recv(1024)  # hello
    with open(md5_path, 'rb') as md5:
        s.send(md5.read())
    status = s.recv(1024)
    print "status %s" % status
    if status == 'different':
        file_number = int(s.recv(1024))
        fileinfo_size = struct.calcsize('128sl')
        while True:
            for i in range(file_number):
                #print i
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
                    print "done"
                    # break
            if i == 1:
                break
    s.send('exit')
    s.close()


if __name__ == '__main__':
    get_md5_file()
    file_trans()
