import pygame

win_width=1200
win_height=700
FPS = pygame.time.Clock()

window=pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("Лабіринт")
game = True
class Settings:
    def __init__(self,image,x,y,w,h):
        self.image=pygame.transform.scale(pygame.image.load(image),(w,h))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.direction=True
        self.image_right=self.image
        self.image_left=pygame.transform.flip(self.image,(True,False))


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


player=Player("hero.png",0,10,100,100,10)
fon=Settings("fon.png",0,0,win_width,win_height)
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)
while game:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            game=False

    fon.draw()
    player.draw()
    player.move()
    pygame.display.flip()
    FPS.tick(60)

