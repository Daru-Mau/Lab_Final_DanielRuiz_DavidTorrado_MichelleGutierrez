import pygame,random,sys,pickle
from pygame.constants import KEYDOWN, K_BACKSPACE, K_ESCAPE, K_RETURN
import visuals as v
from snkCliente import accion,reaccion

pygame.init()

movimiento = "RIGHT"

def colisiones(snake_pos,score): #Detector de colisiones
    if snake_pos[0] <= v.posInicio[0] or snake_pos[0] >= v.size[0]-10:              
        return False,v.Pcontinuar(score),accion(score)           
    if snake_pos[1] <= v.posInicio[1] or snake_pos[1] >= v.size[1]-10:
        return False,v.Pcontinuar(score),accion(score)
    return True

def instruccion(instruido):
    global movimiento
    movimiento = instruido

class snake(): #Juego 
    def start():
        global movimiento
        v.posInicio = reaccion() #Recive del server la posicion inicial
        rgb = reaccion() #Recive del server el color del jugador
        snake_pos = [v.posInicio[0]+100,v.posInicio[1]+50]
        snake_body =[[v.posInicio[0]+100,v.posInicio[1]+50],[v.posInicio[0]+90,v.posInicio[1]+50],[v.posInicio[0]+80,v.posInicio[1]+50]]   
        run = True    
        food_pos = v.food()    
        score = 0
        accion(movimiento)
        while (run):        
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT: accion("RIGHT")
                    if event.key == pygame.K_LEFT: accion("LEFT") 
                    if event.key == pygame.K_UP: accion("UP" )
                    if event.key == pygame.K_DOWN: accion("DOWN" )
            snake_pos = reaccion()
            snake_body.insert(0,list(snake_pos))  
            snake_body,score,food_pos = v.comer(snake_pos,snake_body,food_pos,score)  
            v.screen.fill((0,0,0))
            v.limites() 
            for pos in snake_body:
                pygame.draw.rect(v.screen,(rgb[0],rgb[1],rgb[2]),pygame.Rect(pos[0],pos[1],10,10))
            pygame.draw.rect(v.screen,(rgb[0],rgb[1],rgb[2]),pygame.Rect(food_pos[0],food_pos[1],10,10))
            text = v.font.render(str(score),0,(200,60,80))
            v.screen.blit(text,(v.size[0]-30,20))
            if score < 5:
                v.fps.tick(10)
            elif score < 50:
                v.fps.tick(score+5)
            run = colisiones(snake_pos,score)               
            pygame.display.flip()





