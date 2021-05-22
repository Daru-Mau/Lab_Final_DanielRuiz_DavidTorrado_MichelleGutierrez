import pygame,random,sys,pickle
#from serverSnake import servidor,hilo_server
from pygame.constants import KEYDOWN, K_BACKSPACE, K_ESCAPE, K_RETURN
import visuals as v

pygame.init()

def food(): #posicion de la comida
    random_posx = random.randint(10,(v.size[0]/10)-10)*10
    random_posy = random.randint(10,(v.size[0]/10)-10)*10    
    food_pos = [random_posx,random_posy]
    return food_pos

def colisiones(snake_pos,score): #Detector de colisiones
    if snake_pos[0] <= 0 or snake_pos[0] >= v.size[0]-5:              
        return False,v.Pcontinuar(score)            
    if snake_pos[1] <= 0 or snake_pos[1] >= v.size[1]-5:
        return False,v.Pcontinuar(score)
    return True

class snake(): #Juego 
    global posInicio
    def start():
        rgb = v.randomColor() 
        snake_pos = [v.posInicio[0]+100,v.posInicio[1]+50]
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





