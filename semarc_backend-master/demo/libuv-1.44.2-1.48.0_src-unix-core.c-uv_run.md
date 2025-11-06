# libuv 1.44.2->1.48.0  src-unix-core.c-uv_run()变更语义

1、**整体结论**  
本次变更主要优化了`uv_run`函数中定时器的执行逻辑和事件循环的顺序，解决了定时器在特定模式下错误触发的问题，并统一了事件循环模型。同时引入了类型安全的队列检查函数和性能监控功能。

2、**变更前**  

- UV_RUN_DEFAULT模式下定时器在每次循环开头无条件执行，可能导致停止/未引用的定时器被错误触发
- UV_RUN_ONCE模式下存在冗余的定时器执行逻辑
- 使用不安全的QUEUE_EMPTY宏导致编译器警告
- 缺少事件循环迭代次数的统计功能

3、**变更后**  

- UV_RUN_DEFAULT模式下定时器仅在循环前执行一次，避免重复触发
- 统一在循环末尾执行定时器，确保事件循环模型的一致性
- 使用类型安全的uv__queue_empty函数消除了编译器警告
- 添加了uv__metrics_inc_loop_count调用来统计循环迭代次数

4、**变更描述**  
变更包含两个独立部分：

定时器逻辑优化部分：

- 将uv\__update_time和uv__run_timers从循环开头移至末尾
- 为UV_RUN_DEFAULT模式添加前置定时器条件块
- 移除UV_RUN_ONCE模式的冗余定时器代码
  关联提交：
- hash: 66009549067cab59d697cd8df8091a179d1a15fc
- 时间: 2023-03-20
- 作者: Trevor Norris
- 消息: 调整定时器执行顺序以符合事件循环模型

代码优化部分：

- 替换QUEUE_EMPTY为uv__queue_empty
- 添加uv__metrics_inc_loop_count调用
  关联提交：
- hash: 1b01b786c0180d29f07dccbb98001a2b3148828a
- 时间: 2023-05-25
- 作者: Ben Noordhuis
- 消息: unix,win: replace QUEUE with struct uv__queue

- hash: e14158605336d2852dc5489204d2eb7fbe38a97d
- 时间: 2022-11-11
- 作者: Trevor Norris
- 消息: src: add new metrics APIs