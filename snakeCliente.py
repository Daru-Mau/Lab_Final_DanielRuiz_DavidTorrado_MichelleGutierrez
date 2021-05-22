import pygame,random,socket,sys,threading
#from snakeMultiplayer.serverSnake import servidor,hilo_server
from pygame.constants import KEYDOWN, K_BACKSPACE, K_ESCAPE, K_RETURN

pygame.init()
size = 310,310
nJugadores=1
players =0,0
posInicio=0,0
screen = pygame.display.set_mode(size)
fps = pygame.time.Clock()
pygame.display.set_caption("Snake Online Game")
font = pygame.font.SysFont("comicsansms",20)

def food(): #posicion de la comida
    random_posx = random.randint(10,(size[0]/10)-10)*10
    random_posy = random.randint(10,(size[0]/10)-10)*10    
    food_pos = [random_posx,random_posy]
    return food_pos

class hilo_cliente(threading.Thread): #Hilo
    def __init__(self,socket):
        threading.Thread.__init__(self)
        self.socket = socket
    def run(self):
        while True:
            data = self.socket.recv(2048)
            recivido = data.decode()
            if recivido =="":
                continue
            print(recivido)

class cliente(): #Cliente
    server="" #Direccion en la que se conectara el cliente
    def iniciar():
        server = input("Ingrese ip a conectar")
        try:
            mi_socket = socket.socket()
            mi_socket.connect((server,3000))
        except: 
            print("No se ha encontrado el servidor")
        hilo = hilo_cliente(mi_socket)
        hilo.start()
        while True:
            data = "" #Instruccion
            dt = (data.encode())
            mi_socket.send(dt)

def randomColor(): #Generador del color de la serpiente
    rgb = [0,0,0]
    for i in range(3):
        rgb[i] = random.randint(0,255)
    return rgb

def limites(): #Bordes del juego

    global nJugadores
    if nJugadores == 1:
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(0,(players[1]/2)-10,players[1]/2,10)) # barra medio
        pygame.draw.rect(screen,(200,60,80),pygame.Rect((players[0]/2)-10,0,10,players[0]/2)) #barra vertical
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(0,0,10,players[0]/2)) # techo 
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(0,0,players[1]/2,10)) # lateral izquierdo
    if nJugadores == 2:
        pygame.draw.rect(screen,(200,60,80),pygame.Rect((players[0]/2)-10,0,10,players[0]/2)) #barra vertical
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(0,(players[1]/2)-10,players[1],10)) # barra medio
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(players[0]-10,0,10,players[0]/2)) # lateral derecho
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(0,0,10,players[0]/2)) # techo 
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(0,0,players[1],10)) # lateral izquierdo
    if nJugadores == 3:
        pygame.draw.rect(screen,(200,60,80),pygame.Rect((players[0]/2)-10,0,10,players[0])) #barra vertical
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(0,(players[1]/2)-10,players[1],10)) # barra medio
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(players[0]-10,0,10,players[0]/2)) # lateral derecho
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(0,players[1]-10,players[1]/2,10)) # fondo
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(0,0,10,players[0])) # techo 
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(0,0,players[1],10)) # lateral izquierdo
    if nJugadores == 4:
        pygame.draw.rect(screen,(200,60,80),pygame.Rect((players[0]/2)-10,0,10,players[0])) #barra vertical
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(0,(players[1]/2)-10,players[1],10)) # barra medio
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(players[0]-10,0,10,players[0])) # lateral derecho
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(0,players[1]-10,players[1],10)) # fondo
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(0,0,10,players[0])) # techo 
        pygame.draw.rect(screen,(200,60,80),pygame.Rect(0,0,players[1],10)) # lateral izquierdo

def colisiones(snake_pos,score): #Detector de colisiones
    if snake_pos[0] <= 0 or snake_pos[0] >= size[0]-5:              
        return False,Pcontinuar(score)            
    if snake_pos[1] <= 0 or snake_pos[1] >= size[1]-5:
        return False,Pcontinuar(score)
    return True
    
