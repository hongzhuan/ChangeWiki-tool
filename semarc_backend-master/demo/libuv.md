# libuv 变更分析报告

---

### 1. 模块变更

#### **uv_io_t**

| 变更类型       | 变更内容                               | 关键函数                             | 相关文件                  | Commit ID                              |
| -------------- | -------------------------------------- | ------------------------------------ | ------------------------- | -------------------------------------- |
| 功能特性变更       | 添加支持无扩展名的可执行路径运行           | uv_spawn                            | win/spawn.c               | 3f7191e5c27a0e1852fe046a5ec0512a47e4a409 |
| 功能特性变更       | 添加检索所有环境变量的能力                 | uv_get_env                          | unix/env.c, win/env.c    | 2480b6158a3a21da564bdb565c4db827df176a4e |
| 功能特性变更       | 新增 uv_fs_statfs() 函数                  | uv_fs_statfs                        | unix/fs.c, win/fs.c      | bf86d5fbaf603a508bb7762c5d7e5800499aca96 |
| 功能特性变更       | 添加对 UDP 连接套接字的支持                | uv_udp_init, uv_udp_connect         | unix/udp.c, win/udp.c    | 90415a3394f51056e037a8a4d5a6ada6a710fd42 |
| 功能特性变更       | 增加设置新线程堆栈大小的功能              | uv_thread_create                    | thread.c                  | 0eca049a9b3ca7440b4a4c00ab0ebe57cc3ff948 |
| 功能特性变更       | 添加 uv_os_uname() 函数                   | uv_os_uname                         | unix/os.c, win/os.c      | d4288bbeab134277d20af672c0997ee23641d9aa |
| 功能特性变更       | 添加通过 fsevents 监视 macOS 文件的能力   | uv_fs_event_start                   | unix/fs.c                 | 2d2af382ce84b91d6ee7a185af32fca7f0acd84b |
| 功能特性变更       | 实现 uv_fs_event* 函数                    | uv_fs_event_start, uv_fs_event_stop | unix/fs.c, win/fs.c      | b01de7341f40e1f30d78178442b0b87a46b3b7a7 |
| 功能特性变更       | 改进内存分配器的自定义功能                  | uv_set_allocator                    | core/allocator.c          | bddd6a8489e4c8cf47841de6f05becd99fc06f3e |
| 功能特性变更       | 增加 uv_os_getpid() 函数                   | uv_os_getpid                        | unix/os.c, win/os.c      | d708df110a03332224bd9be1bbd23093d9cf9022 |
| 非功能特性变更     | 修复 uv_async_send() 在特定情况下未工作的错误 | uv_async_send                       | async.c                   | a787a16ac371b2c5ed5c8a61a5602e71beff81e0 |
| 非功能特性变更     | 修复 uv_spawn() 中的内存泄漏问题           | uv_spawn                            | process.c                 | 55cc5bac1b6521f876b4db0f290e7992fe2b2802 |
| 非功能特性变更     | 修复在 Linux 中使用预读和预写的条件        | uv_fs_read, uv_fs_write             | unix/fs.c                 | fef619608bda33a7cb37e78f08ee8abbb62458a3 |
| 非功能特性变更 | uv_run()执行路径优化 | uv_run() | src/uv-common.c | 24d1d0802d2c6ff6d0b2e556c0c2b1a5ebf33493 |
| 非功能特性变更     | 修复与过程中标准输入输出相关的错误         | uv_spawn                            | process.c                 | 5fd2c406f1a990f5f4c081b92d3108a0c999848e |
| 非功能特性变更     | 修复 uv_fs_copyfile() 的部分读取/写入错误 | uv_fs_copyfile                      | unix/fs.c, win/fs.c      | d1bc886e66ec356b16de897373f57a4ae488424b |
| 非功能特性变更     | 修复调用系统调用的错误处理方式              | uv__open_cloexec                    | unix/fs.c                 | 02e7a78628e5373a17b6b19d0c81cc1d12739aa4 |
| 非功能特性变更     | 修复 uv_close() 的功能以更接近于 Unix 的实现 | uv_close                            | core/handle.c             | 99eb736b4c81c8a00aa52ebd75de7198fbbcddbe |
- 该版本的变更为 `uv_io_t` 模块添加了多个新功能，包括对 UDP 套接字的支持、增强的文件系统监控能力、系统信息获取接口等，同时修复了多个性能和稳定性问题。
- 修复了多个内存泄漏、文件 I/O 错误及标准输入输出的相关问题，显著提升了模块的健壮性和性能。
- 此次变更增强了跨平台能力，尤其是在 macOS 和 Linux 上的文件系统监控与 I/O 操作方面。

#### **Test**

| 变更类型       | 变更内容       | 关键函数       | 相关文件       | Commit ID       |
| -------------- | -------------- | -------------- | -------------- | --------------- |
| 功能特性变更       | 增加了对无文件扩展名可执行路径的选择性处理 | uv_spawn | win/spawn | 3f7191e5c27a0e1852fe046a5ec0512a47e4a409 |
| 功能特性变更       | 添加了获取所有环境变量的功能 | uv_getenv | unix,win | 2480b6158a3a21da564bdb565c4db827df176a4e |
| 功能特性变更       | 增加了新的文件状态查询接口 | uv_fs_statfs | unix,win | bf86d5fbaf603a508bb7762c5d7e5800499aca96 |
| 功能特性变更       | 引入了受限内存的获取功能 | uv_get_constrained_memory | unix,win | c4e9657d59723a6273ce68bda935680e1b3596c5 |
| 功能特性变更       | 支持UDP连接的套接字 | uv_udp_open | unix,win | 90415a3394f51056e037a8a4d5a6ada6a710fd42 |
| 功能特性变更       | 允许指定新线程的堆栈大小 | uv_thread_create | unix,win | 0eca049a9b3ca7440b4a4c00ab0ebe57cc3ff948 |
| 功能特性变更       | 定义最大主机名大小 | UV_MAXHOSTNAMESIZE | include, src | 8865e72e25fc8aba94da7c9e18c3b5629d288ecc |
| 功能特性变更       | 增加对文件复制的基础支持 | uv_fs_copyfile | unix,win | 766d7e9c0b8eca53b864764b735682d814c56350 |
| 功能特性变更       | 添加获取主机名功能 | uv_os_gethostname | unix,win | d8cd08bd985b0d4f16f76c6c726b5b938b2ee9ee |
| 功能特性变更       | 为早餐创建路径支持 | uv_os_tmpdir | unix,win | c0fa2e7518a3a0e364c56f8223bdd0f549ddac66 |
| 功能特性变更       | 支持设置线程的优先级 | uv_os_set_priority | unix,win | e57e07172eba9df2f8fa0cec051cac0c5cac9124 |
| 功能特性变更       | 增加了试探性写入功能 | uv_try_write | stream | b5e7798a89411a732e31b436731e17dbc94505d3 |
| 功能特性变更       | 增加了线程池的支持 | uv_threadpool | unix,win | 0cca5391ba8513d22f1c9cdc4a462f6dfd7230c5 |
| 功能特性变更       | 引入了条件变量的支持 | uv_cond_t | unix,windows | 976c8a4387e5ca4d021924dcf22b9cb9c8c638a8 |
| 非功能特性变更     | 修复了目录创建返回无效名称的错误 | uv_fs_mkdir | win/fs | ecff27857dafe3f5d30a6ab8646ea69a93e4940a |
| 非功能特性变更     | 修复了在运行时关闭文件的错误处理 | uv_pipe_connect | unix,win | 6bbccf1fe0e000fd73e945368466cd27291483e3 |
| 非功能特性变更     | 修复时序逻辑 | uv_timer_set_order | unix, windows | f6d8ba3c9a445578baa08267128228ebfa2bc7e3 |
| 非功能特性变更     | 修复管道和套接字关闭后的错误 | uv_pipe_close | unix,win | 8bcd689c048af5aab26842ac5ff903fa3192d57c |
| 非功能特性变更     | 修复多进程复制过程中路径问题 | uv_fs_rename | unix,win | 43e3ac579871819f7730cf60374e49b7ec81fd1f |
| 非功能特性变更     | 修复对隐藏环境变量的读取问题 | uv_getenv | win | fd1502f5630591bf8ce79502df9b5d76868dfd3b |
| 非功能特性变更     | 修复影响阻塞行为的内存泄漏 | uv_fs_scandir | unix,win | b00d1bd225b602570baee82a6152eaa823a84fa6 |
| 非功能特性变更     | 修复竞争条件导致的回调问题 | uv_callback | test | d41749d546e70c5456c13c8741c7784c2c4b2048 |
| 非功能特性变更     | 修复调用未初始化的STDIO管道的问题 | uv_spawn | process | 7108ca885341a81b405c71ecd1b12efc632504fb |
| 非功能特性变更     | 优化了UDP接收性能 | uv_udp_recv | win | dff3f8ccabee15b1545523329e39e7acd2e77563 |
| 非功能特性变更     | 解决在关闭无效FD后访问而导致的问题 | uv_cleanup_fd | unix,win | e4fcd8bca7ded2e25fa8ad0b31933562e7bb8621 |

