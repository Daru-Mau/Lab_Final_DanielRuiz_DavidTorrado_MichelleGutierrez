import pygame,pickle
from pygame.constants import KEYDOWN, K_BACKSPACE, K_ESCAPE, K_RETURN
import visuals as v
import snkCliente as sC

pygame.init()

def colisiones(snake_pos,snake_body,c,score): #Detector de colisiones
    if snake_pos[0] <= v.posInicio[0]+10 or snake_pos[0] >= v.posInicio[0]+310:
        return False#,c.enviar(f"score{score}")      
    if snake_pos[1] <= v.posInicio[1]+10 or snake_pos[1] >= v.posInicio[1]+310:    
        return False#,c.enviar(f"score{score}")
    #for i in range(2,len(snake_body)):
        if snake_body[i] == snake_pos:
            return False
    return True

def recibir(instruido):
    return instruido 

class Snake(): #Juego 
    def start(cliente):
        snake_pos = [v.posInicio[0]+100,v.posInicio[1]+50]
        snake_body =[[v.posInicio[0]+100,v.posInicio[1]+50],[v.posInicio[0]+90,v.posInicio[1]+50],[v.posInicio[0]+80,v.posInicio[1]+50]]   
        run = True    
        food_pos = v.puntos()    
        score = 0
        instruccion = "RIGHT"
        cliente.enviar(instruccion)
        while run:        
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    cliente.enviar("salir")
                    cliente.mi_socket.close()
                if event.type == pygame.KEYDOWN:
                    if instruccion != "LEFT":
                        if event.key == pygame.K_RIGHT:  
                            cliente.enviar("RIGHT")
                            instruccion = "RIGHT"
                    if instruccion != "RIGHT": 
                        if event.key == pygame.K_LEFT: 
                            cliente.enviar("LEFT") 
                            instruccion = "LEFT"
                    if instruccion != "DOWN":
                        if event.key == pygame.K_UP:  
                            cliente.enviar("UP")
                            instruccion = "UP"
                    if instruccion != "UP":
                        if event.key == pygame.K_DOWN:  
                            cliente.enviar("DOWN")
                            instruccion = "DOWN"
            if recibir(sC.devolver()) != "":
                 instruccion = recibir(sC.devolver())
            if "RIGHT" in instruccion:
                snake_pos[0]+=10
            if "LEFT" in instruccion:
                snake_pos[0]-=10
            if "UP" in instruccion:
                snake_pos[1]-=10
            if "DOWN" in instruccion:
                snake_pos[1]+=10            
            snake_body.insert(0,list(snake_pos)) 
            snake_body,score,food_pos = v.comer(snake_pos,snake_body,food_pos,score)  
            v.screen.fill((0,0,0))
            v.limites() 
            for pos in snake_body:
                pygame.draw.rect(v.screen,(v.rgb[0],v.rgb[1],v.rgb[2]),pygame.Rect(pos[0],pos[1],10,10))
            for food in food_pos:
                pygame.draw.rect(v.screen,(v.rgb[0],v.rgb[1],v.rgb[2]),pygame.Rect(food[0],food[1],10,10))
            text = v.font.render(str(score),0,(200,60,80))
            v.screen.blit(text,(v.posInicio[0]+v.size[0]-30,v.posInicio[1]+20))
            if score < 5:
                v.fps.tick(10)
            elif score < 50:
                v.fps.tick(score+5)
            run = colisiones(snake_pos,snake_body,cliente,score)  
            if run == False:
                cliente.enviar(f"score{score}")             
            pygame.display.flip() 
              





