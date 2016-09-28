'''
大型机，中型机，小型机
属性：
图片，位置，速度,能量
方法：
移动
'''

import pygame as pg
from random import *

class smallEnemy(pg.sprite.Sprite):
    def __init__(self,bg_size):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy1.png').convert_alpha()
        #被破坏时的图片
        self.destory_images = []
        self.destory_images.extend(
            [
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy1_down1.png').convert_alpha(),
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy1_down2.png').convert_alpha(),
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy1_down3.png').convert_alpha(),
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy1_down4.png').convert_alpha()
            ]
        )
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size
        self.speed = 3
        #位于地图外的位置生成
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-5 * self.height,0)
        self.active = True
        self.mask = pg.mask.from_surface(self.image)

    #重新生成一架飞机
    def reset(self):
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-5*self.height,0)
        self.active = True

    def move(self):
        if self.rect.top > self.height:
            #越过地图，重新生成
            self.reset()
        else:
            self.rect.top += self.speed

class midEnemy(pg.sprite.Sprite):
    energy = 4

    def __init__(self,bg_size):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy2.png').convert_alpha()
        #被击中时的图片
        self.image_hit = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy2_hit.png').convert_alpha()
        #被破坏时的图片
        self.destory_images = []
        self.destory_images.extend(
            [
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy2_down1.png').convert_alpha(),
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy2_down2.png').convert_alpha(),
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy2_down3.png').convert_alpha(),
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy2_down4.png').convert_alpha()
            ]
        )
        self.rect = self.image.get_rect()
        self.width,self.height = bg_size
        self.speed = 2
        #位于地图外的位置生成
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-10*self.height,0)
        self.active = True
        self.mask = pg.mask.from_surface(self.image)
        self.energy = midEnemy.energy
        self.hit = False

    #重新生成一架飞机
    def reset(self):
        self.rect.left,self.rect.top = randint(0,self.width - self.rect.width),randint(-10*self.height,0)
        self.energy = midEnemy.energy
        self.active = True

    def move(self):
        if self.rect.top > self.height:
            #越过地图，重新生成
            self.reset()
        else:
            self.rect.top += self.speed


class bigEnemy(pg.sprite.Sprite):
    energy = 8

    def __init__(self,bg_size):
        pg.sprite.Sprite.__init__(self)
        self.image1 = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy3_n1.png').convert_alpha()
        self.image2 = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy3_n2.png').convert_alpha()
        #被击中时的图片
        self.image_hit = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy3_hit.png').convert_alpha()
        #被破坏时的图片
        self.destory_images = []
        self.destory_images.extend(
            [
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy3_down1.png').convert_alpha(),
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy3_down2.png').convert_alpha(),
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy3_down3.png').convert_alpha(),
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy3_down4.png').convert_alpha(),
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy3_down5.png').convert_alpha(),
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\enemy3_down6.png').convert_alpha()
            ]
        )
        self.rect = self.image1.get_rect()
        self.width,self.height = bg_size
        self.speed = 1
        #位于地图外的位置生成
        self.rect.left,self.rect.bottom = randint(0,self.width - self.rect.width),randint(-15*self.height,0)
        self.active = True
        self.mask = pg.mask.from_surface(self.image1)
        self.energy = bigEnemy.energy
        self.hit = False

    #重新生成一架飞机
    def reset(self):
        self.rect.left,self.rect.bottom = randint(0,self.width - self.rect.width),randint(-15*self.height,0)
        self.energy = bigEnemy.energy
        self.active = True

    def move(self):
        if self.rect.top > self.height:
            #越过地图，重新生成
            self.reset()
        else:
            self.rect.top += self.speed
