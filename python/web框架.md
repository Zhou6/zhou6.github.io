### flask
  同步框架。接口不支持async\await的写法,数据必须同步返回。
  否则会报错：
```
TypeError: The view function did not return a valid response. The return type must be a string, dict, tuple, Response instance, or WSGI callable, but it was a coroutine.
RuntimeWarning: coroutine 'hello_a' was never awaited
  def _format_timetuple_and_zone(timetuple, zone):
RuntimeWarning: Enable tracemalloc to get the object allocation traceback
```
  所以异步方式目前只能联合使用gevent实现。
### aiohttp
  异步框架，支持异步写法。异步性能优于flask + gevent。评测：https://www.weaf.top/posts/a6235d78/
### sanic
  异步框架，支持异步写法。且使用了uvloop完整替代asyncio事件循环，使得asyncio更快。性能优于aiohttp。https://uvloop.readthedocs.io/
