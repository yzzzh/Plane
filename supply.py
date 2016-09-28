'''
供给：超级子弹和炸弹
属性：图片，位置，速度
方法：移动，重置
'''

import pygame as pg
from random import *

class Bullet_Supply(pg.sprite.Sprite):
    def __init__(self,bg_size):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\ufo1.png')
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size
        self.rect.left,self.rect.bottom = randint(0,self.width - self.rect.width),-50
        self.speed = 5
        self.mask = pg.mask.from_surface(self.image)
        self.active = False

    def move(self):
        if self.rect.top > self.height:
            self.active = False
        else:
            self.rect.bottom += self.speed

    def reset(self):
        self.rect.left,self.rect.bottom = randint(0,self.width - self.rect.width),-50
        self.active = True

class Bomb_Supply(pg.sprite.Sprite):
    def __init__(self,bg_size):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\ufo2.png')
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size
        self.rect.left,self.rect.bottom = randint(0,self.width - self.rect.width),-50
        self.speed = 5
        self.mask = pg.mask.from_surface(self.image)
        self.active = False

    def move(self):
        if self.rect.top > self.height:
            self.active = False
        else:
            self.rect.bottom += self.speed

    def reset(self):
        self.rect.left,self.rect.bottom = randint(0,self.width - self.rect.width),-50
        self.active = True