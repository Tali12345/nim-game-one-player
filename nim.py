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

def main(ip,port):
    init_soc_client=False
    try:
        soc_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        init_soc_client=True
        soc_client.connect((ip, port))
        my_sendall(soc_client, struct.pack(">iii", 0,0,0))
        game_over=False
        while (not game_over):
            abc_bytes=soc_client.recv(struct.calcsize(">iii"))
            if (abc_bytes==0):
                print("Disconnected from server")
                if init_soc_client:
                    soc_client.close()
                break
            abc = struct.unpack(">iii", abc_bytes)
            print ("Heap A:", abc[0])
            print ("Heap B:", abc[1])
            print ("Heap C:", abc[2])
            data_rec_0_1_2_bytes=soc_client.recv(struct.calcsize(">iii"))
            if (data_rec_0_1_2_bytes==0):
                print("Disconnected from server")
                if init_soc_client:
                    soc_client.close()
                break
            data_rec_0_1_2=struct.unpack(">iii", data_rec_0_1_2_bytes)[0]
            if data_rec_0_1_2==1 or data_rec_0_1_2==2:
                if data_rec_0_1_2==1:
                    print("You win!")
                    if init_soc_client:
                        soc_client.close()
                    break
                else:
                    print("Server win!")
                    if init_soc_client:
                        soc_client.close()
                    break
            else:
                print("Your turn:")
                val = input("")
                val=val.split()
                if (val[0]=="Q"):
                    my_sendall(soc_client, struct.pack(">iii", 4,4,4)) # Q
                    if init_soc_client:
                        soc_client.close()
                    break
                if (len(val)!=2):
                    my_sendall(soc_client, struct.pack(">iii", 3,3,3)) #Illegal move
                else:
                    if ((val[0]!="A")and(val[0]!="B")and(val[0]!="C")and(val[0]!="Q")):
                        my_sendall(soc_client, struct.pack(">iii", 3,3,3)) #Illegal move
                    if val[0]=="A":
                        if ((val[1].isdigit()) and (int(val[1])<=1000) and (int(val[1])>=1)):
                            my_sendall(soc_client, struct.pack(">iii", 0,int(val[1]),0))
                        else:
                            my_sendall(soc_client, struct.pack(">iii", 3,3,3)) #Illegal move
                    if val[0]=="B":
                        if ((val[1].isdigit()) and (int(val[1])<=1000) and (int(val[1])>=1)):
                            my_sendall(soc_client, struct.pack(">iii", 1,int(val[1]),0))
                        else:
                            my_sendall(soc_client, struct.pack(">iii", 3,3,3)) #Illegal move
                    if val[0]=="C":
                        if ((val[1].isdigit()) and (int(val[1])<=1000) and (int(val[1])>=1)):
                            my_sendall(soc_client, struct.pack(">iii", 2,int(val[1]),0))
                        else:
                            my_sendall(soc_client, struct.pack(">iii", 3,3,3)) #Illegal move
                data_rec_bytes=soc_client.recv(struct.calcsize(">iii"))
                if (data_rec_bytes==0):
                    print("Disconnected from server")
                    if init_soc_client:
                        soc_client.close()
                    break
                data_rec=struct.unpack(">iii", data_rec_bytes)[0]
                if (data_rec==0):
                    print("Illegal move")
                else:
                    print("Move accepted")
    except OSError as error:
        if error.errno == errno.ECONNREFUSED:
            print("Disconnected from server")
        else:
            print(error.strerror)
        if init_soc_client:
            soc_client.close()  
    except KeyboardInterrupt:
        if init_soc_client:
            soc_client.close()
        exit(0)


if __name__ == "__main__":
    if (len(sys.argv) == 1): # no parameters
        main("localhost",6444)
    else:
        if (len(sys.argv) ==2): # 1 parameters
            main(sys.argv[1],6444)
        else:
            if (len(sys.argv) ==3): # 2 parameters
                if((int(sys.argv[2])<0) or (int(sys.argv[2])>65535)): # a port is a number between 0 to 65535
                    print("The port number should be a number between 0 to 65535")
                else:
                    main(sys.argv[1],int(sys.argv[2]))
            else:
                print("Too many parameters")