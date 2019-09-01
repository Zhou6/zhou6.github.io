## 使用
192.168.3.2 or 192.168.199.188
用户名 pi or  z6
密码 ************

连接成功后输入vncserver， 即可用vnc连接pi作为pi显示器
 

### 摄像头
cd /home/project/mjpg-streamer/mjpg-streamer-experimental
开启服务
./mjpg_streamer -i "./input_uvc.so -n -f 30 -r 1280x960" -o "./output_http.so -w ./www -c <user_name>:<user_pwd> -p <my_port>"
电脑浏览器： 192.168.199.188:<my_port>
用户 z6 密码 ********
端口转发 路由器端口转发 https://zhuanlan.zhihu.com/p/22295170

https://www.jianshu.com/p/ecea3a8291ed
/home/project/mjpg-streamer/mjpg-streamer-experimental/mjpg_streamer -i "/home/project/mjpg-streamer/mjpg-streamer-experimental/input_uvc.so -n -f 30" -o "/home/project/mjpg-streamer/mjpg-streamer-experimental/output_http.so -w /home/project/mjpg-streamer/mjpg-streamer-experimental/www -c <user_name>:<user_pwd> -p <my_port>”