此次变更带来了多个功能性和修复性更新，尤其是在文件操作、网络连接、线程池管理等方面进行了扩展，增强了跨平台的支持和性能。非业务变更方面，修复了多项错误和提升了稳定性。新的功能和修复将对提高模块的可用性和性能产生积极影响，特别是在处理文件操作和网络通信方面。

#### **Network_I/O**

| 变更类型       | 变更内容       | 关键函数       | 相关文件       | Commit ID       |
| -------------- | -------------- | -------------- | -------------- | --------------- |
| 功能变更       | 实现了ifaddrs、getifaddrs 和 freeifaddrs功能 | ifaddrs, getifaddrs, freeifaddrs | ibmi相关文件 | d83fadaf098024857fda42b0d0becc9797339145 |
| 功能变更       | 添加TCP_KEEPINTVL和TCP_KEEPCNT支持 | TCP_KEEPINTVL, TCP_KEEPCNT | darwin相关文件 | 65541f772f7209d8273395fb3e99ea0f0bbfb73e |
| 功能变更       | 添加对UDP连接套接字的支持 | uv_udp_open | 相关文件 | 90415a3394f51056e037a8a4d5a6ada6a710fd42 |
| 功能变更       | 添加uv_os_uname函数实现 | uv_os_uname | unix、win相关文件 | d4288bbeab134277d20af672c0997ee23641d9aa |
| 功能变更       | stream自动检测方向 | uv_fs_event* | stream相关文件 | 40498795ab457dfa3a00a5aad45ba9db3bf71588 |
| 功能变更       | 允许在绑定的套接字上使用uv_udp_open | uv_udp_open | 相关文件 | 03061d54f0730e1565aedecf11b361053e5897a9 |
| 功能变更       | 实现uv_fs_event相关函数 | uv_fs_event* | zos相关文件 | b01de7341f40e1f30d78178442b0b87a46b3b7a7 |
| 功能变更       | 添加uv_os_getpid函数 | uv_os_getpid | unix、win相关文件 | d708df110a03332224bd9be1bbd23093d9cf9022 |
| 功能变更       | 允许NULL循环以同步fs请求 | 相关函数 | unix、windows相关文件 | df62b54aa2b3d916ca442ee84f0678129a848c4f |
| 功能变更       | 添加自定义内存分配器的能力 | 相关功能 | core相关文件 | bddd6a8489e4c8cf47841de6f05becd99fc06f3e |
| 功能变更       | 实现uv_stream_set_blocking | uv_stream_set_blocking | unix相关文件 | b36d4ff9301b39f5116474e435587418faafb21a |
| 功能变更       | 添加uv_get{addr,name}info的同步实现 | uv_get{addr,name}info | unix、win相关文件 | f2bb8d394c06d06ee45e884600466321455751b6 |
| 功能变更       | 添加多个buffer的uv_try_write支持 | uv_try_write | stream相关文件 | 17d60e3f94f4b122f6412e78b10e40573637dfa1 |
| 功能变更       | 支持Android构建 | 相关功能 | unix相关文件 | fc6a2ad24fed0f8c9529d3ef785b0d5a153c3849 |
| 功能变更       | 实现UDP断开功能 | uv_udp_disconnect | ibmi相关文件 | c1128f3db3fe85039f9dc9423b353a3ad673a13a |
| 性能优化       | 修复在高网络负载下的事件循环饥饿 | 相关函数 | unix相关文件 | 738b31eb3aff440ae75ff9f32ba61086a948c3f4 |
| 性能优化       | 修复loop hang问题 | 相关函数 | unix相关文件 | 03f1a6979caff380bfcfcd1293390474eaad6164 |
| 漏洞修复       | 修复在connect调用后返回的不正确错误代码 | connect | 相关文件 | 13ca3bfae89511f9ad67c54b530c827fe092178b |
| 漏洞修复       | 修复UDP地址的错误处理 | uv_udp_bind | unix、windows相关文件 | 86cb5203b6275920c4548f8ef93a0f37165f9416 |
| 漏洞修复       | 修复关闭流后清理的bug | uv_shutdown | 相关文件 | 3a8c3987d6dcc291caef9455461d9f7d5a3443e8 |
| 漏洞修复       | 修复信号处理中的errno覆盖问题 | 相关函数 | unix相关文件 | 7f3c7835831c9308ee3728883db0f77ab4dbf7df |

本次变更对`Network_I/O`模块进行了多个方面的扩展和优化。通过增加对TCP、UDP协议的支持、强化跨平台能力以及提升文件系统事件和I/O处理能力，模块的功能更加完备。同时，通过修复性能瓶颈和漏洞问题，确保了系统在高负载情况下的稳定性和健壮性。整体来看，这些变更大幅提升了模块的灵活性、稳定性和跨平台支持能力，适应了更多的应用场景和需求。

#### **Utility**

| 变更类型       | 变更内容       | 关键函数       | 相关文件       | Commit ID       |
| -------------- | -------------- | -------------- | -------------- | --------------- |
| 功能特性变更       | 增加了获取所有环境变量的功能                       | uv_get_constrained_memory() | unix, win | 2480b615, c4e9657 |
| 功能特性变更       | 添加了获取、设置进程优先级的函数                  | uv_os_getpriority, uv_os_setpriority | unix, win | e57e07172, e57e07172 |
| 功能特性变更       | 添加了获取主机名、进程ID等功能                    | uv_os_gethostname, uv_os_getpid | unix, win | d708df110, d708df110 |
| 功能特性变更       | 增强了对在Windows XP上的支持                     | uv_if_indextoname | win | 17eaa956b, 17eaa956b |
| 功能特性变更       | 提供自定义内存分配器的功能                      | N/A | core | bddd6a848, bddd6a848 |
| 功能特性变更       | 增加了关于环境变量的处理功能                      | uv_os_tmpdir | unix, win | c0fa2e751, c0fa2e751 |
| 功能特性变更       | 在所有平台上增加了条件变量的支持                 | N/A | N/A | 976c8a438, 976c8a438 |
| 功能特性变更       | 添加了新的套接字功能和相关的网络支持              | N/A | N/A | 5c9d749a, fc263218 |
| 功能特性变更       | 进行了一系列针对Windows平台的增强和修复          | uv_winsock_init, uv_fs_stat | win | 6554954e, 855764406 |
| 非功能特性变更     | 修复了多个Windows和Unix相关的BUG对象              | N/A | N/A | 多个 |
| 非功能特性变更     | 改进了UV接口及其他相关API的实现                    | N/A | N/A | 多个 |
| 非功能特性变更     | 检查并修复了内存相关的潜在问题                     | heap, uv_dlerror | unix, windows | 多个 |
| 非功能特性变更     | 进行了多项编译器和平台兼容性增强                  | N/A | N/A | 多个 |

