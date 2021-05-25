import pygame
from pygame.constants import KEYDOWN, K_BACKSPACE, K_ESCAPE, K_RETURN
import visuals as v
import snkCliente as sC

pygame.init()

def colisiones(snake_pos,snake_body,score): #Detector de colisiones
    if snake_pos[0] <= v.posInicio[0] or snake_pos[0] >= v.size[0]-10:              
        return False,v.Pcontinuar(score),sC.accion(score)           
    if snake_pos[1] <= v.posInicio[1] or snake_pos[1] >= v.size[1]-10:
        return False,v.Pcontinuar(score),sC.accion(score)
    for i in range(1,len(snake_body)):
        if snake_body[i] == snake_pos:   
            return False,v.Pcontinuar(score)
    return True

def realizar(instruido):
    return instruido 

class Snake(): #Juego 
    def start(cliente):
        print("El juego comenzo")
        movimiento = "RIGHT"
        v.posInicio,v.rgb = realizar(sC.devolver()) #Recive del server la posicion inicial y Recive del server el color del jugador
        print("posicion inicial serpiente: ", v.posInicio)
        print("color serpiente: ",v.rgb)
        snake_pos = [v.posInicio[0]+100,v.posInicio[1]+50]
        snake_body =[[v.posInicio[0]+100,v.posInicio[1]+50],[v.posInicio[0]+90,v.posInicio[1]+50],[v.posInicio[0]+80,v.posInicio[1]+50]]   
        run = True    
        food_pos = v.food()    
        score = 0
        cliente.enviar(movimiento)
        while (run):        
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if movimiento != "LEFT":
                        if event.key == pygame.K_RIGHT:  
                            cliente.enviar("RIGHT")
                            movimiento = "RIGHT"
                    if movimiento != "RIGHT": 
                        if event.key == pygame.K_LEFT: 
                            cliente.enviar("LEFT") 
                            movimiento = "LEFT"
                    if movimiento != "DOWN":
                            if event.key == pygame.K_UP:  
                                cliente.enviar("UP")
                                movimiento = "UP"
                    if movimiento != "UP":
                        if event.key == pygame.K_DOWN:  
                            cliente.enviar("DOWN")
                            movimiento = "DOWN"
            intruccion = realizar(sC.devolver())
            if intruccion == "RIGHT":
                snake_pos[0]+=10
            if intruccion == "LEFT":
                snake_pos[0]-=10
            if intruccion == "UP":
                snake_pos[1]-=10
            if intruccion == "DOWN":
                snake_pos[1]+=10
            snake_body.insert(0,list(snake_pos))  
            snake_body,score,food_pos = v.comer(snake_pos,snake_body,food_pos,score)  
            v.screen.fill((0,0,0))
            v.limites() 
            for pos in snake_body:
                pygame.draw.rect(v.screen,(v.rgb[0],v.rgb[1],v.rgb[2]),pygame.Rect(pos[0],pos[1],10,10))
            pygame.draw.rect(v.screen,(v.rgb[0],v.rgb[1],v.rgb[2]),pygame.Rect(food_pos[0],food_pos[1],10,10))
            text = v.font.render(str(score),0,(200,60,80))
            v.screen.blit(text,(v.size[0]-30,20))
            if score < 5:
                v.fps.tick(10)
            elif score < 50:
                v.fps.tick(score+5)
            run = colisiones(snake_pos,snake_body,score)               
            pygame.display.flip()





