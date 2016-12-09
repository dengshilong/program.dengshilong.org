title: Mac编译Thrift遇到OpenSSL错误
date: 2016-12-09 20:52:05
tags:
    - Thrift
    - OpenSSL
categories:
---
在编译Thrift时，遇到src/thrift/transport/TSSLSocket.cpp:33:10: fatal error: 'openssl/err.h' file not found问题，按照[Mac安装Thrift的Openssl错误解决](http://unix8.net/home.php/5008.html)没有解决问题

最后按照[stackoverflow](http://stackoverflow.com/questions/33165174/fatal-error-openssl-bio-h-file-not-found)上的解决办法，解决了问题。
```
brew install openssl
./configure LDFLAGS='-L/usr/local/opt/openssl/lib' CPPFLAGS='-I/usr/local/opt/openssl/include'
```