该次变更对 `Utility` 模块进行了多个增强和修复，主要涉及环境变量处理、进程管理、内存管理和跨平台支持等方面。新增功能和优化将显著提高模块的稳定性和跨平台兼容性，特别是在 Windows 系统上。通过修复 BUG 和改进性能，系统的整体运行效率和可靠性也得到了提升。


#### **File_I/O**

| 变更类型       | 变更内容                                       | 关键函数                   | 相关文件       | Commit ID                                            |
| -------------- | ---------------------------------------------- | -------------------------- | -------------- | ---------------------------------------------------- |
| 功能特性变更       | 增加多个文件系统操作的支持，包括文件状态、复制等功能 | uv_fs_statfs, uv_fs_copyfile, uv_open_osfhandle |    | bf86d5fbaf603a508bb7762c5d7e5800499aca96, 766d7e9c0b8eca53b864764b735682d814c56350 |
| 功能特性变更       | 客户端在不同操作系统下增加了对用户符号链接和事件功能的支持 | uv_fs_event_start, uv_fs_event_stop |    | 89d31932a595fdec18dd19b70142816312ea2338, 9d44d786ada6cf94e1bdcee7d777c790ca712a78  |
| 功能特性变更       | 系统日志和错误处理的增强                      | uv_fs_scandir, uv_fs_write |    | a8017fd8a2584550966e0eecbb07467934031d84, 4fb120f6494677ebfab0028a2f7b0cfd7dca09c4 |
| 功能特性变更       | 文件访问及权限检查更新                        | uv_fs_access, uv_fs_chmod |    | 7dcc3e0cf02e54efc99b041f3cd871107f19ebf1, 9f932f92cfed14f5dc1bfa7371bab64980f102be |
| 非功能特性变更     | 修复多个平台下的内存泄漏和并发问题          | uv_fs_poll_stop, uv_fs_event_stop |    | b00d1bd225b602570baee82a6152eaa823a84fa6, 6c760b62073b50a7de284111c6b1c57f73e6d370 |
| 非功能特性变更     | 优化文件系统操作中的错误提示和返回值的处理 | uv_fs_read, uv_fs_write   |    | 23796d208c1309270ee09ff566d00859cdf2e35b, 263516e0a0026fcb59cbb511400da9290e032bf6 |
| 非功能特性变更     | 添加多平台支持及增强对无效句柄的处理        | uv_statfs, uv_mkdtemp     |    | 076df64dbbda4320f93375913a728efc40e12d37, b0c1a3803ab93c93404fd0c00d809ae678a4f43a |
| 非功能特性变更     | 增强对文件IO的性能优化                       | uv_fs_stat, uv_fs_sendfile |    | 855764406e3a1e92370460b87062d745f59b56cc, f9ad0a7bf65c229e50fea90e58757d14684ea9b3 |

本次变更增强了 `File_I/O` 模块的功能性，特别是在跨平台文件操作的支持上，包括文件状态、复制和权限管理等。与此同时，多个平台的内存泄漏和并发问题得到修复，性能得到了优化。总体来看，变更提升了该模块的可用性和稳定性，减少了系统在高负载下的潜在故障，增强了错误提示与处理能力，为开发人员提供了更可靠的文件系统操作接口。

#### **IOCP**

| 变更类型       | 变更内容       | 关键函数       | 相关文件       | Commit ID       |
| -------------- | -------------- | -------------- | -------------- | --------------- |
| 功能特性变更       | 新增对UDP连接套接字的支持，允许使用UDP连接和选择UDP套接字选项 | uv_udp_open, uv_udp_set_multicast_loop, uv_udp_set_ttl | udp.c, tcp.c | 90415a3394f51056e037a8a4d5a6ada6a710fd42, 0c283630590142cbc6348cce3c9a7f2c82784096, 726e36cf7c1daf8b1ecb2d46e1d5eee07b52c7a1 |
| 功能特性变更       | 支持对Windows中的命名管道的实现 | uv_pipe_listen, uv_pipe_connect | pipe.c | b6a6dae34f01814ad1d19f8ffcc3f77c234432f5 |
| 功能特性变更       | 新增uv_try_write和uv_try_write2函数以增强流的写操作支持 | uv_try_write, uv_try_write2 | stream.c | b5e7798a89411a732e31b436731e17dbc94505d3, bcc4f8fdde45471f30e168fe27be347076ebdf2c |
| 功能特性变更       | 增加uv_fileno函数用于获取文件描述符 | uv_fileno | fs.c | 4ca9a363897cfa60f4e2229e4f15ac5abd7fd103 |
| 功能特性变更       | 新增uv_os_uname获取操作系统信息的功能 | uv_os_uname | os.c | d4288bbeab134277d20af672c0997ee23641d9aa |
| 非功能特性变更     | 优化Windows异常处理，提高错误报告的准确性 | GetLastError, SetErrorMode | win.c | 299d51c3edf213c98d0f41665ff5a19c2a0c1623 |
| 非功能特性变更     | 修复和优化数据转换，避免内存泄漏 | uv_tcp_nodelay, uv_tcp_keepalive | tcp.c | d15b88a9355fbd43c85cf15f97912066c90bbfeb, f880023b97b5eb79ea44917bc0c90039dca02395 |
| 非功能特性变更     | 修复uv_loop_init在内存不足时表现不符合预期的错误 | uv_loop_init | loop.c | 7284adfa7a833264fc67d68d39610da27ecbab7c |
| 非功能特性变更     | 修复在不同平台上socket发送和接收错误代码的一致性 | sock_send, sock_recv | socket.c | 9b4f2b84f10c96efa37910f324bc66e27aec3828 |
| 非功能特性变更     | 修复并提高fs/hwait的清理，确保资源正确释放 | fs_poll_close, fs_poll_init | fs.c | bdb5838eac6c159939455285955e3bf7d860ffd6 |
| 功能特性变更       | 增加对Windows XP的支持，提升兼容性 | uv_if_indextoname | win.c | 17eaa956bde35daad99b36b820daf8e8227add74 |
| 非功能特性变更     | 修复与线程创建和同步相关的多处问题 | uv_thread_create, uv_thread_join | thread.c | e900006642a5e8d4ab27a8760afcc03136f0dd8f |
| 非功能特性变更     | 修复在pipe和tcp连接中处理中断和错误的代码 | ipv4_connect, uv_tcp_accept | pipe.c, tcp.c | 2a51b61e460b43b6813425c239db1e5db6931fc9  |

这次变更针对IOCP模块的改进和扩展，增强了Windows平台的兼容性，特别是对UDP协议、命名管道的支持以及对Windows XP的适配。性能优化方面，修复了多个与内存泄漏、错误处理和线程同步相关的问题，提升了系统的稳定性和跨平台能力。新增的API如`uv_try_write`、`uv_fileno`、`uv_os_uname`等为开发者提供了更多控制和灵活性。这些变更将有效提升libuv在网络通信和文件操作中的表现，适用于更多平台和场景。

#### **Epoll**

