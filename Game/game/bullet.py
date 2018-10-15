#子弹
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        #加载子弹图片  /feiji/a.png
        self.image = pygame.image.load('Game/game/images/bullet01.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.left,self.rect.top = position

        #子弹速度与射程
        self.speed = 17

        self.active = False
        #检测是否碰撞
        self.mask = pygame.mask.from_surface(self.image)
    
    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0 :
            self.active = False
        
    def reset(self,position):
        #定义子弹离玩家飞机的位置
        self.rect.left, self.rect.top = position
        self.rect.left -= 3
        self.rect.top -= 10
        self.active = True


#双发子弹
class Bullet1(pygame.sprite.Sprite):
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)

        #加载子弹图片  /feiji/a.png
        self.image = pygame.image.load('Game/game/images/bullet02.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.left,self.rect.top = position

        #子弹速度与射程
        self.speed = 19

        self.active = False
        #检测是否碰撞
        self.mask = pygame.mask.from_surface(self.image)
    
    def move(self):
        self.rect.top -= self.speed

        if self.rect.top < 0 :
            self.active = False
        
    def reset(self,position):
        #定义子弹离玩家飞机的位置
        self.rect.left, self.rect.top = position
        self.rect.left -= 3
        self.rect.top -= 10
        self.active = True