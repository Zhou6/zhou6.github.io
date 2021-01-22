## nginx配置
假如我们有个web服务,服务器配置nginx负责请求转发到web服务，外部还配置了负载均衡（IP：10.10.10.10）,我们的用户（IP：123.123.123.123）来访问负载均衡

然后我们的web服务内的nginx配置修改如下：
```angular2
示例配置
server {
    listen 80;
    server_name XXX.com;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    #  real_ip_recursive on;
}
```
### 请求获取流程
- 用户的请求到达负载均衡时，如果用户请求没有特意设置XFF，则负载均衡获取到的XFF应该为空，remote_addr=123.123.123.123，
之后按照标准把remote_addr添加到XFF请求头，最后把请求转到nginx。

- nginx获取到的请求头XFF为123.123.123.123，remote_addr=10.10.10.10。
当nginx执行完proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for后，把remote_addr添加到XFF后面，
执行proxy_set_header X-Real-IP $remote_addr，则添加了X-Real-IP设置为remote_addr值，接下来请求转到web服务。

- 请求最后到达web服务时，获取到的X-Forwarded-For为123.123.123.123, 10.10.10.10， X-Real-IP为10.10.10.10，remote_addr为127.0.0.1。

### 参数含义
- remote_addr
    
    remote_addr是上一级请求过来的真实ip地址。
    
    remote_addr无法伪造，因为建立 TCP 连接需要三次握手，如果伪造了源 IP，无法建立 TCP 连接，更不会有后面的 HTTP 请求

- X-Forwarded-For(简称：XFF)

    X-Forwarded-For 是一个 HTTP 扩展头部。HTTP/1.1（RFC 2616）协议并没有对它的定义，
    它最开始是由 Squid 这个缓存代理软件引入，用来表示 HTTP 请求端真实 IP。
    如今它已经成为事实上的标准，被各大 HTTP 代理、负载均衡等转发服务广泛使用，
    并被写入 RFC 7239（Forwarded HTTP Extension）标准之中。
    
    X-Forwarded-For 请求头格式非常简单，就这样
    ```angular2
    X-Forwarded-For: client, proxy1, proxy2
    ```
    可以看到，XFF 的内容由「英文逗号 + 空格」隔开的多个部分组成，最开始的是离服务端最远的设备 IP，然后是每一级代理设备的 IP。
- X-Real-IP
    理论上只是一个普通扩展头部，没有特殊含义，但是业内普遍使用，将其赋值为用户真实ip。
    事实上我们可以定义为任何一个名字，可以叫'abc'，最后传到web服务中，header里是会有abc参数的。
    但是像我们本次的架构和nginx配置，我们的X-Real-IP最后是被赋值为负载均衡的ip。
    所以这种配置只适合没有中间负载代理的架构，即用户直接访问nginx，X-Real-IP才会被记录为真实ip。
    
    
### 当nginx配置改为：
```angular2
server {
    listen 80;
    server_name XXX.com;
    set_real_ip_from 10.10.10.10;
    real_ip_header  X-Forwarded-For;
    proxy_set_header X-Real-IP $remote_addr;
    #  real_ip_recursive on;
}
```
请求到达nginx之后获取到remote_addr为123.123.123.123并赋值给X-Real-IP。
- set_real_ip_from
  
    set_real_ip_from指令是告诉nginx，10.10.10.10是我们的反代服务器，不是真实的用户IP。
    真实服务器上一级代理的IP地址或者IP段,可以写多行
- real_ip_header
    
    real_ip_header则是告诉nginx真正的用户IP是存在X-Forwarded-For请求头中
- real_ip_recursive （未完待续）

    递归排除IP地址,ip串从右到左开始排除set_real_ip_from里面出现的IP,如果出现了未出现这些ip段的IP，那么这个IP将被认为是用户的IP