| 变更类型       | 变更内容       | 关键函数       | 相关文件       | Commit ID       |
| -------------- | -------------- | -------------- | -------------- | --------------- |
| 功能增强       | 添加 uv_get_constrained_memory() 函数，支持获取系统内存限制 | uv_get_constrained_memory | unix，win 相关文件 | c4e9657d59723a6273ce68bda935680e1b3596c5 |
| 功能增强       | 实现 uv_fs_event* 函数 | uv_fs_event_start, uv_fs_event_stop | zos，unix，windows | b01de7341f40e1f30d78178442b0b87a46b3b7a7 |
| 功能增强       | 添加 strnlen() 函数的实现 | strnlen | 相关字符串操作文件 | 88d716e126b98d776bcb262d0dea87e6c139e40f |
| 功能增强       | 在 ARP 上设置物理地址 | 未提及 | sunos 相关文件 | d75e334e34487575bcb46f6311fefbdc4849a564 |
| 功能增强       | 增加 UV_DISCONNECT 事件到 poll | uv_poll | poll 相关文件 | c7c8e916b86d2b168e97b04d7b4c8913322c8329 |
| 功能增强       | 对无法轮询的文件描述符报告错误 | uv_poll | unix 相关文件 | a0b56059cfce1a923be17115fd5c666750f0497a |
| 功能增强       | 增加自定义内存分配器的能力 | 未提及 | core 相关文件 | bddd6a8489e4c8cf47841de6f05becd99fc06f3e |
| 功能增强       | 在 uv_poll_init 中设置非阻塞模式 | uv_poll_init | unix, windows 相关文件 | b30a3e677b144afa19143490e9ffc9f882cb4722 |
| 功能增强       | 在 poll 阻塞时增加阻塞 SIGPROF 的标志 | 未提及 | unix 相关文件 | 2daf9448b127f2849de735a76ff4f9a95184d64f |
| 功能增强       | 增加 netmask 到 uv_interface_address | uv_interface_address | unix, windows 相关文件 | 14aa6153bec48da8f247c099d903566794e2da0a |
| 功能增强       | 增加 flags 到 uv_fs_event_init | uv_fs_event_init | 相关文件 | 1997e10b507c467b1b25d2a22263620025eafbcf |
| 功能增强       | 在 sunos 中实现文件监控 API | 未提及 | sunos 相关文件 | 3e4af533ae4c11811d478ad52095763e318948d9 |
| 功能增强       | 实现 loadavg（不支持 cygwin/win） | 未提及 | os 相关文件 | a35591bbfce1c72cfc1108c35013adb55cabdbc1 |
| 功能增强       | 在 epoll 中添加事件端口支持 | 未提及 | epoll 相关文件 | caf22ddbf5b1b8d06006b24f3b50c5e698fe2d8c |
| 问题修复       | 避免无效文件描述符的无效化操作 | 未提及 | unix 相关文件 | 1ce6393a5780538ad8601cae00c5bd079b9415a9 |
| 问题修复       | 修复重复监控文件描述符的情况 | 未提及 | unix 相关文件 | 2256be01b0427ecfeb311c1af7e6bd079e0dc399 |
| 问题修复       | 初始化 pollfd 的 revents 字段 | pollfd | zos 相关文件 | 5f5d19d906320874e5ec249cb72fad8fa0d46c3f |
| 问题修复       | 修复 epoll_wait() 的提前退出问题 | epoll_wait | zos 相关文件 | 27eec099d60a3aa8a9e4e14906a6f79f98d1e67f |
| 问题修复       | 修复系统接口错误的统一报告 | 未提及 | sunos 相关文件 | 23796d208c1309270ee09ff566d00859cdf2e35b |
| 问题修复       | 修复 uv_poll 的 CPU 使用高峰问题 | uv_poll | unix 相关文件 | 2e3e658be1b89d23cad4c126d7e84e2ca1177586 |
| 问题修复       | 修复 fs 事件观察器的取消引用问题 | fs_event_watcher | unix 相关文件 | 38fc6ad839734a3f76d2535b8f62d92e9cfef8c7 |
| 问题修复       | 修复循环计数器的缺失递增 | 未提及 | 相关文件 | ba52023ef333d41129db2f51c9e507c623022b02 |
| 问题修复       | 修改 uv_get_*_memory() 函数的返回类型 | uv_get_*_memory | 相关文件 | d3967992107551988ef309465974eee67fb92c10 |
| 问题修复       | 解决 iovec 调用中的条件问题，确保与非 uv 调用一致 | 未提及 | 相关文件 | dc1d55dfec29d43b5446d97d545cb819b8284e8a |
| 问题修复       | 恢复事件端口的使用 | 未提及 | 相关文件 | 5fe597268e4e78dc84e481f57317a573356f63c2 |
| 问题修复       | 修复 Solaris 10 中缺少 strnlen 函数问题 | strnlen | 相关文件 | 8ea8f124386486af2380127c6885848f9d502a36 |
| 问题修复       | 修正条件判断错误，确保 ioctl 函数调用安全 | ioctl | 相关文件 | 6b0051d14decb22cab1ae7ee0adf0da99620cafe |
| 问题修复       | 确保快速重用文件描述符时的安全性 | 未提及 | 相关文件 | c9406ba0e3d67907c1973a71968b89a6bd83c63c |

此次变更主要聚焦在提升Epoll模块的功能性和性能，增强了跨平台的内存管理、文件描述符监控和事件处理能力，同时解决了一系列关键问题，包括高CPU使用率、文件描述符无效化等。整体而言，这些变更有助于提升模块的稳定性、性能和跨平台兼容性，为开发者提供更高效的工具和更安全的执行环境。

#### **kqueue**

