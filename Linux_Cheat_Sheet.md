
# Linux Troubleshooting

The list of commands that we can use to troubleshoot performance issues in Linux.

1. `uptime` --> used to check Load averages
2. `dmesg -T | tail` --> used to check for Kernel Errors and Kernel messages
3. `vmstat 1` --> Overall stats by time
4. `mpstat -P ALL 1` --> CPU Balance and mp means multiprocessors statistics.
5. `pidstat 1` --> this is very useful to find out all the relevant processes that consuming CPU at large
6. `iostat -xz 1` --> Extended disk i/o processes.
7. `free -m` --> Tells you the free memory available
8. `du -sh` --> Tells you the free disk usage available
9. `df -sh` --> Tells you the file sizes -h: it is human readable -s: it is summary.
10. `sar -n DEV 1` --> System Activity Report, we can use this for network I/o
11. `sar -n TCP, ETCP 1` --> TCP stats
12. `top` --> Check overview
13. `atop` --> top can miss a few short-lived processes but atop will NOT.
14. `htop` --> will give a complete CPU utilization in a horizontal bar graph and looks neat.

#### Scenario's

1. ### Problem: The latency of the application had been increased

Latency means `delay`

#### Step 1 --> As there is a delay in the application, we can approach it from a CPU perspective. So, we can start with `top` command to understand
how the CPU load averages and it is performance. If it seems convincing and the Load Averages are well below or fine, then we can go ahead with
the next hypothesis. 

```
Load Averages should be below the number of CPU processors/core which means it is working fine. For example, if we have 1 core CPU, then the
maximum allowable Load could be 1.0 but if the load average is greater than 1, and by correlating the runnable tasks in the queue, we can know that the 
CPU is getting hammered and there will be a bottleneck.
```

There are two parameters to consider when looking for Load Averages,
1. `Runnable Tasks` --> Tasks waiting for the prior I/O operations to get completed i.e. it is waiting in the queue.
2. `Task uninterruptible` --> These tasks are TASK_UNINTERRUPTIBLE for example, process waiting for disk I/O operation.

#### Step 2 -> Run `vmstat 1` because you can find the runnable tasks using the vmstat command.
Example below,

procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----
 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st
 0  0      0  96240  22900 373952    0    0  4450    53  189  423  3  8 88  1  1
 0  0      0  96240  22900 373952    0    0     0     0   44   69  0  0 100  0  0
 0  0      0  96240  22900 373952    0    0     0     0   48   86  0  0 100  0  0
 0  0      0  96240  22900 373948    0    0     0   152   90  187  0  0 100  0  0
 0  0      0  96240  22900 373948    0    0     0     0   45   89  0  0 100  0  0
 0  0      0  96240  22900 373948    0    0     0     0   46   85  0  0 100  0  0

 If you take a look at the above example, we could see that the total buffer size, free memory, cache memory, 
 blocks received from the memory to the disk i.e. bi and the blocks sent from the memory to the disk is bo.

 Under System,
 system interrupts -> in -> Number of interrupts per second
 context switches -> cs -> context switches per second

 then,
 usertime -> us -> Time taken by the CPU to work on coded programs.
 system time -> sy -> Time taken by the CPU to work on kernel programs.
 idle time -> id -> Waiting by the CPU for receiving tasks or NOT receiving any tasks.

 wa -> Total amount of CPU time spent waiting for an I/O operation to occur.

 st - Steal time, it is the time when the virtual CPU waits for a real CPU while it is working on an other process.
 When the idle time percentage is 0 and the value of steal time shows a higher level over a longer period of time, 
 it is safe to assume processes on the virtual machine are processed with some delay.

 There are three reasons when the steal time can be higher,
 1. When we got a smaller core size like for example, I'm running the entire application in under 1 core process let's say, less than 2GHZ processor.
 2. When the cloud or physical servers are overloaded with processes. And, the VMs are fighting for resources.

 If everything is fine in step 2, then you can move to step 3 and again it checks the CPU utilization based on the cores.

Step 3 -> use mpstat -P ALL 1 5, this command will show the CPU list and it's usertime percentage.
Example OP:
17:49:25     CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle
17:49:26     all    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00  100.00
17:49:26       0    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00  100.00

Step 4 -> iostat -xh -> It is a tool to understand how the disks are running.
Example OP:
avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           1.0%    0.1%    2.7%    0.2%    0.3%   95.6%

r/s     rkB/s   rrqm/s  %rrqm r_await rareq-sz Device
    0.02      0.1k     0.00   0.0%    0.78     8.4k loop0
    0.84     41.4k     0.00   0.0%    1.51    49.1k loop1
    0.02      0.1k     0.00   0.0%    0.61     7.3k loop10
    0.02      0.4k     0.00   0.0%    0.71    17.1k loop11
    0.02      0.4k     0.00   0.0%    1.06    17.3k loop12
    0.03      0.4k     0.00   0.0%    0.56    16.9k loop13
    0.02      0.1k     0.00   0.0%    0.46     8.4k loop14
    0.03      0.6k     0.00   0.0%    0.55    19.2k loop15
    0.00      0.0k     0.00   0.0%    0.00     1.0k loop16
    0.01      0.0k     0.00   0.0%    0.21     1.2k loop2
    0.03      0.4k     0.00   0.0%    0.85    16.4k loop3
    0.02      0.1k     0.00   0.0%    0.68     8.4k loop4
    0.25      3.2k     0.00   0.0%    1.08    12.8k loop5
    0.02      0.1k     0.00   0.0%    0.40     8.0k loop6
    0.10      0.9k     0.00   0.0%    0.51     8.7k loop7
    3.67    191.0k     0.00   0.0%    0.46    52.1k loop8
    0.02      0.4k     0.00   0.0%    1.16    17.1k loop9
   35.26      1.3M     5.40  13.3%    1.00    36.9k xvda

