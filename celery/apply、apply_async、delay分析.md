## celery发送任务(apply、apply_async、delay)分析
- apply: 
   
    官方注释：Execute this task locally, by blocking until the task returns（通过阻塞直到任务返回，在本地执行此任务）
    即同步任务，不走celery worker。

- apply_async：
  ```angular2
  def apply_async(self, args=None, kwargs=None, task_id=None, producer=None,
                  link=None, link_error=None, shadow=None, **options):
      """Apply tasks asynchronously by sending a message."""
      if self.typing:
          try:
              check_arguments = self.__header__
          except AttributeError:  # pragma: no cover
              pass
          else:
              check_arguments(*(args or ()), **(kwargs or {}))

      app = self._get_app()
      if app.conf.task_always_eager:   #  如果celery conf设置了task_always_eager=True，则走apply()同步任务
          with app.producer_or_acquire(producer) as eager_producer:
              serializer = options.get(
                  'serializer',
                  (eager_producer.serializer if eager_producer.serializer
                   else app.conf.task_serializer)
              )
              body = args, kwargs
              content_type, content_encoding, data = serialization.dumps(
                  body, serializer,
              )
              args, kwargs = serialization.loads(
                  data, content_type, content_encoding,
                  accept=[content_type]
              )
          with denied_join_result():
              return self.apply(args, kwargs, task_id=task_id or uuid(),
                                link=link, link_error=link_error, **options)  #  走apply()同步任务

      if self.__v2_compat__:
          shadow = shadow or self.shadow_name(self(), args, kwargs, options)
      else:
          shadow = shadow or self.shadow_name(args, kwargs, options)

      preopts = self._get_exec_options()
      options = dict(preopts, **options) if options else preopts

      options.setdefault('ignore_result', self.ignore_result)
      if self.priority:
          options.setdefault('priority', self.priority)

      return app.send_task(
          self.name, args, kwargs, task_id=task_id, producer=producer,
          link=link, link_error=link_error, result_cls=self.AsyncResult,
          shadow=shadow, task_type=self,
          **options
      )
  ```
  从app.send_task()开始经过一系列的流程（代码较多，不再往上粘贴），把task对应方法、参数、任务id、其他配置等包到一起组成一个message实例，最终到达使用的broker(redis)的_put，代码如下：
  ```angular2
  def _put(self, queue, message, **kwargs):
      """Deliver message."""
      pri = self._get_message_priority(message, reverse=False)

      with self.conn_or_acquire() as client:
          client.lpush(self._q_for_pri(queue, pri), dumps(message))

  def _q_for_pri(self, queue, pri):
      pri = self.priority(pri)
      return '%s%s%s' % ((queue, self.sep, pri) if pri else (queue, '', ''))
  ```
  _put()内把queue和任务权重priority合到一起组成key，message最终被lpush到redis的key中
- delay 同 apply_async
