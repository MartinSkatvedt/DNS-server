import socket

port = 53
ip = "192.168.1.3"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind((ip, port))

def getFlags(flags):
    byte1 = bytes(flags[0:1])
    byte2 = bytes(flags[1:2])

    QR = "1" 
    
    OPCODE = ""
    for bit in range(1,5):
        OPCODE += str(ord(byte1)&(1<<bit))

    AA = "1" 
    TC = "0"
    RD = "0" 
    RA = "0" 
    Z  = "000" 
    RCODE = "0000"

    return int(QR + OPCODE+AA+TC+RD, 2).to_bytes(1, byteorder="big")+int(RA+Z+RCODE, 2).to_bytes(1, byteorder="big")


def getQuestionDomain(data):    
    state = 0
    expectLen = 0
    x = 0
    y = 0

    domainString = ""
    domainParts = []
    
    for byte in data:
        if state == 1: 

            if byte == 0: 
                break
            
            x += 1
            y += 1 
            domainString += chr(byte)
            
            if x == expectLen: 
                domainParts.append(domainString)
                domainString = ""
                state = 0
                x = 0         
        else: 
            state = 1
            expectLen = byte


    questionType = data[y+3:y+5]

    return (domainParts, questionType)

def getResponse(data):
    #Finner transactionID 
    transactionID = data[0:2]
    t_ID = ""    
    for byte in transactionID:    
        t_ID += hex(byte)[2:]

    #Finner flagg 
    flags = getFlags(data[2:4])

    #Question Count
    QDCOUNT = b"\x00\x01"

    #Answer Count 
    domainParts, questionType = getQuestionDomain(data[12:])    


    print (domainParts) 
    print (questionType) 
    
while 1: 
    data, addr = sock.recvfrom(512) 

    response = getResponse(data)
 
    #sock.sendto(response, addr);