| 变更类型   | 变更内容                                                   | 关键函数               | 相关文件             | Commit ID                                   |
| ---------- | ---------------------------------------------------------- | ---------------------- | -------------------- | ------------------------------------------- |
| 功能变更   | 增加了对 macOS 10.7 及以上版本使用 fsevents 的文件监控功能  | fsevents, uv_fs_event_start | fsevents.c, kqueue.c | 2d2af382ce84b91d6ee7a185af32fca7f0acd84b    |
| 功能变更   | 添加了 UV_DISCONNECT 事件支持                                | uv_poll_event, uv_fs_event_stop | poll.c, kqueue.c    | c7c8e916b86d2b168e97b04d7b4c8913322c8329    |
| 功能变更   | 支持 unix 系统报告无法进行轮询的文件描述符错误               | uv_poll_event           | unix.c               | a0b56059cfce1a923be17115fd5c666750f0497a    |
| 功能变更   | 支持通过 kevent 信号重新采集子进程的状态                    | kevent, process_reap    | darwin.c             | 42cc412c4aca0ff17ad40ad3e35b5386ae171dd5    |
| 功能变更   | 增加自定义内存分配器的功能                                  | uv_malloc, uv_free       | core.c               | bddd6a8489e4c8cf47841de6f05becd99fc06f3e    |
| 功能变更   | 增加标志以在轮询期间阻止 SIGPROF 信号                      | uv_fs_event_start       | unix.c, kqueue.c     | 2daf9448b127f2849de735a76ff4f9a95184d64f    |
| 功能变更   | 增加 uv_fs_event_start/stop 函数支持                         | uv_fs_event_start, uv_fs_event_stop | unix.c, windows.c   | 9d44d786ada6cf94e1bdcee7d777c790ca712a78    |
| 功能变更   | 使用 FSEvents 监控目录变化                                  | uv_fs_event_start       | darwin.c             | f8e7513a0618c33aef526abf76eb4bc99f0cdaa0    |
| 功能变更   | 增加 uv_fs_event_init 的标志                                | uv_fs_event_init        | kqueue.c             | 1997e10b507c467b1b25d2a22263620025eafbcf    |
| 功能变更   | 实现 kqueue 文件监视器 API                                  | uv_fs_event_start       | unix.c               | 8e9a3384c951b09f41c94b1a5d06f684a14bf03a    |
| Bug修复     | 修复 FreeBSD 系统在非 Intel 架构上的编译问题               | -                        | freebsd.c            | a407b232f06aa2f6d1031bf2d126725a4e9e2a54    |
| Bug修复     | 修复 kqueue 和 epoll 代码不一致的问题                      | -                        | unix.c               | 2f8275009854599ec7de68dbef795e82b6b5fb30    |
| Bug修复     | 修复 fs 事件路径获取问题                                    | fcntl(F_KINFO)         | freebsd.c            | 004dfd2d4b2bc3c3f2ddda7ac72c9dd579ca4194    |
| Bug修复     | 修复 macOS 旧版本系统回退到 kqueue 时的错误                | -                        | macos.c              | 6602fca820d0d3cb42acb7dd096d567a5f1db16d    |
| Bug修复     | 修复 uv_fs_event_start 错误路径文件描述符泄漏               | uv_fs_event_start       | kqueue.c             | 09ba4778d8a8d36b652c714c2cc6557b7e945ee2    |
| Bug修复     | 修复无效的文件描述符的无效操作                              | uv_fs_event_stop        | unix.c               | 1ce6393a5780538ad8601cae00c5bd079b9415a9    |
| Bug修复     | 修复 events_waiting 指标计数器的问题                        | events_waiting          | src.c                | e02642cf3b768b2c58a41f97fa38507e032ae415    |
| Bug修复     | 使用 C11 原子操作以提升性能                                | atomic_operations       | src.c                | 2f33980a9141bd49cb2c34361854355b23b1e6fc    |
| Bug修复     | 修复 kqueue 事件无效处理导致的段错误                        | uv__io_poll             | osx.c                | f166d6d7055bbd9da83594b045a496e15b3c302a    |
| Bug修复     | 修复 FSEvents 的线程不安全问题                              | fsevents                 | fsevents.c           | 303ae3b958eb0fb433589e86370652ec8d99f3c8    |
| Bug修复     | 修复文件路径查找功能                                        | F_GETPATH               | darwin.c             | 145f7b3560541cd897440940a00c5c0c52f09f9f    |
| Bug修复     | 修复 ngx-queue.h 文件未删除                                 | -                        | unix.c               | 0635e297148ae8cd4065013002de4bbaab72449f    |
| Bug修复     | 修复 libeio 库文件删除问题                                  | -                        | unix.c               | b60a24a206f21a139912eb5d847a9b1ac77187dc    |
| Bug修复     | 修复 kqueue 文件系统监视器编译条件问题                      | -                        | unix.c               | 3c415975d90c96083d9bb97aa937f24d2644b50a    |
| Bug修复     | 修复 NOTE_EXIT 失败后的挂起问题                             | kevent, NOTE_EXIT       | process.c            | bae2992cb0d4b9dd1f8e0fb5f3e01651dbf5c4d6    |
| Bug修复     | 修复 kevent NOTE_EXIT 失败处理问题                          | kevent, NOTE_EXIT       | process.c            | 953f901dd2330a9979838cd43ff04eacde71b25a    |
| Bug修复     | 修复 darwin 系统中的 fs_event 引用计数问题                  | fs_event_refcount       | darwin.c             | b3fe1830409fff6a55131af3156654ee4a712426    |
| Bug修复     | 修复 fs_event 取消引用问题                                  | fs_event_unref          | unix.c               | 38fc6ad839734a3f76d2535b8f62d92e9cfef8c7    |
| Bug修复     | 修复 kqueue 事件触发后编译警告问题                          | kqueue.c, tcp.c, udp.c  | kqueue.c, tcp.c      | c89a75f5a277991fac7ebf281ac977cd56692078    |
| Bug修复     | 修复 kqueue 文件系统监视器未正常取消引用的问题              | kqueue_fs_watcher_unref | unix.c               | 1e0aab06c92838b427ecf41ead62d1e5fcc8e4c5    |

该版本的 kqueue 模块通过引入 fsevents 支持和多项功能增强，显著提升了文件事件监控的能力，特别是在 macOS 平台上的表现。通过新增对 UV_DISCONNECT 事件、子进程状态管理、内存分配器支持等功能的支持，使得网络和文件操作的处理更为灵活和高效。同时，多项 Bug 修复和性能优化确保了系统的稳定性和跨平台兼容性。总体而言，这些变更提升了 kqueue 模块的性能、功能和可靠性，满足了更复杂的异步 I/O 和文件监控需求。

#### **DNS_Ops**

| 变更类型       | 变更内容       | 关键函数       | 相关文件       | Commit ID       |
| -------------- | -------------- | -------------- | -------------- | --------------- |
| 功能特性变更       | 增加对 Windows XP 的支持，修改 uv_if_indextoname() 函数。 | uv_if_indextoname | src/win/dns.c | 17eaa956bde35daad99b36b820daf8e8227add74 |
| 功能特性变更       | 使用本地 API 进行 UTF 转换。 | 无               | src/win/dns.c | f04d5fc3b98cfa6699b9d0b2dedda84a14689761 |
| 功能特性变更       | 增加自定义内存分配器的支持。 | 无               | src/core/memory.c | bddd6a8489e4c8cf47841de6f05becd99fc06f3e |
| 功能特性变更       | 增加同步的 uv_get{addr,name}info 函数。 | uv_getaddrinfo, uv_getnameinfo | src/unix/dns.c, src/win/dns.c | f2bb8d394c06d06ee45e884600466321455751b6 |
| 功能特性变更       | 实现 getnameinfo 函数。 | getnameinfo       | src/unix/dns.c, src/win/dns.c | 70c42563c1df750ca4700582c9904806f30836ed |
| 性能优化       | 如果操作系统支持，使用 GetQueuedCompletionStatusEx 提升性能。 | 无               | src/win/dns.c | fc2632189019baf7f0d1b87f6953320927a756b2 |
| 功能修复       | 修复 IDNA 输入为空时的处理问题。 | 无               | src/core/idna.c | e0327e1d508b8207c9150b6e582f0adf26213c39 |
| 功能修复       | 限制并发 DNS 调用的线程数。 | uv_getaddrinfo, uv_getnameinfo | src/unix/dns.c, src/win/dns.c | 90891b4232e91dbd7a2e2077e4d23d16a374b41d |
| 功能修复       | 修复 uv__getnameinfo_work() 错误处理。 | uv__getnameinfo_work | src/win/dns.c | 76b873e8371be4d8b036ad78d1a9674f94655301 |
| 功能修复       | 修复 GetNameInfoW 错误处理。 | GetNameInfoW      | src/win/dns.c | 7bdcf3dc7ea2bc92cde91a4082b76e111cc07db7 |
| 功能修复       | 修复 uv__getaddrinfo_translate_error 函数中的问题。 | uv__getaddrinfo_translate_error | src/win/dns.c | c87c44fff3f28040159db6ad08134a647e85aacf |
| 功能修复       | 修复 buffer overflow 问题。 | uv__getnameinfo_work | src/win/dns.c | 89fc7d80c46154976a0eeb53087f5c9539528c24 |
| 功能修复       | 修复 OOB 读取问题，在 punycode 解码器中。 | 无               | src/core/punycode.c | b7466e31e4bee160d82a68fca11b1f61d46debae |
| 性能优化       | 如果只有一个 iovec 进行读写操作，则使用非 uv 版本的系统调用。 | 无               | src/core/io.c | dc1d55dfec29d43b5446d97d545cb819b8284e8a |
| 功能特性变更       | 移除 ngx-queue.h 头文件。 | 无               | src/unix/dns.c | 0635e297148ae8cd4065013002de4bbaab72449f |
| 功能特性变更       | 移除 libeio 库。 | 无               | src/core/io.c | b60a24a206f21a139912eb5d847a9b1ac77187dc |
| 功能修复       | 统一操作系统错误报告。 | 无               | src/core/error.c | 23796d208c1309270ee09ff566d00859cdf2e35b |

