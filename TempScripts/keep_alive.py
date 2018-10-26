import socket

class CommandCenter():
    def __init__(self):
        self.UDP_IP = "172.16.10.1" # TODO: read these values from config file
        self.UDP_PORT = 8080
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP

    def __send_to_drone(self,up_down, rotate, foward_backwards, left_right, byte6, byte7, byte8, byte9):
        command = bytearray([255, 8, up_down, rotate, foward_backwards, left_right, byte6, byte7, byte8, byte9])
        command.extend([255 - sum(command[1:]) % 256])  # check sum
        self.sock.sendto(command, (self.UDP_IP, self.UDP_PORT))

    def keep_alive(self):
        self.__send_to_drone(0, 63, 64, 63, 144, 16, 16, 0)  # stand by