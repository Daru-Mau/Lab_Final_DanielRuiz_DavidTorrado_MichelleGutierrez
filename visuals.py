import pygame,random
import snkCliente as sC

pygame.init()
size = 310,310
nJugadores=1
players =0,0
posInicio=0,0
rgb = 0,0,0
font = pygame.font.SysFont("comicsansms",20)
screen = pygame.display.set_mode(size)
fps = pygame.time.Clock()
food_pos =[]
pygame.display.set_caption("Snake Online Game")

def puntos(): #posicion de la comida
    global food_pos
    if len(food_pos) == 0:
        for x in range(1):
            random_posx = random.randint(10,(size[0]/10)-10)*10
            random_posy = random.randint(10,(size[0]/10)-10)*10    
            food_pos.append([random_posx,random_posy])
    if len(food_pos)<1:
        while len(food_pos)<10:
            random_posx = random.randint(10,(size[0]/10)-10)*10
            random_posy = random.randint(10,(size[0]/10)-10)*10    
            food_pos.append([random_posx,random_posy])
    return food_pos

def comer(snake_pos,snake_body,food_pos,score): #Metodo de comer
    for food in food_pos:
        if snake_pos == food:
            food_pos.remove(food)
            food_pos = puntos()
            score +=1
            return snake_body,score,food_pos
    snake_body.pop()            
    return snake_body,score,food_pos

def randomColor(): #Generador del color de la serpiente
    global rgb
    for i in range(3):
        rgb[i] = random.randint(0,255)
    return rgb

def limites(): #Bordes del juego
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
        x = (size[0]/2 - text.get_width() // 2, size[1]/2 - text.get_height() // 2)
        screen.blit(text,(x[0]+5,(size[1]/5)))
        screen.blit(op1,(x[0]+20,(size[1]/5)+30))
        screen.blit(op2,(x[0]+20,(size[1]/5)+60))
        screen.blit(op3,(x[0]+20,(size[1]/5)+90))
        screen.blit(op4,(x[0]+20,(size[1]/5)+120))      
        pygame.display.flip()        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:     
                    start = True  
                    players = 310,310
                    screen = pygame.display.set_mode(players)
                    c = sC.Cliente() 
                    c.iniciar() 
                    c.enviar(nJugadores)   
                if event.key == pygame.K_2:
                    nJugadores =2   
                    players = 610,310
                    screen = pygame.display.set_mode(players)
                    start = True  
                    c = sC.Cliente() 
                    c.iniciar()  
                    c.enviar(nJugadores) 
                if event.key == pygame.K_3:  
                    nJugadores =3                         
                    players = 610,610
                    screen = pygame.display.set_mode(players)                 
                    start = True   
                    c = sC.Cliente() 
                    c.iniciar()  
                    c.enviar(nJugadores)
                if event.key == pygame.K_4: 
                    nJugadores =4   
                    start = True    
                    players = 610,610
                    screen = pygame.display.set_mode(players)
                    c = sC.Cliente()
                    c.iniciar()
                    c.enviar(nJugadores)

def Pmenu(): #Pantalla Menu de Inicio
    start = False
    screen.fill((0,0,0))
    while (not start):
        text = font.render(str("---- Custom Snake Game: ----"),0,(200,60,80))
        op1 = font.render(str("C para crear a partida"),0,(200,60,80))
        op2 = font.render(str("Espacio para unirse a partida"),0,(200,60,80))
        x = (size[0]/2 - text.get_width() // 2, size[1]/2 - text.get_height() // 2)
        screen.blit(text,(x[0]+5,size[1]/3))
        screen.blit(op1,(x[0],(size[1]/3)+60))
        screen.blit(op2,(x[0],(size[1]/3)+30)) 
        limites()       
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:                        
                    start = True                    
                    entrada = sC.Entrada() 
                    entrada.unirse()                  
                if event.key == pygame.K_c:                        
                    start = True                    
                    num_jugador()

def Pespera(texto): #Pantalla de espera
    jugadores = texto
    screen.fill((0,0,0))
    text = font.render(str("---- Esperando Jugadores ----"),0,(200,60,80))
    op2 = font.render(str("Jugadores conectados: {}").format(jugadores),0,(200,60,80))
    op2 = font.render(str("Escape para abandonar"),0,(200,60,80))
    x = (size[0]/2 - text.get_width()/2, size[1]/2 - text.get_height()/2)
    screen.blit(text,(x[0]+5,size[1]/3))
    screen.blit(op2,(x[0],(size[1]/3)+30)) 
    limites()       
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:                 
                Pmenu()

def Pcontinuar(puntaje): #Pantalla de final/Continuar
    global screen
    screen.fill((0,0,0))
    limites()
    score = font.render(str("Puntaje: {}".format(puntaje)),0,(200,60,80))
    text = font.render(str("---- Perdiste ----"),0,(200,60,80))
    op2 = font.render(str("R para revancha"),0,(200,60,80))
    op3 = font.render(str("Espacio para continuar"),0,(200,60,80))
    x = (size[0]/2 - text.get_width() // 2, size[1]/2 - text.get_height() // 2)
    screen.blit(text,(x[0],size[1]/4))
    screen.blit(score,(x[0]-20,size[1]/4+30))
    screen.blit(op2,(x[0]-20,size[1]/4+60))
    screen.blit(op3,(x[0]-20,(size[1]/4)+90))
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
