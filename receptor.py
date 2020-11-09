"""

Este es el lado receptor de un protocolo de parada y espera

Realiza lo siguiente:
It does the following :

1)Pregunta al usuario la probabilidad de que el acuse de recibe no sea enviado

2)Luego procede a enviar o no enviar (para simular la caida de un
canal no confiable) un reconocimiento.

"""

#make necessary imports
import socket
import random
from ast import literal_eval


#------------------------------------------------------------------------
#create socket object and bind it.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host ="localhost"
port =8000
s.connect((host,port))

#------------------------------------------------------------------------

#take input from user 
p_noack = float(input("Ingresa la probabilidad de que el acuse de recibo no se envie"))
count = 0 


def try_ack(previous, current):
    if abs(previous-current) == 1:
        return True
    else:
        return False 

l = []
for i in range(0,1000):
    l = l +[i]
output = ""
   
while 2: 
    data=s.recv(8).decode()
    print("Received --> "+data)
    datadict = literal_eval(data)
    index = list((datadict).keys())[0]
    number= random.randint(0,1000)
    if count == 0:
        count = count +1
        current = index
        previous = 0
        if current == 0:
            previous = 1
    
    #simulando que el mensaje de reconocimiento se pierde en el camino
    else: 
        count = count +1
        previous = current
        current = index
        print ("p /c :", previous, current)
    if try_ack(previous, current):
        output  = output + list(datadict.values())[0]
        #print ("hello", l[number],p_noack*1000 )
        if l[number]<(p_noack*1000):
            print("Ack not sent")
            pass
        else:    
            str="Acknowledgement: Message Received"
            #print ("!!!!!!!!!")
            
            #print datadict.values()
            s.send(str.encode())
    else: 
        str="Acuse de recibo: Mensaje Recibido"
        s.send(str.encode())
        print ("Indices no coinciden. Enviando  acuse de recibo para  paquete previo")
    print("La cadena de bits recibida es ",output)
  
s.close ()
