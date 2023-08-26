import pygame
import math
import copy
from level1 import boards

WIDTH=900
HEIGHT=950
PI = math.pi

pygame.init()
screen = pygame.display.set_mode([WIDTH,HEIGHT])
timer = pygame.time.Clock()
fps=60
font=pygame.font.Font('freesansbold.ttf',20)
run = True
level = copy.deepcopy(boards)
level_color = 'blue'

frames_earthman=[]
for i in range(1,5):
    frames_earthman.append(pygame.transform.scale(
        pygame.image.load(
            f'assets/player_images/{i}.png'),(45,45)
        ))
    
gas_img = pygame.transform.scale(
    pygame.image.load(f'assets/ghost_images/blue.png'),(45,45)
)
gasX=440
gasY=388
gas_directions=2

nuclear_img = pygame.transform.scale(
    pygame.image.load(f'assets/ghost_images/orange.png'),(45,45)
)
nuclearX=440
nuclearY=438
nuclear_directions=2

carvao_img = pygame.transform.scale(
    pygame.image.load(f'assets/ghost_images/pink.png'),(45,45)
)
carvaoX=56
carvaoY=58
carvao_directions=0

petroleo_img = pygame.transform.scale(
    pygame.image.load(f'assets/ghost_images/red.png'),(45,45)
)
petroleoX=440
petroleoY=438
petroleo_directions=2

recicla_img = pygame.transform.scale(
    pygame.image.load(f'assets/ghost_images/powerup.png'),(45,45)
)
morto_img = pygame.transform.scale(
    pygame.image.load(f'assets/ghost_images/dead.png'),(45,45)
)


earthPosX=450
earthPosY=663
directions=0
direction_command=0
counter=0
velocidade=2
velocidade_fantasmas=[2,2,2,2]
flicker= False
pontuacao=0

energia=False
reciclagem_clock=0
energias_rec=[False,False,False,False]

alvos=[
    (earthPosX,earthPosY),
    (earthPosX,earthPosY),
    (earthPosX,earthPosY),
    (earthPosX,earthPosY)
]

carvao_morto = False
gas_morto = False
petroleo_morto = False
nuclear_morto = False

carvao_enjaulado = False
gas_enjaulado = False
petroleo_enjaulado = False
nuclear_enjaulado = False

iniciando_partida=0
vidas=3
gameOver = False
vitoria = False


altura_mapa=int((HEIGHT-50)/32)
largura_mapa=int(WIDTH/30)

