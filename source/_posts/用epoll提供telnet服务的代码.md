title: 用epoll提供telnet服务的代码
tags:
  - epoll
  - telnet
id: 572
categories:
  - 编程
date: 2013-12-25 22:03:54
---

这是之前写的用epoll提供telnet服务的代码。

``` c
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <errno.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <fcntl.h>
#include <arpa/inet.h>
#include <sys/epoll.h>
#include <stdlib.h>
#include <netinet/tcp.h> 
#include <ctype.h>
#include <assert.h>
#define MAX_EVENTS 10
#define PORT 9999
//从buf中得到命令
void _get_command(char *buf, char *cmd) {
	int i = 0;
	int j = 0;
	while (!isalpha(buf[i]))
		i++;
	while (buf[i] != '\0' && buf[i] != ' ' && buf[i] != '\r' && buf[i] != '\n') {
		cmd[j++] = buf[i];
		i++;
	}
	cmd[j] = '\0';
}
// 返回成功发送的字节数
int Send(int sock, void *buffer, int size)
{
	int nsend = 0, total = 0;
	int err;
	if(NULL == buffer || 0 == size) {
		return 0;
	}
	while(size > 0) {
		nsend = write(sock, (char*)buffer + total, size);
		if(nsend == -1) {
			err = errno;
			if(EINTR == err) {
				printf("send data to socket[%d], error is %s[%d]\n", 
							sock, strerror(err), err);
			} else {
				printf("Fail to send data to socket[%d], error is %s[%d]", 
							sock, strerror(err), err);
				return -1;	
			}
		} else {
			total += nsend;
			size -= nsend;
		}
	}
	return total;
}
//处理重置命令
void process_reset(int sock){
	char mess[] = "reset successful\r\n";
	Send(sock, mess, strlen(mess));
	return;
}
//处理错误命令
void process_error(int sock) {
	char error[] = "ERROR\r\n";
	Send(sock, error, strlen(error));
	return;
}
void process_stats(int sock){
	char mess[] = "stats successful\r\n";
	Send(sock, mess, strlen(mess));
	return;
}

//处理退出命令
void process_quit(int sock) {
	close(sock);
}

int process_command(int sock, char *buf) {
	assert(buf != NULL);

	/*char cmd[BUFSIZ];
	_get_command(buf, cmd);	
	printf("command: %s\n", cmd);

	if (strcmp("stats",cmd) == 0) {
		process_stats(sock);
	} else if (strcmp("reset", cmd) == 0) {
		process_reset(sock);
	} else if (strcmp("quit", cmd) == 0){
		process_quit(sock);
	} else {
		process_error(sock);
	}*/
	Send(sock, buf, strlen(buf));

	return 0;
}

//设置socket为非阻塞
void setnonblocking(int sockfd) {
	int opts;
	opts = fcntl(sockfd, F_GETFL);
	if (opts < 0) {
		perror("fcntl(F_GETFL)\n");
		exit(1);
	}
	opts = (opts | O_NONBLOCK);
	if (fcntl(sockfd, F_SETFL, opts) < 0) {
		perror("fcntl(F_SETFL)\n");
		exit(1);
	}
}
int main() {
	int listenfd, conn_sock, epfd;
	char buf[BUFSIZ];
	socklen_t clilen;
	struct sockaddr_in cliaddr, servaddr;
	struct epoll_event ev, events[MAX_EVENTS];
	listenfd = socket(AF_INET, SOCK_STREAM, 0);
	if (listenfd < 0) {
		printf("create socket error\n");
		return -1;
	}
	int on = 1;
	setsockopt(listenfd, SOL_SOCKET, SO_REUSEADDR, &on, sizeof(on));
	setnonblocking(listenfd);
    struct linger {
        int l_onoff; /* 0 = off, nozero = on */
        int l_linger; /* linger time */
    }lin;
    lin.l_onoff = 1;
    lin.l_linger = 0;
    setsockopt(listenfd, SOL_SOCKET, SO_LINGER, (char*)&lin, sizeof(lin));
	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port = htons(PORT);

	if(bind(listenfd,(struct sockaddr*)&servaddr,sizeof(struct sockaddr))<0){
		printf("bind error\n");
		close(listenfd);
		return -1;
	}

	if(listen(listenfd, 5) < 0) {
		printf("listen error\n");
		close(listenfd);
		return -1; 
	}
	epfd = epoll_create(MAX_EVENTS); //生成epoll专用的文件描述符
	if (epfd == -1) {
		printf("epoll_create\n");
		return -1;
	}
	ev.events = EPOLLIN | EPOLLET; //设置处理的事件类型,设置为边沿触发
	ev.data.fd = listenfd;
	if (epoll_ctl(epfd, EPOLL_CTL_ADD, listenfd, &ev) == -1) {
		printf("epoll_ctl add listen_sock fail\n");
		close(listenfd);
		return -1;
	}
	while (1) {
		int timeout = 1000; 
		int nfds = epoll_wait(epfd, events, MAX_EVENTS, timeout);
		if (nfds == -1) {
			printf("epoll_wait\n");
			return -1;
		}
		for (int i = 0;i < nfds; ++i) {
			int fd = events[i].data.fd;
			if (fd == listenfd) { //监听事件
				while ((conn_sock = accept(listenfd, NULL, NULL)) > 0) {//循环处理accept,这样可以处理多个连接在就绪队列中的情况
					printf("accept %d\n", conn_sock);
					setnonblocking(conn_sock);
					ev.events = EPOLLIN | EPOLLET; //设置为边沿触发
					ev.data.fd = conn_sock;
					if (epoll_ctl(epfd, EPOLL_CTL_ADD, conn_sock, &ev) == -1) {
						printf("epoll_ctl: add fail\n");
						close(conn_sock);
						return -1;
					}
				}
			} else if (events[i].events & EPOLLIN) {//读事件，说明有数据从客户端发来
				int n = 0;
				int nread = 0;
				while ((nread = read(fd, buf + n, BUFSIZ - n)) > 0) {
					n += nread;
				}
				if (nread == -1 && errno != EAGAIN) {//读数据错误,关闭描述符
					printf("read error\n");
					close(fd); //关闭一个描述符，它会从epoll描述符集合中自动删除
					continue;
				}
				if(nread == 0) { //客户端关闭连接，关闭相应的描述符
					close(fd);
					continue;
				}
				if( n > 0) {
					process_command(fd, buf);
					memset(buf, 0, sizeof(buf));
				}
			}
		}
	}
}
```
