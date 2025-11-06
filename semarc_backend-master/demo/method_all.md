# **uv_run()函数内部变更组group1语义**

**说明**

研究内容3揭示代码层（文件级，类级，函数级，函数内部级）变更语义，用户通过选择前端系统的变更实体，将会显示输出该实体所处层级的变更语义及相关信息。下例为用户分析libuv项目，对比v1.44.2，v1.48.0的变更文件src/unix/core.c时，选择查看函数uv_run()中某组内部变更具体情况的输出

## 本组变更语义（核心输出）

1、**整体结论**

本次变更的主要目的是调整`uv_run`函数中定时器处理的执行顺序，以确保在`UV_RUN_DEFAULT`模式下，定时器在进入事件循环之前执行一次，从而保持向后兼容性。同时，变更还移除了`UV_RUN_ONCE`模式下的冗余定时器处理逻辑，简化了代码结构。依赖关联的变更函数`uv__run_timers`函数变更进一步支持了这一调整，避免了零超时定时器导致的忙循环问题。

2、**旧代码**

旧代码中，`uv_run`函数在`while`循环中每次都会执行`uv__update_time(loop)`和`uv__run_timers(loop)`，并且在`UV_RUN_ONCE`模式下还会在循环结束后再次执行这些操作。这种设计可能导致定时器在`UV_RUN_DEFAULT`模式下被多次执行，且`UV_RUN_ONCE`模式下的冗余逻辑增加了代码复杂性。

3、**新代码**

新代码通过以下改进解决了旧代码的问题：

- **提前执行定时器**：在`UV_RUN_DEFAULT`模式下，`uv__update_time(loop)`和`uv__run_timers(loop)`在进入`while`循环之前执行一次，确保定时器在事件循环开始前得到处理。
- **移除冗余逻辑**：移除了`UV_RUN_ONCE`模式下循环结束后的定时器处理逻辑，简化了代码结构。
- **统一处理逻辑**：在`while`循环中，`uv__update_time(loop)`和`uv__run_timers(loop)`被统一放置在循环末尾，确保定时器在每次循环结束时得到处理。

4、**变更描述**

本次变更的具体行为包括：

- **新增控制语句**：在`UV_RUN_DEFAULT`模式下，新增了`if`语句，用于在进入`while`循环之前执行`uv__update_time(loop)`和`uv__run_timers(loop)`。
- **移除控制语句**：移除了`UV_RUN_ONCE`模式下的`if`语句及其内部的`uv__update_time(loop)`和`uv__run_timers(loop)`调用。
- **移动函数调用**：将`uv__update_time(loop)`和`uv__run_timers(loop)`从`while`循环的起始位置移动到循环末尾，确保定时器在每次循环结束时得到处理。

通过以上变更，代码在保持向后兼容性的同时，简化了定时器处理的逻辑，并避免了冗余操作。

## **代码变更概览**

![2fb90f58-ccca-4733-bf24-b1705515f940](D:\Typora\user-image\2fb90f58-ccca-4733-bf24-b1705515f940.png)

## 代码变更检测结果

