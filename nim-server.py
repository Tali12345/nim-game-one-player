#!/usr/bin/python3
import socket
import sys
import struct
import errno

def my_sendall(sock, data):
    if(len(data)==0):
        return None
    ret = sock.send(data)
    return my_sendall(sock, data[ret:])


def main(a,b,c,port):
    init_soc_server=False
    init_conn_sock=False
    my_list = [a, b, c]
    try:
        soc_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        init_soc_server=True
        soc_server.bind(('',port))
        soc_server.listen(10)
        while (True):
            init_conn_sock=False
            (conn_sock,address)=soc_server.accept()
            init_conn_sock=True
            conn_sock.recv(struct.calcsize(">iii"))
            game_over=False
            winner="Server"
            while (not game_over):
                my_sendall(conn_sock, struct.pack(">iii", my_list[0],my_list[1],my_list[2]))
                if ((my_list[0]==0)and(my_list[1]==0)and(my_list[2]==0)):
                    if (winner=="You"):
                        my_sendall(conn_sock, struct.pack(">iii", 1,1,1)) #You win!
                        if (init_conn_sock):
                            conn_sock.close()
                        my_list = [a, b, c]
                        break
                    else:
                        my_sendall(conn_sock, struct.pack(">iii", 2,2,2)) #Server win!
                        if (init_conn_sock):
                            conn_sock.close()
                        my_list = [a, b, c]
                        break
                else:
                    my_sendall(conn_sock, struct.pack(">iii", 0,0,0)) #game continue
                rec_bytes=conn_sock.recv(struct.calcsize(">iii"))
                if (rec_bytes==0):
                    if (init_conn_sock):
                        conn_sock.close()
                    break
                rec=struct.unpack(">iii", rec_bytes)
                msg1=rec[0]
                num=rec[1]
                if (msg1==0):
                    if my_list[0]>=int(num):
                        my_sendall(conn_sock, struct.pack(">iii", 1,1,1)) #Move accepted
                        my_list[0]=my_list[0]-int(num)
                    else:
                        my_sendall(conn_sock, struct.pack(">iii", 0,0,0)) #Illegal move
                if (msg1==1):
                    if my_list[1]>=int(num):
                        my_sendall(conn_sock, struct.pack(">iii", 1,1,1)) #Move accepted
                        my_list[1]=my_list[1]-int(num)
                    else:
                        my_sendall(conn_sock, struct.pack(">iii", 0,0,0)) #Illegal move
                if (msg1==2):
                    if my_list[2]>=int(num):
                        my_sendall(conn_sock, struct.pack(">iii", 1,1,1)) #Move accepted
                        my_list[2]=my_list[2]-int(num)
                    else:
                        my_sendall(conn_sock, struct.pack(">iii", 0,0,0)) #Illegal move
                if (msg1==3):
                    my_sendall(conn_sock, struct.pack(">iii", 0,0,0)) #Illegal move
                if (msg1==4):
                    if init_conn_sock:
                        conn_sock.close()
                    my_list = [a, b, c]
                    break
                if ((my_list[0]==0)and(my_list[1]==0)and(my_list[2]==0)):
                    winner="You"
                else:
                    #server turn
                    max_value=max(my_list)
                    for i in range (len(my_list)):
                        if (my_list[i]==max_value):
                            my_list[i]=my_list[i]-1
                            break
    except OSError as error:
        if error.errno == errno.ECONNREFUSED:
            print("connection refused")
        else:
            print(error.strerror)
        if init_conn_sock:
            conn_sock.close()
        if init_soc_server:
            soc_server.close()
    except KeyboardInterrupt:
        if init_conn_sock:
            conn_sock.close()
        if init_soc_server:
            soc_server.close()
        exit(0)
            


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("The program should get 3 numbers")
    else:
        a=int(sys.argv[1])
        b=int(sys.argv[2])
        c=int(sys.argv[3])
        if (len(sys.argv)==4): #no port in the input
            main(a,b,c, 6444)
        if (len(sys.argv)==5):
            if((int(sys.argv[4])<0) or (int(sys.argv[4])>65535)): # a port is a number between 0 to 65535
                print("The port number should be a number between 0 to 65535")
            else:
                main(a,b,c, int(sys.argv[4]))
        else:
            print("Too many parameters")