## celery beat原理分析
执行命令 celery -A app.celery beat -l info

从celery.__main__方法开始执行，经过一系列参数处理，最终会走到celery.apps.beat:Beat => celery.beat:Service，获取到实例Service后，执行核心方法service.start()，代码如下：
```angular
def start(self, embedded_process=False):
    info('beat: Starting...')
    debug('beat: Ticking with max interval->%s',
          humanize_seconds(self.scheduler.max_interval))

    signals.beat_init.send(sender=self)
    if embedded_process:
        signals.beat_embedded_init.send(sender=self)
        platforms.set_process_title('celery beat')

    try:
        while not self._is_shutdown.is_set():
            interval = self.scheduler.tick()  # 核心中的核心方法，返回下一个最近任务还剩多少时间
            if interval and interval > 0.0:   
                debug('beat: Waking up %s.',
                      humanize_seconds(interval, prefix='in '))
                time.sleep(interval)   #  下一个最近任务大于0，则开始休眠
                if self.scheduler.should_sync():
                    self.scheduler._do_sync()
    except (KeyboardInterrupt, SystemExit):
        self._is_shutdown.set()
    finally:
        self.sync()
```
self.scheduler.tick()代码如下：
``` angular
def tick(self, event_t=event_t, min=min, heappop=heapq.heappop,
         heappush=heapq.heappush):
    """Run a tick - one iteration of the scheduler.

    Executes one due task per call.

    Returns:
        float: preferred delay in seconds for next call.
    """
    adjust = self.adjust
    max_interval = self.max_interval   #  最大的休眠时间, 默认300s

    if (self._heap is None or
            not self.schedules_equal(self.old_schedulers, self.schedule)):
        self.old_schedulers = copy.copy(self.schedule)
        self.populate_heap()

    H = self._heap

    if not H:
        return max_interval

    event = H[0]   # 获取堆中第一个数据，即定时任务列表中的第一个任务事件
    entry = event[2]
    is_due, next_time_to_run = self.is_due(entry)  #  检查该ModelEntry是否可以运行，获取下一次运行的时间
    if is_due:
        verify = heappop(H)
        if verify is event:
            next_entry = self.reserve(entry)
            self.apply_entry(entry, producer=self.producer)  #  可以运行，则调用执行定时任务，内部会调用apply_async，和平时项目使用方式相同
            #  heappush将该任务下一次执行的实例压入堆中,方法内部在任务加入堆之后会调用_siftdown方法，
            #  _siftdown会把任务进行排序，使得堆内的排序一直是下次任务距离时间由小到大
            heappush(H, event_t(self._when(next_entry, next_time_to_run),
                                event[1], next_entry))  
            return 0
        else:
            heappush(H, verify)
            return min(verify[0], max_interval)
    return min(adjust(next_time_to_run) or max_interval, max_interval)  #  返回下次运行时间
```
_siftdown代码如下：
```angular2
def _siftdown(heap, startpos, pos):
    newitem = heap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if newitem < parent:
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = newitem
```
由此可见，beat内部原理是由一个while循环和一个最小堆组成，循环内部取出堆的首位，即下次运行时间最近的任务，判断执行时间和now的差值，如果<=0，则执行apply_async发送任务，进入下次循环，如果>0，则sleep相应时间之后进入下次循环
