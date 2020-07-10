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