```
[
{
       "id": "114",
       "type": "Move_Sequence_Statement",
       "nodeBefore": {
       "node_type": "Sequence_Statement",
       "node_string": "uv__update_time(loop);",
       "node_stringDimensionality": "uv__update_time(loop);",
       "node_file": "src_unix_core.c",
       "node_parent": "int uv_run(uv_loop_t * loop, uv_run_mode mode){while(r != 0 && loop -> stop_flag == 0){node}}",
       "node_start_line": "392", 
       "node_end_line": "392" 
   },
       "nodeAfter": {
       "node_type": "Sequence_Statement",
       "node_string": "uv__update_time(loop);",
       "node_stringDimensionality": "uv__update_time(loop);",
       "node_file": "src_unix_core.c",
       "node_parent": "int uv_run(uv_loop_t * loop, uv_run_mode mode){while(r != 0 && loop -> stop_flag == 0){node}}",
       "node_start_line": "465", 
       "node_end_line": "465" 
   }
}, 
{
       "id": "115",
       "type": "Move_Function_Call",
       "nodeBefore": {
       "node_type": "Function_Call",
       "node_string": "uv__update_time(loop)",
       "node_stringDimensionality": "uv__update_time(loop)",
       "node_file": "src_unix_core.c",
       "node_parent": "int uv_run(uv_loop_t * loop, uv_run_mode mode){while(r != 0 && loop -> stop_flag == 0){uv__update_time(loop);}}",
       "node_start_line": "392", 
       "node_end_line": "392" 
   },
       "nodeAfter": {
       "node_type": "Function_Call",
       "node_string": "uv__update_time(loop)",
       "node_stringDimensionality": "uv__update_time(loop)",
       "node_file": "src_unix_core.c",
       "node_parent": "int uv_run(uv_loop_t * loop, uv_run_mode mode){while(r != 0 && loop -> stop_flag == 0){uv__update_time(loop);}}",
       "node_start_line": "465", 
       "node_end_line": "465" 
   }
}, 
{
       "id": "116",
       "type": "Move_Sequence_Statement",
       "nodeBefore": {
       "node_type": "Sequence_Statement",
       "node_string": "uv__run_timers(loop);",
       "node_stringDimensionality": "uv__run_timers(loop);",
       "node_file": "src_unix_core.c",
       "node_parent": "int uv_run(uv_loop_t * loop, uv_run_mode mode){while(r != 0 && loop -> stop_flag == 0){node}}",
       "node_start_line": "393", 
       "node_end_line": "393" 
   },
       "nodeAfter": {
       "node_type": "Sequence_Statement",
       "node_string": "uv__run_timers(loop);",
       "node_stringDimensionality": "uv__run_timers(loop);",
       "node_file": "src_unix_core.c",
       "node_parent": "int uv_run(uv_loop_t * loop, uv_run_mode mode){while(r != 0 && loop -> stop_flag == 0){node}}",
       "node_start_line": "466", 
       "node_end_line": "466" 
   }
}, 
{
       "id": "117",
       "type": "Move_Function_Call",
       "nodeBefore": {
       "node_type": "Function_Call",
       "node_string": "uv__run_timers(loop)",
       "node_stringDimensionality": "uv__run_timers(loop)",
       "node_file": "src_unix_core.c",
       "node_parent": "int uv_run(uv_loop_t * loop, uv_run_mode mode){while(r != 0 && loop -> stop_flag == 0){uv__run_timers(loop);}}",
       "node_start_line": "393", 
       "node_end_line": "393" 
   },
       "nodeAfter": {
       "node_type": "Function_Call",
       "node_string": "uv__run_timers(loop)",
       "node_stringDimensionality": "uv__run_timers(loop)",
       "node_file": "src_unix_core.c",
       "node_parent": "int uv_run(uv_loop_t * loop, uv_run_mode mode){while(r != 0 && loop -> stop_flag == 0){uv__run_timers(loop);}}",
       "node_start_line": "466", 
       "node_end_line": "466" 
   }
}, 
    {
        "id": "118",
        "Change Kind": "Add_Control_Statement",
        "nodeBefore": null,
        "nodeAfter": {
            "node_type": "Control_Statement",
            "node_content": "if (mode == UV_RUN_DEFAULT && r != 0 && loop->stop_flag == 0) {...}",
            "node_file": "src/unix/core.c",
            "node_location": "uv_run(uv_loop_t* loop, uv_run_mode mode){node}",
            "node_begin_line": "428", 
            "node_end_line": "431" 
        }
    },
    {
        "id": "119",
        "Change Kind": "Add_Function_call",
        "nodeBefore": null,
        "nodeAfter": {
            "node_type": "Function_call",
            "node_content": "uv__update_time(loop);",
            "node_file": "src/unix/core.c",
            "node_location": "uv_run(uv_loop_t* loop, uv_run_mode mode){ if (mode == UV_RUN_DEFAULT && r != 0 && loop->stop_flag == 0) {uv__update_time(loop);}}", 
            "node_begin_line": "429", 
            "node_end_line": "429" 
        }
    },
    {
        "id": "120",
        "Change Kind": "Add_Function_call",
        "nodeBefore": null,
        "nodeAfter": {
            "node_type": "Function_call",
            "node_content": "uv__run_timers(loop)",
            "node_file": "src/unix/core.c",
            "node_location": "uv_run(uv_loop_t* loop, uv_run_mode mode){ if (mode == UV_RUN_DEFAULT && r != 0 && loop->stop_flag == 0)  {uv__update_time(loop);}}", 
            "node_begin_line": "430", 
            "node_end_line": "430" 
        }
    },
    {
        "id": "121",
        "Change Kind": "Remove_Control_Statement",
        "nodeBefore": {
            "node_type": "Control_Statement",
            "node_content": "if (mode == UV_RUN_ONCE) {...}",
            "node_file": "src/unix/core.c",
            "node_location": "uv_run(uv_loop_t* loop, uv_run_mode mode){ while (r != 0 && loop->stop_flag == 0) {node}}",
            "node_begin_line": "423", 
            "node_end_line": "434" 
        },
        "nodeAfter": null
    },
    {
        "id": "122",
        "Change Kind": "Remove_Function_Call",
        "nodeBefore": {
            "node_type": "Function_Call",
            "node_content": "uv__update_time(loop)",
            "node_file": "src/unix/core.c",
            "node_location": "uv_run(uv_loop_t* loop, uv_run_mode mode){ while (r != 0 && loop->stop_flag == 0) { if (mode == UV_RUN_ONCE) { uv__update_time(loop);}}}",
            "node_begin_line": "432", 
            "node_end_line": "432" 
        },
        "nodeAfter": null
    },
    {
        "id": "123",
        "Change Kind": "Remove_Function_Call",
        "nodeBefore": {
            "node_type": "Function_Call",
            "node_content": "uv__run_timers(loop)",
            "node_file": "src/unix/core.c",
            "node_location": "uv_run(uv_loop_t* loop, uv_run_mode mode){ while (r != 0 && loop->stop_flag == 0) { if (mode == UV_RUN_ONCE) { uv__run_timers(loop);}}}",
            "node_begin_line": "433", 
            "node_end_line": "433" 
        },
        "nodeAfter": null
    }
```



