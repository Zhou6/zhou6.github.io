## 服务器python升级
### Python2.6升级到python2.7

1. 去python官网获取对应版本包
wget https://www.python.org/ftp/python/2.7.15/Python-2.7.15.tgz
2. 解压，tar -xvf  Python-2.7.15.tgz
3. 进入python目录 cd Python-2.7.15
4. ./configure --with-ssl(先yum install openssl)
(为了防止后期pip报错
Can’t connect to HTTPS URL because the SSL module is not available)
5. make
6. make install
7. 删除旧版本软链 rm -rf /usr/bin/python
8. 创建新版python软链 ln -s /usr/local/python2.7/bin/python2.7 /usr/bin/python
9. 查看python版本 python -v

whereis python 可查看python安装路径
此时python已升级完毕，但是会发现yum和pip无法正常使用，原因是yum和pip是基于python实现的，所以现有的yum和pip是需要基于老版本python来运行

解决yum：
1. 查找yum文件并编辑
 
     which yum  ==》 /usr/bin/yum
     vi /usr/bin/yum 
2. 将文件首行#!/usr/bin/python 改为 #！/usr/bin/python2.6

解决pip：
- 安装setuptools

    如果遇到RuntimeError: Compression requires the (missing) zlib module
则 
        
      yum install zlib， 
      yum install lib-devel,
    之后去python安装目录重新编译:
        
      make clean =>make => make install
-  安装pip
如果安装之后，报错如下：pkg_resources.DistributionNotFound: The 'pip==7.1.0' distribution was not found and is required by the application

    将文件里的pip==后面的版本号改为安装的pip版本即可
        
       vim /usr/bin/pip 


### 安装python3.7
    apt-get install libssl-dev
    wget https://www.python.org/ftp/python/3.7.4/Python-3.7.4.tgz
    tar zxvf Python-3.7.4.tgz
    cd Python-3.7.4
    ./configure --with-ssl 
    注意：–with-ssl必须加上，否则使用pip安装第三方包时，会引发ssl错误。导致无法使用。如果执行pip install出错，重新编译安装即可。
    make && make install
错误解决：

ZipError：
    
    sudo apt install zlib*
ImportError:'_ctypes'

    sudo apt-get install python-dev python-setuptools python-pip python-smbus build-essential libncursesw5-dev libgdbm-dev libc6-dev zlib1g-dev libsqlite3-dev tk-dev libssl-dev openssl libffi-dev
ModuleNotFoundError: No module named '_ctypes’的解决办法：
    
    apt-get install libffi-dev
- 安装完成测试一下，import ssl是否能成功，否则就是上面那些包没装好
- whereis python3.7
- 添加python3的软链接 

      sudo ln -s /usr/local/bin/python3.7 /usr/bin/python3.7 
- 添加 pip3 的软链接 
    
      sudo ln -s /usr/local/bin/pip3.7 /usr/bin/pip3.7

- 创建虚拟环境
    
      virtualenv venv3.7 --python=python3.7
- python3.7要求openssl>= 1.0.2 安装高版本openssl
    
      ./configure --with-openssl=$HOME/openssl
