import socket
import os
from phue import Bridge

def open_server_socket(IP):
    s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_socket.bind((IP.ipaddress, IP.port))
    s_socket.listen()
    print("server open...")
    return s_socket

def parsing_controller(data):
    light_num = 0
    if 'B1=' in data :
        light_num = 1
    elif 'B2=' in data :
        light_num = 2
    elif 'B3=' in data :
        light_num = 3
    else: 
        return

    datalist = data.split("&")

    power = datalist[0][datalist[0].index('=')+1:]
    brightness = datalist[1][datalist[1].index('=')+1:]
    x = datalist[2][datalist[2].index('=')+1:]
    y = datalist[3][datalist[3].index('=')+1:]

    bridge = Bridge('192.168.0.4')
    bridge.connect()

    lights = bridge.lights
    print("complete")
    power_control(light_num, power, lights)
    brightness_control(light_num, brightness, lights)
    color_control(light_num, x, y, lights)


def power_control(bulb_num, power, lights):
    try:
        if power == "on":
            lights[int(bulb_num)-1].on=True
        else:
            lights[int(bulb_num)-1].on=False

    except Exception as e:
        print("error occur with", e)

def brightness_control(bulb_num, brightness, lights):
    try:
        lights[int(bulb_num)-1].brightness = int(brightness)
    except Exception as e:
        print("error occur with", e)

def color_control(bulb_num, x, y, lights):
    try:
        lights[int(bulb_num)-1].xy = [float(x), float(y)]
    except Exception as e:
        print("error occur with", e)


def accept_client(s_socket):
    
    while True:
        client, addr = s_socket.accept()
        print("accept client from", addr)

        data = client.recv(1024).decode('utf-8')
        data_msg = data.split()
        filedir = '.'+data_msg[1]

        if filedir[-1] == '/' :
            filedir = filedir[0:len(filedir)-1]

        f = open(filedir, "r")
        print(data_msg[0]+" "+data_msg[1]+" "+data_msg[2])

        if data_msg[0] == 'POST' :
            parsing_controller(data.split("\n")[-1])


        header = "HTTP/1.1 200 OK\r\n\n"

        htmlData = f.read()
        htmlData = header+htmlData

        client.sendall(htmlData.encode('utf-8'))
        client.close()          
        f.close()

    print("server close...")

def main(FLAGS):
    server_socket = open_server_socket(FLAGS)
    accept_client(server_socket)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ipaddress', type=str, default='172.17.0.2')
    parser.add_argument('-p', '--port', type=int, default=8000)
    FLAGS, _ = parser.parse_known_args()
    main(FLAGS)
