#Python Socket Client
#Author: Marvin Johnson
#Created: 2020-02-29
#Description: Program garners input from user and sends message to server
#through socket connection. Client will recieve a reply from server and
#print to screen. Client will verify Trust through CA auth check of server
#broadcasted hostname. If public key is recieved from CA server (db), server
#will use it to send a session key to server to connection validation

import socket
import CA_Server
import encryption

#Initiate socket connection with Application Server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 9500
s.connect(('localhost', port))

#Recieves broadcasted server name for Certificate Authority Validation
replyMsg = s.recv(1024)
data = replyMsg.decode("utf-8")
print('Reply received:', data)

#Queries CA Database for recieved hostname and recieves public_key for 
#encryption if hostname exists
pKey = CA_Server.checkCAInfo(data)
print(pKey[0])

#uses key to encrypt a session key to send to application server once trust has 
# been established
cipher = encryption.AESCipher(pKey[0])
sessionKey = 'session key'
encryptedMsg = cipher.encrypt(sessionKey)
s.sendall(encryptedMsg)

#Client recieves acknoledgement from Server once sesion key is recieved
replyMsg2 = s.recv(1024)
decryptedRply = cipher.decrypt(replyMsg2)
reply = decryptedRply.decode("utf-8")
print("Reply Recieved: ",reply)

#If session key acknowledgement is recieved by client, client processes secure
#data to be recieved by server and awaits secure reply
if reply == "key acknowledged":
    myMessage = input('Input: ')
    encryptedMsg = cipher.encrypt(myMessage)
    s.sendall(encryptedMsg)
else:
    badReply = "Goodbye"
    encryptedMsg = cipher.encrypt(badReply)
    s.sendall(encryptedMsg)
    s.close()


replyMsg2 = s.recv(1024)
decryptedRply = cipher.decrypt(replyMsg2)
reply = decryptedRply.decode("utf-8")
print("Reply Recieved: ",reply)
s.close()





