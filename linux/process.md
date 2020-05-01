#网络

进程
进程内部文件夹： 
    cd /proc/$PID/
        cd fd （file desriptor:文件描述符）: IO流
             0 - 输入  1 - 输出  2 - 报错
        cd task  线程
        
BIO:堵塞，没数据一直等待，来数据新建一个线程去处理
NIO（Nonblock）：非堵塞，没数据直接返回没数据，挨个轮询所有连接是否有数据，每次查询都是 用户态 =》内核态切换
select：多路复用，不再挨个轮询，把所有fd传给内核，可以直接返回所有有数据传入的结果集，之后挨个去read，和上一个区别是，一个是用户切换内核循环和内核循环
poll：和select稍有区别
epoll:事件回调、多路复同步非堵塞
    epoll_create:return ep_fd（此fd用来维护未来接入服务的连接的文件描述符们）描述符们红黑树？
    epoll_ctl: 传入ep_fd,新连接fd，监听读｜写事件：相当于往ep_fd扔入fd
    epoll_wait:循环等待事件，等待fd事件回调告知服务（redis）有事件，多个事件是链表结构存储



kafka：
存数据：mmap：用户空间和内核空间打通，不需要用户空间和内核空间的数据拷贝过程，但是还需要从硬盘拷贝到内核过程 ，ex: RandomAccessFile.map会开启mmap
取数据：0拷贝 =>sendfile 磁盘 =》内核 =》发送
        正常通过程序获取文件需要两次系统调用（拷贝两次？），程序=》内核读 =》文件 =》内核 =》程序 =》内核写 =》发送文件数据
        冷数据不需要加工就可以直接返回的文件数据，为了减少调用，可以使用0拷贝
        man 2 sendfile
 
 
打开监听（服务端）：nc -localhost 8080 
建立连接（客户端）：nc localhost 8080

查看网络状态：netstat
     
linux追踪进程：strace  -ff   -o ./ooxx 
    strace 
        -ff 跟踪所有线程
        -o 输出到文件


socket：获得fd => bind fd+端口 => 监听fd => accept (poll堵塞)

linux kernel 内核?

man 2 bind|listen|accept|read|recv_from|socket|select｜epoll
BIO：阻塞、多线程IO
NIO：非阻塞， 
select|poll: 多路复用
epoll: 基于事件（event）的多路复用：有人连接会触发事件，产生新的描述符添加到空间，下次循环就只读这些：nginx\redis\netty



说一下BIO、NIO、AIO(windows才有)
说一下select 、 poll、epoll



