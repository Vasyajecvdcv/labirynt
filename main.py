import pygame
import random
win_width=1200
win_height=700
FPS = pygame.time.Clock()

window=pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("Лабіринт")
game = True
finish=False
class Settings:
    def __init__(self,image,x,y,w,h):
        self.image=pygame.transform.scale(pygame.image.load(image),(w,h))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.direction=True
        self.image_right=self.image
        self.image_left=pygame.transform.flip(self.image,True,False)


    def draw(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(Settings):
    def __init__(self,image,x,y,w,h,s):
        super().__init__(image,x,y,w,h)
        self.speed=s


    def move(self):
        keys=pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y>0:
            self.rect.y-=self.speed
        if keys[pygame.K_DOWN] and self.rect.y<win_height-self.rect.height:
            self.rect.y+=self.speed
        if keys[pygame.K_LEFT] and self.rect.x>0:
            self.rect.x-=self.speed
            self.direction=False
        if keys[pygame.K_RIGHT] and self.rect.x<win_width-self.rect.width:
            self.rect.x+=self.speed
            self.direction=True
        if self.direction:
            self.image=self.image_right
        else:
            self.image=self.image_left

class Enemy(Player):
    def __init__(self,image,x,y,w,h,s):
        super().__init__(image,x,y,w,h,s)

    def move(self,x1,x2):
        if self.rect.x>x2:
            self.direction=False

        if self.rect.x<x1:
            self.direction=True
        
        if self.direction==True:
            self.image=self.image_right
            self.rect.x+=self.speed

        if self.direction==False:
            self.rect.x-=self.speed
            self.image=self.image_left

class Wall:
    def __init__(self,x,y,w,h,color):
        self.rect=pygame.Rect(x,y,w,h)
        self.color=color
    def draw(self):
        pygame.draw.rect(window,self.color,self.rect)

class Text:
    def __init__(self,x,y,text,size,color):
        self.x=x
        self.y=y
        self.text=text
        self.size=size
        self.color=color

    def set_text(self):
        self.txt=pygame.font.SysFont("verdana",self.size).render(self.text,True,self.color)
    def draw(self):
        self.set_text()
        window.blit(self.txt,(self.x,self.y))

class Button:
    def __init__(self,x,y,w,h,t_color,color):
        self.rect=pygame.Rect(x,y,w,h)
        self.t_color=t_color
        self.color=color

    def set_text(self,size,text):
        self.txt=pygame.font.SysFont("verdana",size).render(text,True,self.t_color)
    def draw(self,_x,_y):
        pygame.draw.rect(window,self.color,self.rect)
        pygame.draw.rect(window,(0,0,0),self.rect,width=4)
        window.blit(self.txt,(self.rect.x+_x,self.rect.y+_y))





reset=Button(win_width//2.5,win_height-200,250,150,(0,0,0),"grey")
zoloto=Settings("gold.png",win_width-150,win_height-200,100,100)
enemy=Enemy("enemy.png",600,win_height//2,100,100,8)        
player=Player("hero.png",0,10,100,100,10)
fon=Settings("fon.png",0,0,win_width,win_height)
pygame.font.init()
win=Text(win_width//7,win_height//3,"You win", 150,"green")
lose=Text(win_width//7,win_height//3,"Loser", 150,"red")
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)

walls=[
    Wall(206,70,10,400,(random.randint(0,255),random.randint(0,255),random.randint(0,255))),
    Wall(206,70,600,10,(random.randint(0,255),random.randint(0,255),random.randint(0,255))),
    Wall(206,470,600,10,(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
]

while game:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game=False
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            x,y=event.pos
            if reset.rect.collidepoint(x,y):
                finish=False
                player.rect.x=0
                player.rect.y=10
    if finish!= True:
        enemy.draw()
        enemy.move(600,win_width-enemy.rect.width)
        fon.draw()
        for w in walls:
            if player.rect.colliderect(w.rect):
                player.rect.x=0
                player.rect.y=10
            w.draw()
        player.draw()
        player.move()
        enemy.draw()
        enemy.move(600,win_width-enemy.rect.width)
        zoloto.draw()
        if player.rect.colliderect(enemy.rect):
            fon.draw()
            lose.draw()
            reset.set_text(30,"Again")
            reset.draw(50,50)
            finish=True
        if player.rect.colliderect(zoloto.rect):
            fon.draw()
            win.draw()
            finish=True
    pygame.display.flip()
    FPS.tick(60)
