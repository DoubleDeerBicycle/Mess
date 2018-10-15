#创建敌机

import pygame
from random import *

#小型敌机
class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        #敌机图片/feiji/a.png
        self.image = pygame.image.load('Game/game/images/enemy1.png').convert_alpha()
        
        #加载飞机坠毁图片
        self.destroy_images = []
        self.destroy_images.extend(
            [
                pygame.image.load('Game/game/images/enemy1_down1.png').convert_alpha(),
                pygame.image.load('Game/game/images/enemy1_down2.png').convert_alpha(),
                pygame.image.load('Game/game/images/enemy1_down3.png').convert_alpha(),
                pygame.image.load('Game/game/images/enemy1_down4.png').convert_alpha()
            ]
        )
        #获取敌机图片尺寸
        self.rect = self.image.get_rect()

        #背景宽高
        self.width,self.height = bg_size[0],bg_size[1]

        #敌机速度
        self.speed = 3

        #定义标记，用来检查飞机是否被毁灭
        self.active = True

        #定义碰撞检测算法
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width), randint(-5 * self.height,0)
        
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    
    def reset(self):
        self.active = True
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-5 * self.height,0)

#中型敌机
class MidEnemy(pygame.sprite.Sprite):
    #敌机血量
    energy = 8
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        #敌机图片
        self.image = pygame.image.load('Game/game/images/enemy2.png').convert_alpha()
        
        #敌机被击中时的图片
        self.image_hit = pygame.image.load('Game/game/images/enemy2_hit.png').convert_alpha()
        
        #加载飞机坠毁图片
        self.destroy_images = []
        self.destroy_images.extend(
            [
                pygame.image.load('Game/game/images/enemy2_down1.png').convert_alpha(),
                pygame.image.load('Game/game/images/enemy2_down2.png').convert_alpha(),
                pygame.image.load('Game/game/images/enemy2_down3.png').convert_alpha(),
                pygame.image.load('Game/game/images/enemy2_down4.png').convert_alpha()
            ]
        )

        #获取敌机图片尺寸
        self.rect = self.image.get_rect()

        #背景宽高
        self.width,self.height = bg_size[0],bg_size[1]

        #敌机速度
        self.speed = 2
        
        #定义标记，用来检查飞机是否被毁灭
        self.active = True
        
        #定义碰撞检测算法
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width), randint(-10 * self.height,-self.height)
        
        self.energy = MidEnemy.energy
        
        self.hit = False
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    
    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-10 * self.height,-self.height)


#大型敌机
class MaxEnemy(pygame.sprite.Sprite):
    #敌机血量
    energy = 20
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        #敌机图片
        self.image = pygame.image.load('Game/game/images/enemy3_n1.png').convert_alpha()
        self.image1 = pygame.image.load('Game/game/images/enemy3_n2.png').convert_alpha()
        
        #敌机被击中时的图片
        self.image_hit = pygame.image.load('Game/game/images/enemy3_hit.png').convert_alpha()

        #加载飞机坠毁图片
        self.destroy_images = []
        self.destroy_images.extend(
            [
                pygame.image.load('Game/game/images/enemy3_down1.png').convert_alpha(),
                pygame.image.load('Game/game/images/enemy3_down2.png').convert_alpha(),
                pygame.image.load('Game/game/images/enemy3_down3.png').convert_alpha(),
                pygame.image.load('Game/game/images/enemy3_down4.png').convert_alpha(),
                pygame.image.load('Game/game/images/enemy3_down5.png').convert_alpha(),
                pygame.image.load('Game/game/images/enemy3_down6.png').convert_alpha()
            ]
        )

        #获取敌机图片尺寸
        self.rect = self.image.get_rect()

        #背景宽高
        self.width,self.height = bg_size[0],bg_size[1]

        #敌机速度
        self.speed = 1

        #定义标记，用来检查飞机是否被毁灭
        self.active = True

        #定义碰撞检测算法
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width), randint(-15 * self.height,-5 * self.height)

        self.energy = MaxEnemy.energy

        self.hit = False
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()
    
    def reset(self):
        self.active = True
        self.energy = MaxEnemy.energy
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-15 * self.height,-5 * self.height)