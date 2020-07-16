## flask
内部优先使用simplejson,所以使用flask尽量安装simplejson包，提升效率
    try:
        import simplejson as json
    except ImportError:
        import json
    
    class _CompactJSON(object):
        """Wrapper around json module that strips whitespace."""
        @staticmethod
        def loads(payload):
            return json.loads(payload)
        @staticmethod
        def dumps(obj, **kwargs):
            kwargs.setdefault("ensure_ascii", False)
            kwargs.setdefault("separators", (",", ":"))
            return json.dumps(obj, **kwargs)

####坑：
注意：在没有安装simplejson时，全局把json猴子补丁替换成ujson后，如果使用flask的jsonify方法会报错，因为jsonify内部会使用
    
    json.dumps({}, **{'indent': None, 'separators': (',', ':'), 'cls': <class 'flask.json.JSONEncoder'>, 'sort_keys': True})
但是经过测试发现ujson.dumps({}, **args)的args不支持里面的值为None，会报错：
    
    TypeError: an integer is required (got type NoneType)
所以如果想要猴子补丁的话，可以先保证安装simplejson，让flask内部使用simplejson，外部自己的代码使用ujson，或者直接全部猴子补丁成simplejson也可以

### 使用问题
#### 1
- 众所周知，gevent是一个协助项目以协程的方式执行请求，但是今天用flask项目的时候进行测试，发现在没有使用gevent的情况下，单独启动flask项目，接口依旧是非阻塞的。
    ```
    @backend_view.route("/test", methods=["GET"])
    def test():
        all_param = getattr(request, 'all_param', {})
        print('接收请求', all_param.get('n'))
        time.sleep(5)
        return render_response()
    ```
    我写了一个协程来调用上面的接口10次。本以为单线程单进程的服务，肯定是阻塞的，每次执行会阻塞5s，10次至少50s。但是结果并非如此，总共耗时5.02s。
    
    总共执行了5s多一点，代表程序肯定是以多线程or多进程or协程的方式在跑。那么究竟使用了哪种方式，需要进一步测试。我在接口内加上了线程和进程id的输出
    ```
    print(threading.current_thread().ident, threading.main_thread().ident, os.getpid(), os.getppid())
    ```
    输出结果为
    ```
    123145482813440 4478598592 60907 47971
    123145488068608 4478598592 60907 47971
    123145482813440 4478598592 60907 47971
    ...
    ```
    由此可见，每次接收一个新请求，程序都会新开一个线程来执行任务，所以请求并没有阻塞。
    
    经过进一步测试发现，并发有多少，项目就会同时产生多少个新线程，并没有限制线程数，这样的方式并不适合线上使用。
    
    翻看了flask的源代码，发现是flask内部自有一个简易WSGI应用，且多线程和多进程两种方式都可以进行选择，当然也可以都不选。
    只需在执行app.run()时传入对应参数即可。
    
    [image](/image/flask_run_simple.png)
    
    [image](/image/flask_UWSGI.png)
    
    当尝试去掉多线程以及多进程方式之后：app.run(threaded=False, processes=1)，程序终于以预想的阻塞方式执行了。
