import socket,threading,pygame,pickle
from pygame.constants import KEYDOWN, K_BACKSPACE, K_ESCAPE, K_RETURN
import visuals as v
import snakeGame as sG

def accion_reaccion(instruido):
    return instruido

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
    def __init__(self,socket):
        threading.Thread.__init__(self)
        self.socket = socket
    def run(self):
        data = self.socket.recv(2048)
        instruccion = data.decode()
        while instruccion != "comenzar":
            v.Pespera()
        sG.snake.start(self)
        while True:
            data = self.socket.recv(2048)
            instruccion = data.decode()
            accion_reaccion(instruccion)           
            if instruccion =="":
                continue

class Cliente(): #Cliente
    host="localhost" #Direccion en la que se conectara el cliente 
    def iniciar(self):
        #host = input("Ingrese ip a conectar")
        try:
            mi_socket = socket.socket()
            mi_socket.connect((self.host,3000))
        except: 
            print("No se ha encontrado el servidor")
        hilo = Hilo_cliente(mi_socket)
        hilo.start()

    def enviar(self,instruccion):
        dt = instruccion.encode()
        self.mi_socket.send(dt)
