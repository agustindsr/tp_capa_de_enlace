"""
Este es el lado del emisor de un protocolo de detencion y espera.

Hace esto:

1) Solicita la entrada del usuario para la cadena de bits, el tiempo de propagacion y la probabilidad de
el paquete se caiga entre el remitente y el receptor.

2)Luego procede a enviar o no enviar (para simular la caida de un
canal no confiable) los bits de la cadena de bits de entrada.
"""

#realiza imports
import socket
from threading import *
import time
import random



#------------------------------------------------------------------------
#crea el socket y lo une al puerto 8000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 8000
s.bind((host, port))

#------------------------------------------------------------------------
#define la clase para el cliente
class client(Thread):
    #inicializacion
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()


    def run(self):

        while True:

            #toma la entrada del usuario
            bitstring  = str(input("ingresa la cadena de bits"))
            propogationtime = float(input("ingresa el tiempo de propagacion de cada paquete"))
            p_nosend = float(input("ingresa la probabilidad de perder el mensaje:"))
            
            #crea una lista de 1000 elementos(se puede modificar)
            l = []
            for i in range(0,1000):
                l = l +[i]

            #recorre los bits de toda la cadena
            i = 0
            while i < len(bitstring):
                #por cada bit, crea un  diccionario con el indice
                #de ventana actual (i%2 => 0,1,0,1...) ay el bit en si mismo
                datadict = {}
                datadict = {i%2 : bitstring[i], }
                
                #convierte el diccionario a una cadena
                sendstring = str(datadict)
                
                #encuentra un numero entre 0 y 1000
                number= random.randint(0,1000)
                
                #almacena el tiempo actual
                time1 = time.time()
                
                #la condicion es verdadera con una probabilidad de (1-p_nosend)
                if l[number] < (p_nosend*1000):
                    #si es verdadera,envia la cadena de bits
                    clientsocket.send(sendstring)
                    #espera para simular el tiempo de propagacion del canal
                    time.sleep((propogationtime)/1.1)
                    #despues de parar,guarda el tiempo actual
                    time2 = time.time()
                    #la bandera indica si el acuse de recibo ha sido recibido
                    ackflag= False
                
                #la sentencia else is verdadera con una probability of (p_nosend)
                #this simulates a packet being sent but getting lost
                #simula un paquete siendo enviado pero que luego se pierde
                else:
                    #espera por el tiempo de propagacion ,otra vez
                    time.sleep(propogationtime/1.1)
                    #guarda el tiempo actual
                    time2 = time.time()
                    #le informa al usuario:
                    print ("package dropped 1")
                    #setea la bandera de acuse de recibo a Falso , de vuelta.
                    ackflag= False               

                while True:

                    #si el tiempo transcurrido es menor que el tiempo de propagacion del paquete
                    if time2-time1<= propogationtime:
                        #almacena el tiempo actual
                        time2= time.time()


                        #setea el tiempo de espera para el acuse de recibo
                        clientsocket.settimeout(propogationtime/1.1)

                        #lanza una excepcion cuando se acaba el tiempo de espera
                        try:
                            #preparado para escuchar por un acuse de recibo
                            recieved = clientsocket.recv(1024)
                            print(recieved)
                            
                            if recieved:
                                print("ack received")
                                i = i+1
                                ackflag = True
                                break 

                        #esto ocurre si se acaba el tiempo de espera
                        except:
                            #vuelve a chequear si se termino el tiempo de espera
                            if time2 - time1 >propogationtime and ackflag == False:
                                print ("timeout")

                                #aca simulamos la caida del paquete
                                #con la probabilidad ingresada por el usuario
                                number= random.randint(0,1000)

                                #paquete enviado
                                if l[number] < (p_nosend*1000):
                                    clientsocket.send(sendstring)
                                    time1 = time.time()
                                    time2 = time.time()
                                    print("package sent")

                                #paquete perdido
                                else: 
                                    
                                    time1 = time.time()
                                    time2 = time.time()
                                    #time.sleep(propogationtime/1.1)
                                    
                                    print("package dropped 2")

                        
                    
                    
    
            

s.listen(5)
print ('Emisor listo y escuchando')
while (True):

    #acepta todas las conexiones entrantes
    clientsocket, address = s.accept()
    print("Receiver "+str(address)+" connected")
    #crea un hilo distinto para cada conexion entrante
    client(clientsocket, address)