def comer(snake_pos,snake_body,food_pos,score): #Metodo de comer
    if snake_pos == food_pos: 
        food_pos = food()
        score +=1   
    else:
        snake_body.pop()     
    return snake_body,score,food_pos

def num_jugador(): #Seleccion de jugadores para crear server
    global nJugadores
    start = False
    global screen
    screen.fill((0,0,0))
    limites()
    while (not start):
        text = font.render(str("--- Cantidad de Jugadores: ---"),0,(200,60,80))
        op1 = font.render(str("1 para un jugador"),0,(200,60,80))
        op2 = font.render(str("2 para un jugador"),0,(200,60,80))
        op3 = font.render(str("3 para un jugador"),0,(200,60,80))
        op4 = font.render(str("4 para un jugador"),0,(200,60,80))
        x = size[0]/2-(len(str(text))/2)*(size[0]/((size[0]/10)-6))
        screen.blit(text,(x+5,size[1]/3))
        screen.blit(op1,(x+20,(size[1]/3)+30))
        screen.blit(op2,(x+20,(size[1]/3)+60))
        screen.blit(op3,(x+20,(size[1]/3)+90))
        screen.blit(op4,(x+20,(size[1]/3)+120))      
        pygame.display.flip()        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: 
                    nJugadores =1              
                    start = True  
                    players = 310,310
                    screen = pygame.display.set_mode(players)                      
                    snake.start() 
                if event.key == pygame.K_2:
                    nJugadores =2   
                    players = 610,310
                    screen = pygame.display.set_mode(players)
                    start = True    
                    snake.start()
                if event.key == pygame.K_3:  
                    nJugadores =3                         
                    players = 610,610
                    screen = pygame.display.set_mode(players)                 
                    start = True                        
                    snake.start() 
                if event.key == pygame.K_4: 
                    nJugadores =4   
                    start = True    
                    players = 610,610
                    screen = pygame.display.set_mode(players)
                    snake.start()

class Entrada(): #Entrada de texto/datos
    def __init__(self,):
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
                        print("borrar")
                    else:
                        self.caracteres[self.linea] = self.caracteres[self.linea][0:-1]
                elif accion.key == K_ESCAPE:
                    Pmenu()                    
                else:
                    self.caracteres[self.linea]=str(self.caracteres[self.linea]+accion.unicode)

    def texto(self,display,pos):
        for self.linea in range(len(self.caracteres)):
            letra = self.font.render(self.caracteres[self.linea],True,(230,230,230))
            self.ip = self.caracteres[self.linea]
        display.blit(letra,(pos+20,(size[1]/3)+30))

    def unirse(self,):
        start = False
        screen.fill((0,0,0))
        ip = Entrada()
        while (not start):
            text = font.render(str("---- Escribir IP: ----"),0,(200,60,80))
            x = size[0]/2-(len(str(text))/2)*(size[0]/((size[0]/10)-6))
            screen.blit(text,(x+5,size[1]/3))
            limites()  
            if self.linea <=15:   
                eventos = pygame.event.get()
                for event in eventos:
                    if event.type == pygame.QUIT: pygame.quit()
                ip.teclas(eventos)
                ip.texto(screen,x)
                pygame.display.flip()

def Pmenu(): #Pantalla Menu de Inicio
    start = False
    screen.fill((0,0,0))
    while (not start):
        text = font.render(str("---- Custom Snake Game: ----"),0,(200,60,80))
        op1 = font.render(str("C para crear a partida"),0,(200,60,80))
        op2 = font.render(str("Espacio para unirse a partida"),0,(200,60,80))
        x = size[0]/2-(len(str(text))/2)*(size[0]/((size[0]/10)-6))
        screen.blit(text,(x+5,size[1]/3))
        screen.blit(op1,(x+20,(size[1]/3)+60))
        screen.blit(op2,(x,(size[1]/3)+30)) 
        limites()       
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:                        
                    start = True                    
                    Entrada.unirse()                    
                if event.key == pygame.K_c:                        
                    start = True                    
                    num_jugador()

