#我方飞机

import pygame


#我方飞机类，继承pygame.sprite.Sprite用以检测碰撞
class MyPlane(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        #加载飞机图片
        self.image = pygame.image.load('Game/game/images/me1.png').convert_alpha()
        self.image1 = pygame.image.load('Game/game/images/me2.png').convert_alpha()        
        
        #加载飞机坠毁图片
        self.destroy_images = []
        self.destroy_images.extend(
            [
                pygame.image.load('Game/game/images/me_destroy_1.png').convert_alpha(),
                pygame.image.load('Game/game/images/me_destroy_2.png').convert_alpha(),
                pygame.image.load('Game/game/images/me_destroy_3.png').convert_alpha(),
                pygame.image.load('Game/game/images/me_destroy_4.png').convert_alpha()
            ]
        )
       
        #获取飞机图片尺寸
        self.rect = self.image.get_rect()

        #获取背景图片的宽和高
        self.width,self.height = bg_size[0],bg_size[1]

        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, self.height - self.rect.height - 60

        #我方飞机速度
        self.speed = 7

        #定义标记，用来检查飞机是否被毁灭
        self.active = True

        #无敌
        self.invincible = False

        #定义碰撞检测算法
        self.mask = pygame.mask.from_surface(self.image)
    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < self.height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 60

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width
    
    def reset(self):
        self.rect.left, self.rect.top = (self.width - self.rect.width) // 2, self.height - self.rect.height - 60
        self.active = True
        self.invincible = True