class Ghost:
    def __init__(self, cordX, cordY, alvo, vel, img, dir, morto, jaula, id):
        self.x_pos = cordX
        self.y_pos = cordY
        self.centroX = self.x_pos+22
        self.centroY = self.y_pos+22
        self.alvo = alvo
        self.velocidade = vel
        self.img = img
        self.direction = dir
        self.morto = morto
        self.jaula = jaula
        self.id = id
        self.turns, self.enjaulado = self.checa_colisao()
        self.retan = self.draw()
    
    def checa_colisao(self):
        #DIREITA, ESQUERDA, CIMA, BAIXO
        if 350<self.centroY<480 and 370<self.centroX<480:
            self.enjaulado = True
        else:
            self.enjaulado = False
        sobra = 15
        self.turns = [False,False,False,False]
        if self.centroX//30<29:
            if self.morto:
                self.turns = [True,True,True,True]
            else:
                if level[self.centroY//altura_mapa][(self.centroX-sobra)//largura_mapa]<3 \
                or (level[self.centroY//altura_mapa][(self.centroX-sobra)//largura_mapa]== 9 and (
                self.enjaulado or self.morto)):
                    self.turns[1]=True
                if level[self.centroY//altura_mapa][(self.centroX+sobra)//largura_mapa]<3 \
                or (level[self.centroY//altura_mapa][(self.centroX+sobra)//largura_mapa]== 9 and (
                self.enjaulado or self.morto)):
                    self.turns[0]=True
                if level[(self.centroY+sobra)//altura_mapa][self.centroX//largura_mapa]<3 \
                or (level[(self.centroY+sobra)//altura_mapa][self.centroX//largura_mapa]== 9 and (
                self.enjaulado or self.morto)):
                    self.turns[3]=True
                if level[(self.centroY-sobra)//altura_mapa][self.centroX//largura_mapa]<3 \
                or (level[(self.centroY-sobra)//altura_mapa][self.centroX//largura_mapa]== 9 and (
                self.enjaulado or self.morto)):
                    self.turns[2]=True

                if self.direction==2 or self.direction==3:

                    if 12<=self.centroX%largura_mapa<=18:
                        if level[(self.centroY+sobra)//altura_mapa][self.centroX//largura_mapa] < 3 \
                        or (level[(self.centroY+sobra)//altura_mapa][self.centroX//largura_mapa] == 9 and(
                        self.enjaulado or self.morto)):
                            self.turns[3]=True

                        if level[(self.centroY-sobra)//altura_mapa][self.centroX//largura_mapa] < 3 \
                        or (level[(self.centroY-sobra)//altura_mapa][self.centroX//largura_mapa] == 9 and(
                        self.enjaulado or self.morto)):
                            self.turns[2]=True

                    if 12<=self.centroY%altura_mapa<=18:
                        if level[self.centroY//altura_mapa][(self.centroX-largura_mapa)//largura_mapa] < 3 \
                        or (level[self.centroY//altura_mapa][(self.centroX-largura_mapa)//largura_mapa] == 9 and(
                        self.enjaulado or self.morto)):
                            self.turns[1]=True

                        if level[self.centroY//altura_mapa][(self.centroX+largura_mapa)//largura_mapa] < 3 \
                        or (level[self.centroY//altura_mapa][(self.centroX+largura_mapa)//largura_mapa] == 9 and(
                        self.enjaulado or self.morto)):
                            self.turns[0]=True
                
                if self.direction==0 or self.direction==1:
                    
                    if 12<=self.centroX%largura_mapa<=18:
                        if level[(self.centroY+altura_mapa)//altura_mapa][self.centroX//largura_mapa] < 3 \
                        or (level[(self.centroY+altura_mapa)//altura_mapa][self.centroX//largura_mapa] == 9 and(
                        self.enjaulado or self.morto)):
                            self.turns[3]=True

                        if level[(self.centroY-altura_mapa)//altura_mapa][self.centroX//largura_mapa] < 3 \
                        or (level[(self.centroY-altura_mapa)//altura_mapa][self.centroX//largura_mapa] == 9 and(
                        self.enjaulado or self.morto)):
                            self.turns[2]=True

                    if 12<=self.centroY%altura_mapa<=18:
                        if level[self.centroY//altura_mapa][(self.centroX-largura_mapa)//largura_mapa] < 3 \
                        or (level[self.centroY//altura_mapa][(self.centroX-largura_mapa)//largura_mapa] == 9 and(
                        self.enjaulado or self.morto)):
                            self.turns[1]=True

                        if level[self.centroY//altura_mapa][(self.centroX+largura_mapa)//largura_mapa] < 3 \
                        or (level[self.centroY//altura_mapa][(self.centroX+largura_mapa)//largura_mapa] == 9 and(
                        self.enjaulado or self.morto)):
                            self.turns[0]=True
            
        else:
            self.turns[0] = True
            self.turns[1] = True
        
        
        return self.turns,self.enjaulado

    def draw(self):
        if (not energia and not self.morto) or (energias_rec[self.id] and energia and not self.morto): 
        #se não está ativo o powerup e o fantasma está vivo, ou se está ativo o powerup e o fantasma já foi comido e ressuscitou 
            screen.blit(self.img,(self.x_pos,self.y_pos))

        elif energia and not self.morto and not energias_rec[self.id]:
        #se o powerup está ativo e o fantasma ainda não foi comido
            screen.blit(recicla_img,(self.x_pos,self.y_pos))

        else:
            screen.blit(morto_img,(self.x_pos,self.y_pos))
        
        retangulo_fantasma = pygame.rect.Rect(
            (self.centroX-18,self.centroY-18),
            (36,36)
        )
        return retangulo_fantasma
    
    def move_petroleo(self):
        # petroleo vai virar sempre que for vantajoso para a perseguição
        if self.direction == 0:
            if self.alvo[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.velocidade
            elif not self.turns[0]:
                if self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
            elif self.turns[0]:
                if self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                if self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                else:
                    self.x_pos += self.velocidade
        elif self.direction == 1:
            if self.alvo[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.alvo[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.velocidade
            elif not self.turns[1]:
                if self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
            elif self.turns[1]:
                if self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                if self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                else:
                    self.x_pos -= self.velocidade
        elif self.direction == 2:
            if self.alvo[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.velocidade
            elif self.alvo[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.velocidade
            elif not self.turns[2]:
                if self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
            elif self.turns[2]:
                if self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                else:
                    self.y_pos -= self.velocidade
        elif self.direction == 3:
            if self.alvo[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.velocidade
            elif not self.turns[3]:
                if self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
            elif self.turns[3]:
                if self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                else:
                    self.y_pos += self.velocidade
        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30
        return self.x_pos,self.y_pos,self.direction
    
    def move_carvao(self):
        # carvão vai virar sempre que bater em uma parede, de outra forma, se manterá reto
        if self.direction == 0:
            if self.alvo[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.velocidade
            elif not self.turns[0]:
                if self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
            elif self.turns[0]:
                self.x_pos += self.velocidade

        elif self.direction == 1:
            if self.alvo[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.velocidade
            elif not self.turns[1]:
                if self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
            elif self.turns[1]:
                self.x_pos -= self.velocidade

        elif self.direction == 2:
            if self.alvo[1] < self.y_pos and self.turns[2]:
                self.y_pos -= self.velocidade
            elif not self.turns[2]:
                if self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
            elif self.turns[2]:
                self.y_pos -= self.velocidade

        elif self.direction == 3:
            if self.alvo[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.velocidade
            elif not self.turns[3]:
                if self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
            elif self.turns[3]:
                self.y_pos += self.velocidade

        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30
        return self.x_pos,self.y_pos,self.direction
    
    def move_gas(self):
        # gas vai virar em qualquer ponto para perseguir, mas direita e esquerda apenas durante colisões
        if self.direction == 0:
            if self.alvo[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.velocidade
            elif not self.turns[0]:
                if self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
            elif self.turns[0]:
                if self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                if self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                else:
                    self.x_pos += self.velocidade

        elif self.direction == 1:
            if self.alvo[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.alvo[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.velocidade
            elif not self.turns[1]:
                if self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
            elif self.turns[1]:
                if self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                if self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                else:
                    self.x_pos -= self.velocidade

        elif self.direction == 2:
            if self.alvo[1] < self.y_pos and self.turns[2]:
                self.y_pos -= self.velocidade
            elif not self.turns[2]:
                if self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
            elif self.turns[2]:
                self.y_pos -= self.velocidade

        elif self.direction == 3:
            if self.alvo[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.velocidade
            elif not self.turns[3]:
                if self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
            elif self.turns[3]:
                self.y_pos += self.velocidade

        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30
        return self.x_pos,self.y_pos,self.direction

    def move_nuclear(self):
        # nuclear sempre vai virar esquerda ou direita para perseguir e apenas cima ou baixo ao colidir
        if self.direction == 0:
            if self.alvo[0] > self.x_pos and self.turns[0]:
                self.x_pos += self.velocidade
            elif not self.turns[0]:
                if self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
            elif self.turns[0]:
                self.x_pos += self.velocidade

        elif self.direction == 1:
            if self.alvo[1] > self.y_pos and self.turns[3]:
                self.direction = 3
            elif self.alvo[0] < self.x_pos and self.turns[1]:
                self.x_pos -= self.velocidade
            elif not self.turns[1]:
                if self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
            elif self.turns[1]:
                self.x_pos -= self.velocidade

        elif self.direction == 2:
            if self.alvo[0] < self.x_pos and self.turns[1]:
                self.direction = 1
                self.x_pos -= self.velocidade
            elif self.alvo[1] < self.y_pos and self.turns[2]:
                self.direction = 2
                self.y_pos -= self.velocidade
            elif not self.turns[2]:
                if self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.alvo[1] > self.y_pos and self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.turns[3]:
                    self.direction = 3
                    self.y_pos += self.velocidade
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
            elif self.turns[2]:
                if self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                else:
                    self.y_pos -= self.velocidade

        elif self.direction == 3:
            if self.alvo[1] > self.y_pos and self.turns[3]:
                self.y_pos += self.velocidade
            elif not self.turns[3]:
                if self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.alvo[1] < self.y_pos and self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[2]:
                    self.direction = 2
                    self.y_pos -= self.velocidade
                elif self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                elif self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
            elif self.turns[3]:
                if self.alvo[0] > self.x_pos and self.turns[0]:
                    self.direction = 0
                    self.x_pos += self.velocidade
                elif self.alvo[0] < self.x_pos and self.turns[1]:
                    self.direction = 1
                    self.x_pos -= self.velocidade
                else:
                    self.y_pos += self.velocidade

        if self.x_pos < -30:
            self.x_pos = 900
        elif self.x_pos > 900:
            self.x_pos = -30
        return self.x_pos,self.y_pos,self.direction

def reset_positions():
    global earthPosX, earthPosY, gasX, gasY, nuclearX, nuclearY, carvaoX, carvaoY, petroleoX, petroleoY
    earthPosX=450
    earthPosY=663
    gasX=440
    gasY=388
    nuclearX=440
    nuclearY=438
    carvaoX=56
    carvaoY=58
    petroleoX=440
    petroleoY=438

    global carvao_morto, gas_morto, petroleo_morto, nuclear_morto, vidas, iniciando_partida
    carvao_morto = False
    gas_morto = False
    petroleo_morto = False
    nuclear_morto = False
    vidas-=1
    iniciando_partida=0

    global energia, reciclagem_clock, energias_rec
    energia=False
    reciclagem_clock=0
    energias_rec=[False,False,False,False]

def draw_misc():
    if energia:
        texto_pontos = font.render(f'Pontuação: {pontuacao}', True, 'blue')
    else:
        texto_pontos = font.render(f'Pontuação: {pontuacao}', True, 'white')
    screen.blit(texto_pontos,(10,920))

    for i in range(vidas):
        screen.blit(pygame.transform.scale(
            frames_earthman[3],(30,30)),
            (650+(i*40),915))
    
    if gameOver:
        pygame.draw.rect(screen,'white',[50,200,800,300],0,10)
        pygame.draw.rect(screen,'dark gray',[70,220,760,260],0,10)
        texto_derrota = font.render('Consumido pelas fontes energias não renováveis! Espaço para reiniciar!',True,'red')
        screen.blit(texto_derrota,(100,300))
    if vitoria:
        pygame.draw.rect(screen,'white',[50,200,800,300],0,10)
        pygame.draw.rect(screen,'dark gray',[70,220,760,260],0,10)
        texto_vitoria = font.render('Se tornou auto-suficiente em Energia Solar! Espaço para reiniciar!',True,'blue')
        screen.blit(texto_vitoria,(100,300))

def draw_board(lvl): #desenhando a tela do earthman
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            match lvl[i][j]:
                case 1:
                    x = i*altura_mapa+ (0.5*altura_mapa)
                    y = j*largura_mapa + (0.5*largura_mapa)
                    pygame.draw.circle(screen,'white',[y,x],4)
                case 2:
                    if not flicker:
                        x = i*altura_mapa+ (0.5*altura_mapa)
                        y = j*largura_mapa + (0.5*largura_mapa)
                        pygame.draw.circle(screen,'white',[y,x],10)
                case 3:
                    inicio_linha = [j*largura_mapa+(0.5*largura_mapa),i*altura_mapa]
                    final_linha = [j*largura_mapa+(0.5*largura_mapa),i*altura_mapa+altura_mapa]
                    pygame.draw.line(screen,level_color,
                                     inicio_linha,final_linha,3)
                case 4:
                    inicio_linha = [j*largura_mapa,i*altura_mapa+(0.5*altura_mapa)]
                    final_linha = [j*largura_mapa+largura_mapa,i*altura_mapa+(0.5*altura_mapa)]
                    pygame.draw.line(screen,level_color,
                                     inicio_linha,final_linha,3)
                case 5:
                    retangulo=[
                        (j*largura_mapa-(0.4*largura_mapa)-2),
                        (i*altura_mapa+(0.5*altura_mapa)),
                        largura_mapa,
                        altura_mapa]
                    pygame.draw.arc(screen,level_color,retangulo,0,PI/2,3)
                case 6:
                    retangulo=[
                        (j*largura_mapa+(0.5*largura_mapa)),
                        (i*altura_mapa+(0.5*altura_mapa)),
                        largura_mapa,
                        altura_mapa]
                    pygame.draw.arc(screen,level_color,retangulo,PI/2,PI,3)
                case 7:
                    retangulo=[
                        (j*largura_mapa+(0.5*largura_mapa)),
                        (i*altura_mapa-(0.4*altura_mapa)),
                        largura_mapa,
                        altura_mapa]
                    pygame.draw.arc(screen,level_color,retangulo,PI,3*PI/2,3)
                case 8:
                    retangulo=[
                        (j*largura_mapa-(0.4*largura_mapa)-2),
                        (i*altura_mapa-(0.4*altura_mapa)),
                        largura_mapa,
                        altura_mapa]
                    pygame.draw.arc(screen,level_color,retangulo,3*PI/2,0,3)
                case 9:
                    inicio_linha = [j*largura_mapa,i*altura_mapa+(0.5*altura_mapa)]
                    final_linha = [j*largura_mapa+largura_mapa,i*altura_mapa+(0.5*altura_mapa)]
                    pygame.draw.line(screen,'white',
                                     inicio_linha,final_linha,3)

def draw_player():
    match directions:
        case 0: #esquerda
            screen.blit(frames_earthman[counter//5],(earthPosX,earthPosY))
        case 1: #direita
            screen.blit(
                pygame.transform.flip(frames_earthman[counter//5],True,False),
                (earthPosX,earthPosY))
        case 2: # cima
            screen.blit(
                pygame.transform.rotate(frames_earthman[counter//5],90),
                (earthPosX,earthPosY))
        case 3: # baixo
            screen.blit(
                pygame.transform.rotate(frames_earthman[counter//5],270),
                (earthPosX,earthPosY))

def check_player_position(x:int,y:int,lvl):
    permitidoAvancar=[False,False,False,False]
    sobra = 15

    #checando colisão com certa sobra

    if x//30 < 29:
        match directions: #checando se posso retornar
            case 0:
                if lvl[y//altura_mapa][(x-sobra)//largura_mapa]<3:
                    permitidoAvancar[1]=True
            case 1:
                if lvl[y//altura_mapa][(x+sobra)//largura_mapa]<3:
                    permitidoAvancar[0]=True
            case 2:
                if lvl[(y+sobra)//altura_mapa][(x)//largura_mapa]<3:
                    permitidoAvancar[3]=True
            case 3:
                if lvl[(y-sobra)//altura_mapa][x//largura_mapa]<3:
                    permitidoAvancar[2]=True

        if directions==2 or directions==3: #andando pra cima ou pra baixo
            if 12<= x%largura_mapa<=18: #checando se posso continuar subindo ou descendo
                if level[(y+sobra)//altura_mapa][x//largura_mapa]<3:
                    permitidoAvancar[3]=True
                if level[(y-sobra)//altura_mapa][x//largura_mapa]<3:
                    permitidoAvancar[2]=True

            if 12<= y%altura_mapa<=18: #checando se posso fazer curva para esquerda ou direita
                if level[y//altura_mapa][(x-largura_mapa)//largura_mapa]<3:
                    permitidoAvancar[1]=True
                if level[y//altura_mapa][(x+largura_mapa)//largura_mapa]<3:
                    permitidoAvancar[0]=True

        if directions==0 or directions==1: #andando pra esquerda ou direita
            if 12<= x%largura_mapa<=18: #checando se posso fazer curva para cima ou baixo
                if level[(y+altura_mapa)//altura_mapa][x//largura_mapa]<3:
                    permitidoAvancar[3]=True
                if level[(y-altura_mapa)//altura_mapa][x//largura_mapa]<3:
                    permitidoAvancar[2]=True

            if 12<= y%altura_mapa<=18: #checando se posso continuar pra esquerda ou para a direita
                if level[y//altura_mapa][(x-sobra)//largura_mapa]<3:
                    permitidoAvancar[1]=True
                if level[y//altura_mapa][(x+sobra)//largura_mapa]<3:
                    permitidoAvancar[0]=True

    else:
        permitidoAvancar[0] = True
        permitidoAvancar[1] = True
    return permitidoAvancar
    
def move_player(x,y,podeAvancar):
    match directions:
        case 0:
            if podeAvancar[0]:
                x+=velocidade
        case 1:
            if podeAvancar[1]:
                x-=velocidade
        case 2:
            if podeAvancar[2]:
                y-=velocidade
        case 3:
            if podeAvancar[3]:
                y+=velocidade
    return x,y

def come_safado(x,y,pontos,energia_limpa, reciclagem_count, energias_reprimidas):
    if 0 < earthPosX < 870:
        if level[y//altura_mapa][x//largura_mapa]==1:
            level[y//altura_mapa][x//largura_mapa]=0
            pontos+=10
    if 0 < earthPosX < 870:
        if level[y//altura_mapa][x//largura_mapa]==2:
            level[y//altura_mapa][x//largura_mapa]=0
            pontos+=50
            energia_limpa=True
            reciclagem_count=0
            energias_reprimidas = [False,False,False,False]
    return pontos, energia_limpa, reciclagem_count, energias_reprimidas

def get_alvos(carvaoX,carvaoY,gasX,gasY,petroleoX,petroleoY,nuclearX,nuclearY):
    reviverPos = (380,400)
    if earthPosX<450:
        fuga_x = 900
    else:
        fuga_x = 0
    if earthPosY<450:
        fuga_y = 900
    else:
        fuga_y = 0
    if energia:
        if not carvao.morto and not energias_rec[carvao.id]:
            carvao_alvo = (fuga_x,fuga_y)
        elif not carvao.morto:
            if 340<carvaoX<560 and 340<carvaoY<500:
                carvao_alvo=(400,100)
            else:
                carvao_alvo=(earthPosX,earthPosY)
        else:
            carvao_alvo = reviverPos

        if not gas.morto and not energias_rec[gas.id]:
            gas_alvo = (fuga_x,earthPosY)
        elif not gas.morto:
            if 340<gasX<560 and 340<gasY<500:
                gas_alvo=(400,100)
            else:
                gas_alvo=(earthPosX,earthPosY)
        else:
            gas_alvo = reviverPos

        if not petroleo.morto and not energias_rec[petroleo.id]:
            petroleo_alvo = (earthPosX,fuga_y)
        elif not petroleo.morto:
            if 340<petroleoX<560 and 340<petroleoY<500:
                petroleo_alvo=(400,100)
            else:
                petroleo_alvo=(earthPosX,earthPosY)
        else:
            petroleo_alvo = reviverPos

        if not nuclear.morto and not energias_rec[nuclear.id]:
            nuclear_alvo = (earthPosY,earthPosX)
        elif not nuclear.morto:
            if 340<nuclearX<560 and 340<nuclearY<500:
                nuclear_alvo=(400,100)
            else:
                nuclear_alvo=(earthPosX,earthPosY)
        else:
            nuclear_alvo = reviverPos
    else:
        if not carvao.morto:
            if 330<carvaoX<580 and 330<carvaoY<520:
                carvao_alvo=(400,100)
            else:
                carvao_alvo=(earthPosX,earthPosY)
        else:
            carvao_alvo = reviverPos
        if not gas.morto:
            if 330<gasX<580 and 330<gasY<520:
                gas_alvo=(400,100)
            else:
                gas_alvo=(earthPosX,earthPosY)
        else:
            gas_alvo = reviverPos
        if not petroleo.morto:
            if 330<petroleoX<580 and 330<petroleoY<520:
                petroleo_alvo=(400,100)
            else:
                petroleo_alvo=(earthPosX,earthPosY)
        else:
            petroleo_alvo = reviverPos
        if not nuclear.morto:
            if 330<nuclearX<580 and 330<nuclearY<520:
                nuclear_alvo=(400,100)
            else:
                nuclear_alvo=(earthPosX,earthPosY)
        else:
            nuclear_alvo = reviverPos

    
    return [carvao_alvo, gas_alvo, petroleo_alvo, nuclear_alvo]

def game_over():
    reset_positions()
    global gameOver, iniciando_partida, movimentando
    gameOver=True
    movimentando=False
    iniciando_partida=0

def check_vitoria():
    victoria = True
    for i in range(len(level)):
        if 1 in level[i] or 2 in level[1]:
            victoria = False
    return victoria

while run:
    timer.tick(fps)

    if counter<19:
        counter+=1
        if counter>3:
            flicker = False
    else:
        counter =0
        flicker = True

    if energia and reciclagem_clock < 600:
        reciclagem_clock+=1
    elif energia:
        energia=False
        reciclagem_clock=0
        energias_rec=[False,False,False,False]

    if iniciando_partida < 180  and (not gameOver or not vitoria):
        movimentando=False
        if(gameOver or vitoria):
            iniciando_partida=0
        else:
            iniciando_partida+=1
    else:
        movimentando=True

    screen.fill('black')
    draw_board(level)

    centroX = earthPosX+23
    centroY = earthPosY+24

    eart_hitbox=pygame.draw.circle(screen,'black',(centroX,centroY),19,2)
    draw_player()

    carvao = Ghost(carvaoX,carvaoY,alvos[0],velocidade_fantasmas[0],carvao_img,
                   carvao_directions,carvao_morto,carvao_enjaulado,0)
    gas = Ghost(gasX,gasY,alvos[1],velocidade_fantasmas[1],gas_img,
                   gas_directions,gas_morto,gas_enjaulado,1)
    petroleo = Ghost(petroleoX,petroleoY,alvos[2],velocidade_fantasmas[2],petroleo_img,
                   petroleo_directions,petroleo_morto,petroleo_enjaulado,2)
    nuclear = Ghost(nuclearX,nuclearY,alvos[3],velocidade_fantasmas[3],nuclear_img,
                   nuclear_directions,nuclear_morto,nuclear_enjaulado,3)
    
    draw_misc()
    
    #checando a velocidade dos fantasmas
    if energia:
        velocidade_fantasmas=[1,1,1,1]
        if energias_rec[0]:
            velocidade_fantasmas[0]=2
        if energias_rec[1]:
            velocidade_fantasmas[1]=2
        if energias_rec[2]:
            velocidade_fantasmas[2]=2
        if energias_rec[3]:
            velocidade_fantasmas[3]=2
    else:
        velocidade_fantasmas=[2,2,2,2]
    if carvao.morto:
        velocidade_fantasmas[0]=4
    if gas.morto:
        velocidade_fantasmas[1]=4
    if petroleo.morto:
        velocidade_fantasmas[2]=4
    if nuclear.morto:
        velocidade_fantasmas[3]=4
    
    alvos = get_alvos(
        carvaoX,carvaoY,
        gasX,gasY,
        petroleoX,petroleoY,
        nuclearX,nuclearY
    )

    permitidoAvancar = check_player_position(centroX,centroY,level)

    if movimentando:
        earthPosX,earthPosY= move_player(earthPosX,earthPosY,permitidoAvancar)
        petroleoX, petroleoY, petroleo_directions= petroleo.move_petroleo()

        if not carvao_morto and not carvao.enjaulado:
            carvaoX, carvaoY, carvao_directions= carvao.move_carvao()
        else:
            carvaoX, carvaoY, carvao_directions= carvao.move_petroleo()

        if not gas_morto and not gas.enjaulado:
            gasX, gasY, gas_directions= gas.move_gas()
        else:
            gasX, gasY, gas_directions= gas.move_petroleo()

        if not nuclear_morto and not nuclear.enjaulado:
            nuclearX, nuclearY, nuclear_directions= nuclear.move_nuclear()
        else:
            nuclearX, nuclearY, nuclear_directions= nuclear.move_petroleo()

    pontuacao, energia, reciclagem_clock, energias_rec = come_safado(centroX,centroY,pontuacao, energia, reciclagem_clock, energias_rec)
    vitoria = check_vitoria()
    #checando colisão com os fantasmas
    if not energia:
        if  (eart_hitbox.colliderect(petroleo.retan) and not petroleo.morto) or \
            (eart_hitbox.colliderect(gas.retan) and not gas.morto) or \
            (eart_hitbox.colliderect(carvao.retan) and not carvao.morto) or \
            (eart_hitbox.colliderect(nuclear.retan) and not nuclear.morto):
            reset_positions()
            if vidas<0:
                game_over()
    elif energia and eart_hitbox.colliderect(carvao.retan) and not carvao.morto and not energias_rec[0]:
        carvao_morto=True
        energias_rec[0] = True
        pontuacao+=(2**energias_rec.count(True))*100
    elif energia and eart_hitbox.colliderect(gas.retan) and not gas.morto and not energias_rec[1]:
        gas_morto=True
        energias_rec[1] = True
        pontuacao+=(2**energias_rec.count(True))*100
    elif energia and eart_hitbox.colliderect(petroleo.retan) and not petroleo.morto and not energias_rec[2]:
        petroleo_morto=True
        energias_rec[2] = True
        pontuacao+=(2**energias_rec.count(True))*100
    elif energia and eart_hitbox.colliderect(nuclear.retan) and not nuclear.morto and not energias_rec[3]:
        nuclear_morto=True
        energias_rec[3] = True
        pontuacao+=(2**energias_rec.count(True))*100

    elif energia and eart_hitbox.colliderect(carvao.retan) and not carvao.morto and energias_rec[0]:
        reset_positions()
        if vidas<0:
            game_over()
    elif energia and eart_hitbox.colliderect(gas.retan) and not gas.morto and energias_rec[1]:
        reset_positions()
        if vidas<0:
            game_over()
    elif energia and eart_hitbox.colliderect(petroleo.retan) and not petroleo.morto and energias_rec[2]:
        reset_positions()
        if vidas<0:
            game_over()
    elif energia and eart_hitbox.colliderect(nuclear.retan) and not nuclear.morto and energias_rec[3]:
        reset_positions()
        if vidas<0:
            game_over()  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT:
                direction_command=0
            if event.key==pygame.K_LEFT:
                direction_command=1
            if event.key==pygame.K_UP:
                direction_command=2
            if event.key==pygame.K_DOWN:
                direction_command=3
            if event.key==pygame.K_SPACE and (gameOver or vitoria):
                vidas=3
                pontos=0
                level = copy.deepcopy(boards)
                reset_positions()
                gameOver = False
                vitoria = False
            if event.key==pygame.K_ESCAPE:
                run = False

        if event.type==pygame.KEYUP:
            if event.key==pygame.K_RIGHT and direction_command==0:
                direction_command=directions
            if event.key==pygame.K_LEFT and direction_command==1:
                direction_command=1
            if event.key==pygame.K_UP and direction_command==2:
                direction_command=2
            if event.key==pygame.K_DOWN and direction_command==3:
                direction_command=3

    for i in range(4):
        if direction_command == i and permitidoAvancar[i]:
            directions=i

    if earthPosX>900:
        earthPosX=-47
    elif earthPosX<-50:
        earthPosX=897

    #ressuscitando os mortos
    if petroleo.enjaulado and petroleo.morto:
        petroleo_morto=False
    if gas.enjaulado and gas.morto:
        gas_morto=False
    if nuclear.enjaulado and nuclear.morto:
        nuclear_morto=False
    if carvao.enjaulado and carvao.morto:
        carvao_morto=False

    pygame.display.flip()

pygame.quit()