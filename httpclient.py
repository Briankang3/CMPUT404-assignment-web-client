#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse
from sys import stdout

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return int(data.split(' ')[1])

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return data.split('\r\n\r\n')[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        temp=urllib.parse.urlparse(url)
        host=temp.hostname
        port=temp.port
        if not port:
            port=80
        path=temp.path
        if len(path)==0:
            path="/"
        
        self.connect(host, port)
        
        to_send="GET "+ path +" HTTP/1.1\r\n"
        to_send+="Host: "+ host + "\r\n"
        to_send+="Connection: close\r\n\r\n"
        
        self.sendall(to_send)
        data=self.recvall(self.socket)
        
        stdout.write("This is the response from GET\n")
        stdout.write(data)
        stdout.write('\n')
        
        code=self.get_code(data)
        body=self.get_body(data)
        
        self.close()
        
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        temp=urllib.parse.urlparse(url)
        host=temp.hostname
        port=temp.port
        if not port:
            port=80
        path=temp.path
        if len(path)==0:
            path="/"
        
        send_body=None
        if args is not None:
            send_body=urllib.parse.urlencode(args)
        
        self.connect(host, port)
        
        to_send="POST " + path + " HTTP/1.1\r\n"
        to_send+="Host: " + host + "\r\n"
        to_send+="Connection: closed\r\n"
        
        if send_body!=None:
            to_send+="Content-Type: application/x-www-form-urlencoded\r\n"
            to_send+="Content-Length: "+str(len(send_body)) +"\r\n\r\n"
            to_send+=send_body+"\r\n"
        else:
            to_send+="Content-Length: 0\r\n\r\n"
        
        self.sendall(to_send)
        data=self.recvall(self.socket)
        
        stdout.write("This is the response from POST\n")
        stdout.write(data)
        stdout.write('\n')
        
        code=self.get_code(data)
        body=self.get_body(data)
        
        self.close()
        
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))