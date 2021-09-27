import sys
import os
from Crypto.Cipher import AES
from base64 import b64decode
import socket
import time

flagSize = 32

blocksize = 16

flagBloksCount = 2

# reconnection socket


class tcpSocket:
    """docstring for mSocket"""

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.a = 0

    def connect(self, host, port):
        self.host = host
        self.port = port
        self.s.connect((self.host, self.port))

    def reconect(self, st=""):
        print("recon"+st)
        self.s.close()
        time.sleep(5)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.host, self.port))
        self.s.recv(1024)

    def send(self, data):
        try:
            if(self.a > 128):
                self.reconect(" wanted")
                self.a = 0
            self.s.send(data)
            self.a += 1
            time.sleep(0.25)
        except:
            print(self.a)
            self.reconect(" error")
            self.a = 0
            self.send(data)

    def recv(self, size):
        d = self.s.recv(size)
        if len(d) == 0:
            print(self.a)
        return d

    def close(self):
        self.s.close()

# function to find eventual offset


def findOffset(s):

    OffsetChar = '_'
    offsetLen = 0
    offsetStr = ""
    data = 'A'*blocksize*2
    while offsetLen < 52:

        offsetStr = OffsetChar*offsetLen
        s.send((offsetStr+data+"\n").encode())
        Rdata = s.recv(1024)
        Rdatat = Rdata.decode().split('\n')
        rd = b64decode(Rdatat[0])
        print (rd)
        if (rd[flagBloksCount*blocksize] == rd[(flagBloksCount+1)*blocksize]):
            print(f"offset fond : {offsetLen}")
            return offsetLen
        offsetLen += 1
        pass
    print("offset error")
    exit(1)

# define an simple oracle function


def oracle(s, data):
    s.send((data+"\n").encode())
    Rdata = s.recv(1024)
    Rdatat = Rdata.decode().split('\n')
    rd = b64decode(Rdatat[0])
    return rd


def printByte(b, g=16):
    out = ""
    i = 0
    m = len(b)
    while i < m:
        out += b[i:i+g].hex()
        out += " "
        i += g
    print(out)

# function to find a single character


def solvLetter(s, offsetLen, found, bp, bm):
    offset = 'B'*offsetLen
    static = '~'*(blocksize-len(found)-1)
    d = oracle(s, offset+static)
    target = d[bp:bm]
    for i in range(33, 128):
        val = (offset+static+found+chr(i))
        # print(val)
        ct = oracle(s, val)
        if (ct[bp:bm] == target):
            print(f"found : {chr(i)} => {i}")
            print(f"{found}{chr(i)}")
            return chr(i)
    return None

# function to find the key (use solvLetter)


def solvKey(s):
    offsetLen = findOffset(s)
    found = ""
    bp = flagBloksCount*blocksize
    bm = (flagBloksCount+1)*blocksize
    for i in range(0, 16):
        found += solvLetter(s, offsetLen, found, bp, bm)
    print(f"key : \"{found}\", length = {len(found)}")
    return found


def main():
    s = tcpSocket()
    s.connect("pwn-2021.duc.tf", 31914)
    print(s.recv(1024))
    key = solvKey(s).encode()

    # decoding flag
    data = oracle(s, "")
    printByte(data)
    cipher = AES.new(key, AES.MODE_ECB)
    pt = cipher.decrypt(data)
    print(pt)
    s.close()
    exit(0)


if __name__ == "__main__":
    main()
