# 简介

本文主要对[Ellisys - USB, Bluetooth and WiFi Protocol Test Solutions](https://www.ellisys.com/index.php)的**Injection**机制进行说明和python实现（官方提供的C#实现已经很好了）。

仓库源码为：[bobwenstudy/bt_ellisys_injection (github.com)](https://github.com/bobwenstudy/bt_ellisys_injection)

## Ellisys介绍

ellisys是目前我用过蓝牙抓包软件体验最舒服的了，尤其是其Timing窗口，操作体验很好，比Frontline体验好很多。同时其抓包的操作体验也是傻瓜式，很舒服，虽然抓包可靠性有些坑，时不时会有丢包，但是不影响分析问题。

还好公司有购买Ellisys的产品，所以这边有其安装包。东西太大了，就不传到Github上了，需要的私聊。

![image-20240105135846657](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105135846657.png)

**注意**：这里要吐槽下，蓝牙的两个方案商提供安装包都必须要联系他们厂商，而不是直接提供下载，理论上都是买设备的产商，软件有什么好限制下载的，不如好好学学Jlink这些。

## Ellisys Injection

直接进Help，看user Manu。

简单直接，就是TCP和UDP接口，Ellisys开了2个service，分别是Injected User Log Service和HCI Injection Service。这里重点看HCI Injection Service。

![image-20240105140107217](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105140107217.png)

User Manual只提供了基本说明，协议和例程需要看[bex400a_injection_api.zip](http://www.ellisys.com/better_analysis/bex400a_injection_api.zip)，仓库里面给大家下载好了。

User Manual还写了需要在Tools中打开Injection Service。

![image-20240105135459961](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105135459961.png)

然后选择Injection API启动Record就可以了。

![image-20240105140529624](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105140529624.png)



# 协议说明

直接看[bex400a_injection_api.zip](http://www.ellisys.com/better_analysis/bex400a_injection_api.zip)，里面一个是讲协议的2个pdf文档。

一个是C#的Sample实现。

![image-20240105140917160](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105140917160.png)

## TCP/UDP接口

IP地址就是运行Ellisys软件的PC的地址，如果Client和Service在一台电脑，用`127.0.0.1`就可以。端口号看你配置的是什么，如果没改的话，就是`24352`。



## TCP/UDP帧格式

### Target Service Object

TCP只要第一笔包发送一次，UDP每笔包都需要发送。

![image-20240105142043102](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105142043102.png)

3个字节由2个字节的Service ID和1个字节的Service Version组成。 

![image-20240105142316024](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105142316024.png)

目前支持下面2中Service ID：

| Name                      | ID     | Version |
| ------------------------- | ------ | ------- |
| Injected User Log Service | 0x0001 | 0x01    |
| HCI Injection Service     | 0x0002 | 0x01    |
|                           |        |         |

![image-20240105145054712](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105145054712.png)



### 基本帧格式

基本的包格式就是`Object ID(1 octet)+Object Data(N octets)`，比较简单。

Object Data内容的意义由Object ID决定。

![image-20240105141332842](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105141332842.png)

目前从文档看到的Object ID包括：

| Name                        | Object ID | 备注 |
| --------------------------- | --------- | ---- |
| DateTimeMs Object           | 0x01      |      |
| DateTimeNs Object           | 0x02      |      |
| GroupStart Object           | 0x04      |      |
| GroupEnd Object             | 0x05      |      |
| Text Object                 | 0x06      |      |
| Severity Object             | 0x80      |      |
| Bitrate Object              | 0x80      |      |
| HCI Packet Type Object      | 0x81      |      |
| HCI Packet Data Object      | 0x82      |      |
| HCI Controller Index Object | 0x83      |      |
|                             |           |      |



### DateTimeMs Object (0x01)

![image-20240105151935798](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105151935798.png)

### DateTimeNs Object (0x02)

![image-20240105152013710](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105152013710.png)

### GroupStart Object (0x04)

![image-20240105152125403](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105152125403.png)

![image-20240105152135691](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105152135691.png)



### GroupEnd Object (0x05)

![image-20240105152157781](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105152157781.png)



### Text Object (0x06)

![image-20240105152213633](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105152213633.png)



### Severity Object (0x80)

![image-20240105152447625](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105152447625.png)



### Bitrate Object (0x80)

![image-20240105153559756](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105153559756.png)



### HCI Packet Type Object (0x81)

![image-20240105153623591](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105153623591.png)

![image-20240105153645739](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105153645739.png)

### HCI Packet Data Object (0x82)

![image-20240105153714205](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105153714205.png)



### HCI Controller Index Object (Optional) (0x83)

![image-20240105153758831](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105153758831.png)



## Message Packet Container (TCP)

TCP包发送时需要在外面在包一层，`Message Packet`就是`Target Service Object+Objects(n)`。

其格式如下，3个字节的length，1个字节的hash和n(n=length)个字节的Payload。

![image-20240105141701811](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105141701811.png)



## Injection Service

目前Ellisys文档只提供了2种Service，但是软件里面看有4个，这里只对文档描述的进行说明。

### Injected User Log Service

一个UDP示例如下，其实可以看到就是`Target Service Object+DateTimeMs Object (0x01)+Text Object (0x06)+Text Object (0x06)`组成。

![image-20240105152823528](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105152823528.png)



### HCI Injection Service

HCI Injection Service的包帧格式更为严格，不像Log可以出现多个String。

其格式如下，其中HCI Controller Index Object (Optional) 是可选的。

![image-20240105153055591](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105153055591.png)

一个示例如下：

![image-20240105161659050](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105161659050.png)



# Python实现

Sample里面已经有C#实现了，python有的人多，争取几行代码搞定。

## 基本参数

准备几个HCI数据包，`generate_ellisys_packet`用于构建Ellisys所需的数据包。

```python

def generate_ellisys_packet(packet_type, data):
    send_data = b''
    ## WriteServiceId
    # HciInjectionServiceId
    send_data += ((0x0002).to_bytes(length=2, byteorder='little', signed=False))
    # HciInjectionServiceVersion
    send_data += (0x01).to_bytes()


    ## WriteDateTimeNs
    dt = datetime.now()
    dt_day = datetime(dt.year, dt.month, dt.day)
    timestamp_ns = (dt.timestamp() - dt_day.timestamp()) * 1000000000

    send_data += (0x02).to_bytes()
    send_data += ((dt.year).to_bytes(length=2, byteorder='little', signed=False))
    send_data += (dt.month).to_bytes()
    send_data += (dt.day).to_bytes()
    send_data += (int(timestamp_ns).to_bytes(length=6, byteorder='little', signed=False))


    ## WriteBitrate
    # Bitrate
    send_data += (0x80).to_bytes()
    send_data += ((12000000).to_bytes(length=4, byteorder='little', signed=False)) # 12 Mbit/s (USB Full Speed)
    
    ## WriteHciData
    # HciPacketType
    send_data += (0x81).to_bytes()
    send_data += (packet_type).to_bytes()

    # HciPacketData
    send_data += (0x82).to_bytes()
    send_data += (data)

    return send_data

InjectedHciPacketType_Command				= 0x01
InjectedHciPacketType_AclFromHost			= 0x02
InjectedHciPacketType_AclFromController		= 0x82
InjectedHciPacketType_ScoFromHost			= 0x03
InjectedHciPacketType_ScoFromController		= 0x83
InjectedHciPacketType_Event					= 0x84

# HCI Read_BD_ADDR
# Simulate the sending of an HCI Read_BD_ADDR command to a Bluetooth Device.
sampleFrame_cmd = bytes.fromhex("09 10 00")
# Command Complete Event
# Simulate the response from a Bluetooth Device to an HCI Read_BD_ADDR command.
sampleFrame_event = bytes.fromhex("0e 0a 01 09 10 00 82 14 01 5b 02 00")
# Connection Complete Event
# Simulate a Connection Complete reponse from a Bluetooth Device for an ACL connection. (This establishes the connection handle for the next two buttons.)
sampleFrame_event1 = bytes.fromhex("03 0b 00 28 00 2d 18 00 5b 08 00 01 00")
# Send ACL Data
# Simulate sending ACL data from a Host to a remote Bluetooth Device.
sampleFrame_acl_send = bytes.fromhex("28 20 1c 00 18 00 40 00 4d 65 73 73 61 67 65 20 74 6f 20 72 65 6d 6f 74 65 20 64 65 76 69 63 65")
# Receive ACL Data
# Simulate receiving ACL data from a remote Bluetooth Device.
sampleFrame_acl_recv = bytes.fromhex("28 20 1e 00 1a 00 40 00 4d 65 73 73 61 67 65 20 66 72 6f 6d 20 72 65 6d 6f 74 65 20 64 65 76 69 63 65")

```



## UDP发送示例

直接调用UDP发送接口，发送数据给Ellisys。

```python
HOST = '127.0.0.1'
PORT = 24352
BUFSIZ = 1024
ADDRESS = (HOST, PORT)

udpClientSocket = socket(AF_INET, SOCK_DGRAM)

udpClientSocket.sendto(generate_ellisys_packet(InjectedHciPacketType_Command, sampleFrame_cmd), ADDRESS)
time.sleep(0.001)
udpClientSocket.sendto(generate_ellisys_packet(InjectedHciPacketType_Event, sampleFrame_event), ADDRESS)
time.sleep(0.001)
udpClientSocket.sendto(generate_ellisys_packet(InjectedHciPacketType_Event, sampleFrame_event1), ADDRESS)
time.sleep(0.001)
udpClientSocket.sendto(generate_ellisys_packet(InjectedHciPacketType_AclFromHost, sampleFrame_acl_send), ADDRESS)
time.sleep(0.001)
udpClientSocket.sendto(generate_ellisys_packet(InjectedHciPacketType_AclFromController, sampleFrame_acl_recv), ADDRESS)
time.sleep(0.001)

udpClientSocket.close()
```

直接运行`python main.py`，就可以看到Ellisys收到了这5笔数据包。

![image-20240105171857067](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105171857067.png)





## TCP发送示例

尝试用TCP去连接，一直无法成功，而且sample里面也没有TCP的示例，UDP能用就算了。

![image-20240105173246045](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105173246045.png)

而且看了下之前的配置参数，上面也只有UDP Port配置，可能TCP不支持吧，暂时不研究了。

![image-20240105173845949](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20240105173845949.png)