NOTE: loopX -> these are pseudo-devices i.e. it is a plain filesystem that can be used as a block device without any repartitioning the disks.
This can help you to store images. 

INFERENCE from Disk -> If you see high utilization in the Disk, then the latency is because of the disk I/O operations.

Finally, just to confirm are there any latency in the network,
we can run network stats using sar
Step 5 -> sar -n DEV 1
Example OP:
18:06:08        IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s   rxcmp/s   txcmp/s  rxmcst/s   %ifutil
18:06:09           lo      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00
18:06:09         eth0      4.00      1.00      0.19      0.04      0.00      0.00      0.00      0.00
18:06:09      docker0      0.00      0.00      0.00      0.00      0.00      0.00      0.00      0.00

there is no utilization so there is NO issues with Network.

So, Latency of the application can be from the Disks.


Scenario's,

2. The application is taking forever

Step 1 -> start with top - This gives you the overview immediately.
Step 2 -> vmstat 1 - This gives you the swap memory usage.
Step 3 -> pidstat 1 - This gives you the process that is consuming the maximum memory or CPU.
Step 4 -> strace -tp `pgrep <process_name>` | head -100 -> taking only the top 100. this will output what it is the process doing.

Step 5 -> If needed, we can kill the process. kill <PID>

Scenario's,

3. Something mysterious is consuming the CPU.

We can follow the same troubleshooting steps as before,

Step 1 -> start with top - This gives you the overview immediately.
Step 2 -> vmstat 1 - This gives you the swap memory usage.
Step 3 -> pidstat 1 - This gives you the process that is consuming the maximum memory or CPU.
Step 4 -> strace -tp `pgrep <process_name>` | head -100 -> taking only the top 100. this will output what it is the process doing.

Step 5 -> If needed, we can kill the process. kill <PID>

BUT, if we were unable to find the process, then we can use a command called, perf record -> It is used to count both the hardware and the software events 
in the kernel and the system. To keep it simple, it collects data as a whole and DO NOT miss even the short-lived processes.

Step 6 -> perf record, let's record the events for a while like 10 seconds. Then, we can use "perf report -n --stdio" to display the data that it collected.

Example OP:
To display the perf.data header info, please use --header/--header-only options.
#
#
# Total Lost Samples: 0
#
# Samples: 53K of event 'cpu-clock:pppH'
# Event count (approx.): 13307250000
#
# Overhead       Samples  Command          Shared Object            Symbol
# ........  ............  ...............  .......................  ............................
#
     7.95%          4234  while.sh         libc.so.6                [.] malloc
     5.55%          2952  while.sh         bash                     [.] discard_unwind_frame
     4.96%          2639  while.sh         bash                     [.] hash_search
     4.84%          2576  while.sh         libc.so.6                [.] cfree
     3.77%          2006  while.sh         bash                     [.] builtin_address_internal
     3.57%          1901  while.sh         bash                     [.] execute_command_internal
     2.46%          1310  while.sh         libc.so.6                [.] _IO_fflush
     1.90%          1013  while.sh         bash                     [.] unquoted_glob_pattern_p
     1.87%           995  while.sh         libc.so.6                [.] 0x0000000000198afe
     1.76%           939  while.sh         libc.so.6                [.] 0x000000000019d981
     1.34%           714  while.sh         bash                     [.] begin_unwind_frame
     1.21%           643  while.sh         bash                     [.] dispose_words
     1.12%           595  while.sh         bash                     [.] execute_command
     1.08%           573  while.sh         libc.so.6                [.] 0x0000000000198af2
     0.88%           471  while.sh         bash                     [.] run_pending_traps
     0.83%           444  while.sh         bash                     [.] copy_word_list
     0.83%           441  while.sh         bash                     [.] make_bare_word
     0.81%           432  while.sh         libc.so.6                [.] 0x000000000019d985
     0.75%           401  while.sh         libc.so.6                [.] 0x00000000000a27bf
     0.75%           397  while.sh         libc.so.6                [.] 0x000000000019d375
     0.73%           389  while.sh         libc.so.6                [.] 0x0000000000198b04
     0.73%           386  while.sh         bash                     [.] dequote_string
     0.71%           379  while.sh         bash                     [.] do_redirections
     0.69%           365  while.sh         libc.so.6                [.] 0x000000000019d98d
     0.68%           361  while.sh         libc.so.6                [.] 0x00000000000a2a80
     0.63%           334  while.sh         libc.so.6                [.] 0x0000000000198afa
     0.62%           329  while.sh         libc.so.6                [.] 0x00000000000a2720
     0.59%           314  while.sh         bash                     [.] set_pipestatus_array
     0.56%           299  while.sh         bash                     [.] make_word_list
     0.55%           293  while.sh         libc.so.6                [.] 0x00000000000a273e
     0.54%           286  while.sh         bash                     [.] alloc_word_desc
     0.52%           278  while.sh         bash                     [.] bind_variable
     0.50%           264  while.sh         libc.so.6                [.] 0x000000000019d328

NOTE:  We can use atop or htop to check the short-lived processes.