def Pespera(): #Pantalla de espera
    esperando = True
    jugadores = nJugadores - 1
    screen.fill((0,0,0))
    while (esperando):
        text = font.render(str("---- Esperando Jugadores ----"),0,(200,60,80))
        op2 = font.render(str("Jugadores conectas: {}").format(jugadores),0,(200,60,80))
        op2 = font.render(str("Escape para abandonar"),0,(200,60,80))
        x = (size[0]/2 - text.get_width() // 2, size[1]/2 - text.get_height() // 2)
    #size[0]/2-(len(str(text))/2)*(size[0]/((size[0]/10)-6))
        screen.blit(text,(x+5,size[1]/3))
        screen.blit(op2,(x,(size[1]/3)+30)) 
        limites()       
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:                        
                    esperando = True                    
                    Pmenu()

def Pcontinuar(puntaje): #Pantalla de final/Continuar
    global screen
    screen.fill((0,0,0))
    limites()
    score = font.render(str("Puntaje: {}".format(puntaje)),0,(200,60,80))
    text = font.render(str("---- Perdiste ----"),0,(200,60,80))
    op2 = font.render(str("R para revancha"),0,(200,60,80))
    op3 = font.render(str("Espacio para continuar"),0,(200,60,80))
    screen.blit(score,(size[1]/8,size[1]/4+30))
    screen.blit(text,(size[1]/8,size[1]/4))
    screen.blit(op2,(size[1]/8,size[1]/4+60))
    screen.blit(op3,(size[1]/8,(size[1]/4)+90))
    pygame.display.flip()
    continuar = False
    while not continuar:
        for event in pygame.event.get():            
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.QUIT: pygame.quit()
                if event.key == pygame.K_SPACE:
                    continuar=True
                    screen.fill((0,0,0))
                    players = size
                    screen = pygame.display.set_mode(players)
                    Pmenu()
                if event.key == pygame.K_r:
                    continuar=True
                    screen.fill((0,0,0))
                    Pmenu()

class snake(): #Juego 
    global posInicio
    def start():
        rgb = randomColor() 
        snake_pos = [posInicio[0]+100,posInicio[1]+50]
        snake_body =[[100,50],[90,50],[80,50]]   
        run = True    
        food_pos = food()    
        score = 0
        change = "RIGHT"    
        while (run):        
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT: change = "RIGHT" 
                    if event.key == pygame.K_LEFT: change = "LEFT" 
                    if event.key == pygame.K_UP: change = "UP" 
                    if event.key == pygame.K_DOWN: change = "DOWN" 
            if change == "RIGHT":
                snake_pos[0]+=10
            if change == "LEFT":
                snake_pos[0]-=10
            if change == "UP":
                snake_pos[1]-=10
            if change == "DOWN":
                snake_pos[1]+=10
            snake_body.insert(0,list(snake_pos))  
            snake_body,score,food_pos = comer(snake_pos,snake_body,food_pos,score)  
            screen.fill((0,0,0))
            limites() 
            for pos in snake_body:
                pygame.draw.rect(screen,(rgb[0],rgb[1],rgb[2]),pygame.Rect(pos[0],pos[1],10,10))
            pygame.draw.rect(screen,(rgb[0],rgb[1],rgb[2]),pygame.Rect(food_pos[0],food_pos[1],10,10))
            text = font.render(str(score),0,(200,60,80))
            screen.blit(text,(size[0]-30,20))
            if score < 5:
                fps.tick(10)
            elif score < 50:
                fps.tick(score+5)
            run = colisiones(snake_pos,score)               
            pygame.display.flip()

Pmenu()




