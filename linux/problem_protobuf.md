## ubuntu安装protobuf 没有_message.so的问题

1. cd ~
2. sudo /home/virtenv/bin/pip uninstall protobuf
3. export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
4. git clone --depth=1 https://github.com/google/protobuf.git
5. cd protobuf
6. sed -i.bak 's/https:\/\/googletest.googlecode.com\/files\/gtest-1.7.0.zip/http:\/\/qs-file.b0.upaiyun.com\/resources\/gtest-1.7.0.zip/g' autogen.sh
7. ./autogen.sh
8. ./configure
9. sudo make
10. sudo make install
11. cd python  # python安装包文件夹
12. sudo /home/virtenv/bin/python setup.py build --cpp_implementation
13. sudo /home/virtenv/bin/python setup.py install --cpp_implementation
14. sudo ldconfig

或者试试卸载pyrex,可能是受它影响
