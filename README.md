# MIN-security-system

MIN的安全感知系统：主要分为两个部分，1，基于网络的入侵检测系统；2，基于主机的入侵检测系统。
(程序依赖：mongodb，其余依赖库脚本会自行安装，使用python2进行实现)

##  基于网络的入侵检测系统：
   该系统可以检测所有的NDN数据包，从而进行解码，提取出关键信息，进行恶意行为判断，与流量监控等等。实现过程仿照IP体系中常用的snort入侵检测工具，主要有以下模式：监听模式，监测模式，封包记录模式。
   
*    监听模式为监听所有NDN数据包；
   
*    监测模式是开启流量检测功能，进行恶意流量检测；
   
*    封包记录模式是将捕获的数据包保存记录在pcap包中。
   
   程序入口在net_message.py，检测过程中的日志储存在当前log目录中。
   使用方式（可通过-h查询）：
   
```minuser@ubuntu:~/xin777$ ./net_message.py -h

WARNING: No route found for IPv6 destination :: (no default route?)
usage: net_message.py [-h] [-p PORT] [-i INTERFACE] [-s] [-v] [-t] [-d] [-sp]

optional arguments:
  -h, --help            show this help message and exit
  
  -p PORT, --port PORT  port, -1 means to listen all ports
  -i INTERFACE, --interface INTERFACE
                        choose interface to capture data, 'any' means all
                        interface
  -s, --strong          strong mode, analyze every packet, deny the dangerous
                        data.
  -v, --view            open the view mode, view the packet message
  -t, --time            add the time to every packet in the controller
  -d, --detail          view the detailed packet message
  -sp, --save_packet    save the packet message to pcap file
  ```
  
  对于
  数据库的读取，也封装好了接口，在mongodb.py文件中，同样可以运行./mongodb.py -h来查看使用说明：
  
  ```
  ./mongodb.py -h
only display at most 20 messages if limit param is set
usage: m
ongod
b.py [-h] [-f] [-g] [-a] [-us] [-c] [-o ORDER] [-m MINUTES]
                  [-l LIMIT] [-u USERNAME] [-d DAYS] [-e DEMAND]

optional arguments:
  -h, --help            show this help message and exit
  -f, --find            find under demands, need -e,-l
  -g, --get_frequency   view the user's frequency, need -u, -m, -d, -l
  -a, --all             get all messages, need -o, -l
  -us, --users          get all users
  -c, --count           the count of the whole db
  -o ORDER, --order ORDER
                        the order of results
  -m MINUTES, --minutes MINUTES
                        minutes ago -> now set
  -l LIMIT, --limit LIMIT
                        limit the displayed count
  -u USERNAME, --username USERNAME
                        set username
  -d DAYS, --days DAYS  days ago -> now
  -e DEMAND, --demand DEMAND
                        search conditions
  ```                    
                        
    Filter模块中包含了恶意流量检测的规则，若有需要，可以自行更改。
   
   