## 关联上下文信息

### 变更所在函数

**{before}**

```c
int uv_run(uv_loop_t* loop, uv_run_mode mode) {
  int timeout;
  int r;
  int can_sleep;

  r = uv__loop_alive(loop);
  if (!r)
    uv__update_time(loop);

  while (r != 0 && loop->stop_flag == 0) {
    uv__update_time(loop);
    uv__run_timers(loop);

    can_sleep =
        QUEUE_EMPTY(&loop->pending_queue) && QUEUE_EMPTY(&loop->idle_handles);

    uv__run_pending(loop);
    uv__run_idle(loop);
    uv__run_prepare(loop);

    timeout = 0;
    if ((mode == UV_RUN_ONCE && can_sleep) || mode == UV_RUN_DEFAULT)
      timeout = uv__backend_timeout(loop);

    uv__io_poll(loop, timeout);

    /* Process immediate callbacks (e.g. write_cb) a small fixed number of
     * times to avoid loop starvation.*/
    for (r = 0; r < 8 && !QUEUE_EMPTY(&loop->pending_queue); r++)
      uv__run_pending(loop);

    /* Run one final update on the provider_idle_time in case uv__io_poll
     * returned because the timeout expired, but no events were received. This
     * call will be ignored if the provider_entry_time was either never set (if
     * the timeout == 0) or was already updated b/c an event was received.
     */
    uv__metrics_update_idle_time(loop);

    uv__run_check(loop);
    uv__run_closing_handles(loop);

    if (mode == UV_RUN_ONCE) {
      /* UV_RUN_ONCE implies forward progress: at least one callback must have
       * been invoked when it returns. uv__io_poll() can return without doing
       * I/O (meaning: no callbacks) when its timeout expires - which means we
       * have pending timers that satisfy the forward progress constraint.
       *
       * UV_RUN_NOWAIT makes no guarantees about progress so it's omitted from
       * the check.
       */
      uv__update_time(loop);
      uv__run_timers(loop);
    }

    r = uv__loop_alive(loop);
    if (mode == UV_RUN_ONCE || mode == UV_RUN_NOWAIT)
      break;
  }

  /* The if statement lets gcc compile it to a conditional store. Avoids
   * dirtying a cache line.
   */
  if (loop->stop_flag != 0)
    loop->stop_flag = 0;

  return r;
}
```



**{after}**