DNS_Ops模块的变更不仅增加了对旧版本操作系统的支持，还通过引入新功能和优化现有处理逻辑显著增强了模块的性能和安全性。这些变更将提升模块在各种环境中的适用性，并改善用户体验，确保其在现代网络环境中的有效性与稳定性。

---

### 2. 功能特性变更总结

(1) **Thread_Pool_Management**

- **线程池大小限制增加**：增加了 `UV_THREADPOOL_SIZE` 的限制，提升了线程池的容量。
- **栈大小可配置**：引入了新功能，允许为线程指定自定义的栈大小。
- **自定义信号量**：支持自定义信号量的使用，提高了线程池的灵活性。
- **io_uring 支持**：为 Linux 系统增加了对 `io_uring` 的支持，提升了 I/O 操作的性能。
- **线程亲和性支持**：为线程池提供了线程亲和性支持，使得线程可以绑定到特定的 CPU 核心上。

(2) **uv_io_t**

1. **添加支持无扩展名的可执行路径运行**  
   - 通过 `uv_spawn` 函数支持在无扩展名的可执行路径上启动进程。
   - 关键函数: `uv_spawn`
   - 影响文件: `win/spawn.c`

2. **添加检索所有环境变量的能力**  
   - 新增了 `uv_get_env` 函数，允许检索所有环境变量，提供更高的灵活性。
   - 关键函数: `uv_get_env`
   - 影响文件: `unix/env.c`, `win/env.c`

3. **新增 `uv_fs_statfs()` 函数**  
   - 新增文件系统统计函数，返回文件系统的信息。
   - 关键函数: `uv_fs_statfs`
   - 影响文件: `unix/fs.c`, `win/fs.c`

4. **添加对 UDP 连接套接字的支持**  
   - 新增对 UDP 套接字的支持，提供 `uv_udp_init` 和 `uv_udp_connect` 等函数来初始化和连接 UDP 套接字。
   - 关键函数: `uv_udp_init`, `uv_udp_connect`
   - 影响文件: `unix/udp.c`, `win/udp.c`

5. **增加设置新线程堆栈大小的功能**  
   - 新增 `uv_thread_create` 函数，支持设置线程堆栈大小。
   - 关键函数: `uv_thread_create`
   - 影响文件: `thread.c`

6. **添加 `uv_os_uname()` 函数**  
   - 新增函数 `uv_os_uname()` 获取系统信息。
   - 关键函数: `uv_os_uname`
   - 影响文件: `unix/os.c`, `win/os.c`

7. **添加通过 fsevents 监视 macOS 文件的能力**  
   - 在 macOS 平台上，通过 fsevents 增强文件事件监控。
   - 关键函数: `uv_fs_event_start`
   - 影响文件: `unix/fs.c`

8. **实现 `uv_fs_event*` 函数**  
   - 新增文件事件监控函数，支持启动和停止文件事件的监控。
   - 关键函数: `uv_fs_event_start`, `uv_fs_event_stop`
   - 影响文件: `unix/fs.c`, `win/fs.c`

9. **改进内存分配器的自定义功能**  
   - 增强了内存分配器的自定义功能，可以通过 `uv_set_allocator` 设置自定义内存分配器。
   - 关键函数: `uv_set_allocator`
   - 影响文件: `core/allocator.c`

10. **增加 `uv_os_getpid()` 函数**  
    - 新增函数 `uv_os_getpid()` 获取进程 ID。
    - 关键函数: `uv_os_getpid`
    - 影响文件: `unix/os.c`, `win/os.c`

(3) **Test**

- **增加对无文件扩展名可执行路径的选择性处理**：通过 `uv_spawn` 在 Windows 平台上处理无扩展名的可执行文件路径，改善了路径的灵活性。
- **获取所有环境变量的功能**：通过 `uv_getenv` 增强了环境变量访问的功能，支持所有平台。
- **新增文件状态查询接口**：引入了 `uv_fs_statfs`，用于获取文件系统的状态信息，支持平台为 Unix 和 Windows。
- **受限内存获取功能**：引入了 `uv_get_constrained_memory`，为资源有限的环境提供内存管理功能。
- **UDP连接的套接字支持**：通过 `uv_udp_open` 提供了对 UDP 套接字的支持，增强了网络功能。
- **线程堆栈大小设置功能**：支持在创建线程时设置堆栈大小，通过 `uv_thread_create` 控制线程资源。
- **增加了文件复制功能**：通过 `uv_fs_copyfile` 提供了文件复制的基础支持。
  
(4) **Network_I/O**

- 实现了`ifaddrs`、`getifaddrs`和`freeifaddrs`功能（影响：增强了对网络接口的操作能力）。
  - 添加了对TCP协议中的`TCP_KEEPINTVL`和`TCP_KEEPCNT`支持（影响：提升了TCP连接的可控性和可靠性）。
  - 支持UDP连接套接字，增加`uv_udp_open`功能（影响：使UDP支持更为完备）。
  - 实现了`uv_os_uname`函数，支持Unix和Windows系统（影响：提供系统信息获取能力）。
  - 增加了stream自动检测方向功能（影响：提升了stream的灵活性和自适应性）。
  - 允许在绑定的套接字上使用`uv_udp_open`（影响：增强了UDP套接字的可操作性）。
  - 实现了与`uv_fs_event`相关的函数（影响：增强文件系统事件处理的能力）。
  - 新增`uv_os_getpid`函数（影响：提供了跨平台的进程ID获取功能）。
  - 允许NULL循环以同步fs请求（影响：提高了文件操作的灵活性）。
  - 提供了自定义内存分配器的能力（影响：增强了内存管理的定制性和优化能力）。
  - 实现了`uv_stream_set_blocking`（影响：提供了stream的阻塞设置功能）。
  - 实现了`uv_get{addr,name}info`的同步版本（影响：提供了更加一致的API）。
  - 支持多个buffer的`uv_try_write`（影响：提升了数据写入的性能）。
  - 支持Android构建（影响：扩展了支持的平台，增加了Android的兼容性）。
  - 实现了UDP断开功能（影响：加强了UDP连接的管理能力）。

(5) **Utility**

- 增加了获取所有环境变量的功能，提供更强的跨平台支持。
- 提供了对进程优先级的管理功能，可以在多个平台上调整优先级。
- 新增了获取主机名和进程 ID 的能力，扩展了系统信息的获取功能。
- 加强了 Windows XP 平台的支持，优化了系统兼容性。
- 提供了自定义内存分配器的功能，允许开发者根据具体需求进行内存管理。
- 增加了条件变量的跨平台支持，改进了线程同步机制。
- 新增了套接字功能和网络支持，增强了网络通信能力。

(6) **File_I/O**

- **文件系统操作的扩展**：
  - 新增了文件状态、复制等操作，包括 `uv_fs_statfs`、`uv_fs_copyfile` 和 `uv_open_osfhandle` 等函数。
  - 客户端在不同操作系统下，增加了对用户符号链接和事件功能的支持，使用了 `uv_fs_event_start` 和 `uv_fs_event_stop`。
  - 增强了系统日志和错误处理机制，涉及 `uv_fs_scandir` 和 `uv_fs_write` 等函数。
  - 文件访问及权限检查功能得到了更新，支持 `uv_fs_access` 和 `uv_fs_chmod` 等操作。
