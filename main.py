import os
from socket import *
from datetime import *
import time


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




# HOST = 'localhost'
# ADDRESS = (HOST, PORT)

# tcpClientSocket = socket(AF_INET, SOCK_STREAM)
# tcpClientSocket.connect(ADDRESS)

