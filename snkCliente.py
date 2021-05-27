import socket,threading,pygame,pickle
from pygame.constants import KEYDOWN, K_BACKSPACE, K_ESCAPE, K_RETURN
import visuals as v
import snakeGame as sG

comando=""

def accion_reaccion(instruccion):
    global comando
    comando= instruccion

def devolver():
    global comando
    return comando

class Entrada(): #Entrada de texto/datos ------ Faltan Arreglos
    def __init__(self):
        self.ip =""
        self.linea =0
        self.caracteres = ['',]
        self.font = pygame.font.Font(None,30)
        self.espaciado = 20
        self.posx=50
        self.posy = 50

    def teclas(self,evento):
        for accion in evento:
            if accion.type == KEYDOWN:
                if accion.key == K_RETURN:
                    self.caracteres.append('')
                    self.linea +=1
                    print(self.ip)
                elif accion.key == K_BACKSPACE:
                    if self.caracteres[self.linea]=='' and self.linea > 0:
                        self.caracteres == self.caracteres[0:-1]
                        self.linea-=1
                        self.texto()
                    else:
                        self.caracteres[self.linea] = self.caracteres[self.linea][0:-1]
                elif accion.key == K_ESCAPE:
                    v.num_jugador()                    
                else:
                    self.caracteres[self.linea]=str(self.caracteres[self.linea]+accion.unicode)

    def texto(self,display,pos):
        for self.linea in range(len(self.caracteres)):
            letra = self.font.render(self.caracteres[self.linea],True,(230,230,230))
            self.ip = self.caracteres[self.linea]
        display.blit(letra,(pos+20,(v.size[1]/3)+30))

    def unirse(self):
        start = False
        v.screen.fill((0,0,0))
        ip = Entrada()
        while (not start):
            text = v.font.render(str("---- Escribir IP: ----"),0,(200,60,80))
            x = v.size[0]/2-(len(str(text))/2)*(v.size[0]/((v.size[0]/10)-6))
            v.screen.blit(text,(x+5,v.size[1]/3))
            v.limites()  
            if self.linea <=15:   
                eventos = pygame.event.get()
                for event in eventos:
                    if event.type == pygame.QUIT: pygame.quit()
                    if event.type == pygame.K_RETURN:
                        start = True
                        v.num_jugador()
                ip.teclas(eventos)
                ip.texto(v.screen,x)
                pygame.display.flip()

class Hilo_cliente(threading.Thread): #Hilo
    def __init__(self,socket,cliente):
        threading.Thread.__init__(self)
        self.socket = socket
        self.cliente = cliente
        self.comenzar = False
        self.terminar = False
    def run(self):        
        try:
            data = self.socket.recv(2048)
            v.posInicio,v.rgb,self.cliente.id = pickle.loads(data)
            instruccion=""
            while "comenzar" not in instruccion:
                data = self.socket.recv(2048)
                instruccion = data.decode() 
                accion_reaccion(instruccion[2:])   
            self.comenzar = True          
            while True:
                data = self.socket.recv(2048)
                instruccion = data.decode()
                print(instruccion)
                if instruccion !="":
                    if "ganador" in instruccion:
                        self.terminar = True
                        if str(self.cliente.id) in instruccion:
                            accion_reaccion(f"ganaste{instruccion[13:]}")
                        else:
                            accion_reaccion(f"perdiste{instruccion[13:]}")
                    else:
                        if str(self.cliente.id) in instruccion:                    
                            accion_reaccion(instruccion[2:])                
        except Exception as e:
            print()

class Cliente(): #Cliente
    host="26.19.70.130" #Direccion en la que se conectara el cliente 
    def __init__(self):
        try:
            self.mi_socket = socket.socket()
            self.mi_socket.connect((self.host,3000))
            self.id =0
        except: 
            print("No se ha encontrado el servidor")

    def iniciar(self):
        #host = input("Ingrese ip a conectar")
        hilo = Hilo_cliente(self.mi_socket,self)
        hilo.start()
        while not hilo.comenzar:
            v.Pespera(devolver(),self)
        sG.Snake.start(self)
        while not hilo.terminar:
            v.Pespera(devolver(),self)
        if "ganaste" in devolver():
            v.PcontinuarG(devolver()[8:],self)
        else:
            v.PcontinuarP(devolver()[8:],self)

    def enviar(self,instruccion):
        dt = str(f"{self.id}{instruccion}").encode()
        self.mi_socket.send(dt)