```c
int uv_run(uv_loop_t* loop, uv_run_mode mode) {
  int timeout;
  int r;
  int can_sleep;

  r = uv__loop_alive(loop);
  if (!r)
    uv__update_time(loop);

  /* Maintain backwards compatibility by processing timers before entering the
   * while loop for UV_RUN_DEFAULT. Otherwise timers only need to be executed
   * once, which should be done after polling in order to maintain proper
   * execution order of the conceptual event loop. */
  if (mode == UV_RUN_DEFAULT && r != 0 && loop->stop_flag == 0) {
    uv__update_time(loop);
    uv__run_timers(loop);
  }

  while (r != 0 && loop->stop_flag == 0) {
    can_sleep =
        uv__queue_empty(&loop->pending_queue) &&
        uv__queue_empty(&loop->idle_handles);

    uv__run_pending(loop);
    uv__run_idle(loop);
    uv__run_prepare(loop);

    timeout = 0;
    if ((mode == UV_RUN_ONCE && can_sleep) || mode == UV_RUN_DEFAULT)
      timeout = uv__backend_timeout(loop);

    uv__metrics_inc_loop_count(loop);

    uv__io_poll(loop, timeout);

    /* Process immediate callbacks (e.g. write_cb) a small fixed number of
     * times to avoid loop starvation.*/
    for (r = 0; r < 8 && !uv__queue_empty(&loop->pending_queue); r++)
      uv__run_pending(loop);

    /* Run one final update on the provider_idle_time in case uv__io_poll
     * returned because the timeout expired, but no events were received. This
     * call will be ignored if the provider_entry_time was either never set (if
     * the timeout == 0) or was already updated b/c an event was received.
     */
    uv__metrics_update_idle_time(loop);

    uv__run_check(loop);
    uv__run_closing_handles(loop);

    uv__update_time(loop);
    uv__run_timers(loop);

    r = uv__loop_alive(loop);
    if (mode == UV_RUN_ONCE || mode == UV_RUN_NOWAIT)
      break;
  }

  /* The if statement lets gcc compile it to a conditional store. Avoids
   * dirtying a cache line.
   */
  if (loop->stop_flag != 0)
    loop->stop_flag = 0;

  return r;
}
```

### 依赖关联的代码信息

**uv__update_time()**

对比的前后版本中未发生变更

```c
UV_UNUSED(static void uv__update_time(uv_loop_t* loop)) {
  /* Use a fast time source if available.  We only need millisecond precision.
   */
  loop->time = uv__hrtime(UV_CLOCK_FAST) / 1000000;
}
```

**uv__run_timers()**

对比的前后版本中发生变更

```
**uv__run_timers函数变更语义**

1、**整体结论**

本次变更的主要目的是解决`uv__run_timers`函数在处理零超时定时器时可能导致的忙循环问题，并通过引入`uv__queue`结构体来改进队列操作的类型安全性和代码可读性。`elseCodeChanges`中的`uv__queue`相关变更（如`uv__queue_init`、`uv__queue_insert_tail`等）与本次变更协同作用，共同实现了定时器队列的初始化和操作，避免了内存损坏和忙循环问题。

2、**旧代码**

旧代码中，`uv__run_timers`函数直接处理定时器堆中的节点，并在每次循环中立即执行定时器回调。这种设计在处理零超时定时器时可能导致忙循环问题，因为定时器会立即重新插入堆中并再次触发回调。此外，旧代码使用了`QUEUE`宏进行队列操作，存在类型转换问题，导致gcc编译器发出警告。

3、**新代码**

新代码通过引入`uv__queue`结构体和相关操作函数，改进了定时器队列的处理方式。具体改进包括：

- 新增了`ready_queue`队列，用于收集所有已过期的定时器。
- 在`for`循环中，定时器不再立即执行回调，而是被插入到`ready_queue`中。
- 在`while`循环中，逐个处理`ready_queue`中的定时器，确保定时器回调不会立即重新触发，从而避免了忙循环问题。
- 使用`uv__queue`结构体替代了`QUEUE`宏，解决了类型转换问题，提升了代码的类型安全性和可读性。

4、**变更描述**

本次变更的具体行为包括：

- **新增变量**：新增了`queue_node`和`ready_queue`变量，用于管理定时器队列。
- **初始化队列**：通过`uv__queue_init(&ready_queue)`初始化`ready_queue`。
- **插入队列**：在`for`循环中，使用`uv__queue_insert_tail(&ready_queue, &handle->node.queue)`将已过期的定时器插入到`ready_queue`中。
- **处理队列**：在`while`循环中，使用`uv__queue_head(&ready_queue)`获取队列头节点，并通过`uv__queue_remove(queue_node)`和`uv__queue_init(queue_node)`处理队列节点。
- **执行回调**：在`while`循环中，通过`uv_timer_again(handle)`和`handle->timer_cb(handle)`执行定时器回调，确保回调不会立即重新触发。

通过以上变更，代码解决了零超时定时器导致的忙循环问题，并提升了队列操作的类型安全性和可读性。
```



