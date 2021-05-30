import socket
import base64
import hashlib
import time
import sys
import random
from CustomExceptions import *

def CreateTcpSocket(ip_addr_dest, port_addr_dest):
    try:
        tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_socket.connect((ip_addr_dest, int(port_addr_dest)))
        return tcp_socket
    except socket.error as err:
        print("La creación del socket tcp ha fallado: %s" % (err))

def CreateUdpSocket(ip_addr_sourc):
    try:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_port = random.randint(49152, 65535)
        udp_socket.bind((ip_addr_sourc, udp_port))
        return udp_socket, udp_port
    except socket.error as err:
        print("La creación del socket udp ha fallado: %s" % (err))

def CheckUsername(tcp_socket, username):
    helloiam = "helloiam " + username
    tcp_socket.send(helloiam.encode())
    response = tcp_socket.recv(1024)
    return response.decode()

def CheckLength(tcp_socket):
    tcp_socket.send('msglen'.encode())
    response = tcp_socket.recv(1024)
    return response.decode()

def CheckSum(tcp_socket, msg_md5):
    msg_hex = "chkmsg "+msg_md5.hexdigest()
    tcp_socket.send(msg_hex.encode())
    respuesta = tcp_socket.recv(1024)
    return respuesta.decode()

def ConfirmBye(tcp_socket):
    tcp_socket.send('bye'.encode())
    bye_res = tcp_socket.recv(1024)
    return bye_res.decode()

def GetMsg(tcp_socket, udp_port):
    givememsg =  "givememsg " + str(udp_port)
    tcp_socket.send(givememsg.encode())
    response = tcp_socket.recv(1024)
    return response.decode()

def GetMsgUdp(udp_socket):
    started_time = time.time()
    while True:
        elapsed_time = time.time() - started_time
        udp_socket.settimeout(10)
        msg = udp_socket.recv(12000)
        if(msg):
            return msg
        if(int(elapsed_time) >= 10):
            raise TimeoutException(int(elapsed_time))

if __name__ == "__main__":

    try:
        tcp_socket = CreateTcpSocket(sys.argv[1], sys.argv[2])
        udp_socket, udp_port = CreateUdpSocket(sys.argv[3])
        if not tcp_socket:
            raise SocketException()
        if not udp_socket:
            raise SocketException()
        username = sys.argv[4]
        
        helloiam_resp = CheckUsername(tcp_socket, username).split()[0]
        if(helloiam_resp == "error"):
            raise UsernameException(username)

        msglen_resp = CheckLength(tcp_socket).split()[0]
        if(msglen_resp == "error"):
            raise LengthException()
        
        givememsg_resp = GetMsg(tcp_socket, udp_port).split()[0]
        if(givememsg_resp == "error"):
            raise UdpException(udp_port)

        msg = GetMsgUdp(udp_socket)
        if(msg):
            msg_b64 = str(base64.b64decode(msg).decode())
            msg_md5 = hashlib.md5(msg_b64.encode())
            chkmsg_resp = CheckSum(tcp_socket, msg_md5).split()[0]
            if(chkmsg_resp == "ok"):
                print("\nEl mensaje para " + username + " es: \n\n" + msg_b64)
                bye_resp = ConfirmBye(tcp_socket).split()[0]
                if(bye_resp == "ok"):
                    tcp_socket.close()
                    udp_socket.close()
            else:
                raise BadChecksumException()

    except UsernameException as e:
        print(e.message + e.username)
    except LengthException as e:
        print(e.message)
    except UdpException as e:
        print(e.message + str(e.udp_port))
    except TimeoutException as e:
        print(e.message + str(e.elapsed_time) + " seg")
    except BadChecksumException as e:
        print(e.message)
    except SocketException as e:
        print(e.message)

        
