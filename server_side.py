#Python Socket Server
#Author: Marvin Johnson
#Created: 2020-02-29
#Description: Server will listen on designated port for message being pushed
#from client. Once message is recieved server program will reply with predetermined
#reply and close session. To esnure secure connection/trusted connection
#the server will publish it cert info to the CA Authority DB through a CA Server application.
#Simple encryption and decryption for secure communication is utilized for communication after
#trust is established. 

import socket
import sys
import CA_Server
import encryption

Hostname = "Homebase"
Public_Key = "1234pass"

#Create entry in CA database for this server
CA_Server.addCAInfo(Hostname,Public_Key)

#Initialize open socket for communication with client devices
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9500
s.bind(('0.0.0.0', port))
print ('Socket binded to port 9500')
s.listen(3)
print ('Socket is listening')

while True:
    #Send client server name necessary to verify against CA Authority
    clientConnection, addr = s.accept()
    print ('Connection made')
    hostname = "Homebase"
    clientConnection.sendall(hostname.encode())

    #Recieves encrypted response from client once Certificate is verified through session key reciept
    msg =  clientConnection.recv(1024)
    cipher = encryption.AESCipher(Public_Key)
    decryptedMsg = cipher.decrypt(msg)
    data = decryptedMsg.decode("utf-8")
    print('Message recieved:', data)
    if data == "session key":
        reply = "key acknowledged"
        encryptedRply = cipher.encrypt(reply)
        clientConnection.sendall(encryptedRply)
        print('Reply Sent:', reply)
    else:
        clientConnection.close()

    #Trust established, server sends encrypted response to client depending on reponse decrypted message from client
    msg2 =  clientConnection.recv(1024)
    decryptedMsg = cipher.decrypt(msg2)
    data2 = decryptedMsg.decode("utf-8")
    print('Message recieved:', data2)
    if data2 == 'Hello':
        reply2 = 'Hi'
        encryptedRply2 = cipher.encrypt(reply2)
        clientConnection.sendall(encryptedRply2)
        print('Reply Sent:', reply2)
        break
    else:
        reply2 = 'Goodbye'
        encryptedRply2 = cipher.encrypt(reply2)
        clientConnection.sendall(encryptedRply2)
        print('Reply Sent:', reply2)
        break

clientConnection.close()
                          