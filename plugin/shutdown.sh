#!/bin/bash

# 删除运行在端口8000上的程序
# 1. 获取运行在端口8000上的程序的pid
pid=$(lsof -t -i:8000)

# 2. 如果pid存在，则杀死该进程
if [ -n "$pid" ]; then
    kill -9 $pid
    echo "已删除运行在端口8000上的程序，PID: $pid"
else
    echo "没有程序运行在端口8000上"
fi