- **日志与错误处理**：
  - 强化了日志记录，增强了错误提示和相关功能的反馈。

(7) **IOCP**

- **文件系统操作的扩展**：
- **UDP连接套接字支持**：通过`uv_udp_open`、`uv_udp_set_multicast_loop`、`uv_udp_set_ttl`等函数的新增，支持UDP协议的高效通信，扩展了支持的网络协议范围。
- **命名管道实现**：在Windows平台上新增命名管道的支持，增强了IPC（进程间通信）的功能，特别是Windows环境下的进程间数据传输能力。
- **流写操作增强**：新增的`uv_try_write`和`uv_try_write2`函数，优化了流写入操作，提供了非阻塞的写操作支持，使得I/O操作更高效。
- **文件描述符获取功能**：`uv_fileno`函数的新增，使得程序能够直接获取文件描述符，在底层I/O操作中提供了更多的控制和灵活性。
- **操作系统信息获取**：`uv_os_uname`函数的引入，增强了系统信息的获取，尤其在需要获取系统信息进行平台适配时非常有用。

(8) **Epoll**

- **添加 uv_get_constrained_memory() 函数**：此函数支持获取系统内存限制，增强了内存管理功能，适用于Unix和Windows平台。
- **实现 uv_fs_event* 函数**：提供了文件系统事件监控功能，能够在文件系统变化时触发事件。此功能已在Unix、Windows和z/OS平台实现。
- **添加 strnlen() 函数的实现**：为字符串操作提供了一个跨平台的实现，增强了字符串处理能力。
- **在 ARP 上设置物理地址**：为sunos平台的ARP协议栈增加了对物理地址的支持。
- **增加 UV_DISCONNECT 事件到 poll**：提升了对网络连接断开的检测能力，支持在事件循环中处理此类事件。
- **增加自定义内存分配器的能力**：允许开发者使用自定义的内存分配策略，提高了内存管理的灵活性。
- **在 uv_poll_init 中设置非阻塞模式**：增强了对非阻塞I/O的支持，提升了poll操作的性能。
- **增加 netmask 到 uv_interface_address**：为网络接口地址增加了子网掩码的获取能力，支持更细粒度的网络接口管理。

(9) **kqueue**

- **macOS 10.7 及以上版本支持 fsevents**：通过 fsevents 提供了更高效的文件变化监控方式，特别在 macOS 上提升了文件监控的准确性和性能。
- **新增 UV_DISCONNECT 事件支持**：对于网络操作中连接断开事件的支持，可以更好地处理断开连接时的清理工作。
- **增强对无法进行轮询的文件描述符错误的支持**：确保在文件描述符不可用时，能及时报告错误，避免出现不可预测的行为。
- **支持子进程状态的重新采集**：通过 kevent 信号对子进程的状态进行重新采集，增强了对进程管理的支持，特别在 macOS 上。
- **增加自定义内存分配器功能**：允许用户自定义内存管理方式，适应不同的内存分配需求，提升性能。
- **支持通过标志阻止 SIGPROF 信号**：提高了对轮询过程中的信号处理控制，确保不被 SIGPROF 中断。
- **uv_fs_event_start/stop 支持**：为文件事件监控接口添加了启动和停止的支持，增强了文件监控的灵活性和可控性。
- **通过 FSEvents 监控目录变化**：利用 FSEvents 改进了目录变化的监听和处理，提升了 macOS 下的文件监控能力。
- **改进了 kqueue 文件监视器 API**：新增 API 功能，使得文件监控机制更加健壮和灵活。

(10) **DNS_Ops**

- 支持 Windows XP 提升了模块的兼容性，扩大了其用户基础。
- 本地 API 的使用增强了 UTF 转换的效率和稳定性。
- 自定义内存分配器的加入为开发者提供了更灵活的内存管理选项。
- 新增的同步 `uv_get{addr,name}info` 函数优化了信息获取的可操作性。
- 实现的 `getnameinfo` 函数增强了 DNS 操作的功能，提供了更全面的解析能力。
- 修复多个错误和潜在的缺陷，增强了整体的稳定性与安全性，包括对 IDNA 输入的处理、并发调用的限制以及多处错误处理的改进。

---

### 3. 非功能特性变更总结

(1) **Thread_Pool_Management**

- **性能优化**：通过修改线程栈大小、优化信号量的实现等，增强了线程池的性能。
- **线程池线程堆栈优化**：优化了线程池线程的堆栈大小，默认设置为 8MB，避免了线程栈空间不足的问题。
- **修复线程饥饿问题**：解决了由于线程池线程调度不当导致的线程饥饿问题，确保线程的公平调度。
- **内存屏障优化**：在多个平台（如 Windows 和 Unix）上对 `uv_thread_join()` 操作进行了内存屏障的优化。

(2) **uv_io_t**

1. **修复 `bind/connect` 对于抽象套接字的处理**  
   - 修复了在使用抽象套接字时 `bind` 和 `connect` 函数的处理问题。
   - 关键函数: `uv_bind`, `uv_connect`
   - 影响文件: `unix/tcp.c`

2. **修复 `uv_async_send()` 在特定情况下未工作的错误**  
   - 修复了 `uv_async_send()` 在特定条件下无法正确工作的错误。
   - 关键函数: `uv_async_send`
   - 影响文件: `async.c`

3. **修复 `uv_spawn()` 中的内存泄漏问题**  
   - 修复了 `uv_spawn()` 在某些情况下可能导致的内存泄漏问题。
   - 关键函数: `uv_spawn`
   - 影响文件: `process.c`

4. **修复在 Linux 中使用预读和预写的条件**  
   - 修复了 Linux 上使用 `uv_fs_read` 和 `uv_fs_write` 时预读和预写的错误。
   - 关键函数: `uv_fs_read`, `uv_fs_write`
   - 影响文件: `unix/fs.c`

5. **修复与过程中标准输入输出相关的错误**  
   - 修复了 `uv_spawn()` 与进程的标准输入输出相关的错误。
   - 关键函数: `uv_spawn`
   - 影响文件: `process.c`

6. **修复 `uv_fs_copyfile()` 的部分读取/写入错误**  
   - 修复了在使用 `uv_fs_copyfile()` 进行文件复制时出现的部分读取和写入错误。
   - 关键函数: `uv_fs_copyfile`
   - 影响文件: `unix/fs.c`, `win/fs.c`

7. **修复调用系统调用的错误处理方式**  
   - 改进了系统调用错误处理，修复了 `uv__open_cloexec` 函数中的错误。
   - 关键函数: `uv__open_cloexec`
   - 影响文件: `unix/fs.c`

8. **修复 `uv_close()` 的功能以更接近于 Unix 的实现**  
   - 修复了 `uv_close()` 使其功能更接近于 Unix 平台上的实现。
   - 关键函数: `uv_close`
   - 影响文件: `core/handle.c`
9. **信号处理兼容性增强**：引入了 uv_loop_handle_signal() 机制，允许在事件循环以外注册并处理信号，从而改善了与异步子进程协作的能力。
10. **uv_run 执行路径优化**：统一了 uv_run() 在不同平台下的行为路径，提升了跨平台一致性和事件循环调度效率。

(2) **Test**
- **修复目录创建返回无效名称的错误**：通过 `uv_fs_mkdir` 修复了 Windows 上的目录创建问题，确保路径返回正确。
- **修复关闭文件时的错误处理**：修复了 `uv_pipe_connect` 在运行时关闭文件的错误处理，提高了稳定性。
- **时序逻辑修复**：通过 `uv_timer_set_order` 修复了定时器的时序逻辑问题，解决了不同平台的定时器行为不一致问题。
- **修复管道和套接字关闭后的错误**：通过 `uv_pipe_close` 修复了管道和套接字关闭后的错误，确保无误访问。
- **UDP接收性能优化**：通过 `uv_udp_recv` 提升了 UDP 数据包接收的性能，改善了网络传输的效率。
- **修复内存泄漏问题**：通过 `uv_fs_scandir` 修复了内存泄漏问题，解决了阻塞行为的影响。

(3) **Network_I/O**
- **性能优化**：修复了高负载情况下的事件循环饥饿问题，解决了`loop hang`问题，这些优化提高了网络I/O的稳定性和性能，确保在繁忙的网络条件下仍能保持高效。
- **漏洞修复**：通过修复`connect`错误返回、UDP地址错误处理和流关闭后的清理问题，显著提高了系统的健壮性和错误处理的准确性。

(4) **Utility**
- **Windows 和 Unix 平台的 BUG 修复**  
  修复了多个在 Windows 和 Unix 系统上的 BUG，提升了系统稳定性。

- **改进了 UV 接口和相关 API 实现**  
  对现有接口进行了优化，提升了 API 的效率和兼容性。

- **内存问题修复**  
  修复了与内存相关的潜在问题，增强了系统的内存管理能力。

- **编译器和平台兼容性增强**  
  进行了一系列的编译器和平台兼容性增强，保证了更广泛的系统支持。

(5) **File_I/O**
- **内存泄漏和并发问题修复**：
  - 修复了多个平台下的内存泄漏和并发问题，确保了系统的稳定性和性能。
  
- **文件操作优化**：
  - 优化了文件 I/O 中的错误提示和返回值处理，提高了操作的鲁棒性。
  - 增强了对无效句柄的处理，提高了系统的健壮性。
  
- **性能提升**：
  - 对文件 I/O 性能进行了优化，使用了 `uv_fs_stat` 和 `uv_fs_sendfile` 等函数，减少了文件操作时的延迟。

(6) **IOCP**
- **优化Windows异常处理**：通过优化`GetLastError`和`SetErrorMode`函数的使用，提高了错误报告的准确性，改进了Windows平台的异常处理机制。
- **修复数据转换问题**：修复了`uv_tcp_nodelay`和`uv_tcp_keepalive`的内存泄漏问题，提高了TCP通信中的数据转换性能。
- **修复内存不足时的`uv_loop_init`问题**：解决了内存不足时`uv_loop_init`的错误，确保了事件循环的正常初始化。
- **修复socket发送接收错误代码问题**：改进了不同平台间socket发送和接收错误代码的一致性，增强了跨平台的可靠性。
- **修复资源释放问题**：改进了`fs_poll_close`和`fs_poll_init`的清理工作，确保资源得以正确释放，避免了内存泄漏。
- **多线程同步问题修复**：修复了多线程创建和同步中的问题，提升了线程池和线程管理的稳定性。
- **修复管道和TCP连接中的中断与错误处理**：修复了在`pipe`和`tcp`连接中处理中断和错误的代码，提升了错误处理的准确性和可靠性。

(7) **Epoll**
- **修复文件描述符无效化操作**：避免了因无效文件描述符引发的问题，提高了系统的稳定性。
- **修复重复监控文件描述符的情况**：解决了文件描述符被多次监控的问题，避免了资源浪费。
- **修复 epoll_wait() 提前退出问题**：改进了事件等待机制，确保epoll等待能正确完成。
- **修复系统接口错误的统一报告**：增强了系统接口错误的报告机制，提高了系统的可调试性。
- **修复 CPU 使用高峰问题**：通过优化 uv_poll 机制，降低了在某些情况下的CPU使用率。
- **修复 fs 事件观察器的取消引用问题**：解决了文件系统事件监控器的内存访问错误问题，避免了程序崩溃。
- **修复 Solaris 10 中缺少 strnlen 函数问题**：解决了Solaris 10平台上缺少 strnlen 函数的问题，增强了兼容性。
- **修正条件判断错误，确保 ioctl 函数调用安全**：解决了ioctl调用中存在的条件判断问题，确保系统稳定运行。
- **确保快速重用文件描述符时的安全性**：增强了对文件描述符重用过程中的安全性，防止了潜在的资源泄露和冲突。

(7) **kqueue**
- **性能优化**：修复了多个性能瓶颈问题，例如在使用 C11 原子操作优化性能、修复 FSEvents 的线程不安全问题等，提升了文件监控的稳定性和性能。
- **漏洞修复**：
  - 修复了 FreeBSD 系统在非 Intel 架构上的编译问题，解决了跨平台兼容性问题。
  - 解决了 kqueue 和 epoll 代码不一致的问题，确保了跨平台的一致性。
  - 修复了 kqueue 事件触发后的段错误问题，增强了稳定性。
  - 解决了 uv_fs_event_start 错误路径文件描述符泄漏等问题，避免了资源泄漏。
  - 修复了 FSEvents 线程不安全问题，确保文件事件监控更加可靠。
  - 修复了 kqueue 文件系统监视器编译条件问题，确保在不同环境下的正确编译。

(8) **DNS_Ops**
- 性能优化通过支持 `GetQueuedCompletionStatusEx` 提升了响应速度和处理效率。 
- 修复 buffer overflow 和 OOB 读取问题显著增强了模块的安全性，防止潜在的安全漏洞导致的攻击风险。
- 除了性能和安全提升外，限制并发 DNS 调用的线程数优化了资源使用，避免了线程过度竞争与饱和带来的不必要资源耗损。


---

### 4. 组件变更

- **I/O Loop**：
  - 增加了TCP、UDP协议的支持功能，增强了I/O操作的灵活性和可靠性。
  - 提供了对跨平台系统操作的支持，增加了进程信息和网络接口的处理能力。
  - 作为I/O句柄的管理组件，提供了对不同类型套接字和流的管理，提升了网络通信的处理能力。
  - 确保了在不同平台下高效的I/O轮询和非阻塞操作，增强了系统的跨平台能力。

- **File I/O**：
  - 提升了对文件I/O的异步处理能力，确保阻塞I/O操作能够高效转换为异步操作。

- **Utility**：
  - 提供了更丰富的工具和功能支持，确保其他模块和组件能够顺利运行。

---

### 5. 综合结论

1. **整体变更优先级**
   - **高优先级**：众多关键性功能的增强和漏洞修复，显著提升了系统的稳定性和安全性。
   - **中优先级**：多项新功能的引入（如 I/O 监控、线程池管理、DNS 处理能力等）提升了模块的灵活性与适应能力。

2. **影响范围**
   - **广泛的跨平台兼容性**：修改和调整对 Windows、Unix 和 macOS 特性的支持，提升了不同操作系统间的一致性和稳定性。
   - **网络和 I/O 性能优化**：通过引入如 `uv_fs_event` 和 `uv_try_write` 等新接口，增强了文件和网络处理的效率。
   - **多线程支持增强**：提升了线程池的管理、控制和性能，使得在高并发环境下的操作更加流畅。

3. **后续行动建议**
   - **测试与监控**：在生产环境中进行全面的测试，特别关注新引入的功能如 UDP 套接字和文件监控的稳定性，确保没有引入新的问题。
   - **文档更新**：更新技术文档，明确新的功能和 API 的用法，为开发者提供清晰的使用指南，减少使用上的疑问。
   - **代码审查和反馈**：鼓励开发者对新功能和变更进行审查和反馈，及时发现潜在的问题并进行修复。
   - **性能评估**：定期进行性能评估，针对关键路径进行性能监控和调优，确保在高负载情况下各模块依然能够保持良好的性能表现。