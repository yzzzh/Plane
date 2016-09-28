'''
plane类
包含：
属性：
图片
位置
屏幕大小
速度
方法：
移动
'''

import pygame as pg

class myPlane(pg.sprite.Sprite):
    def __init__(self,image1,image2,bg_size):
        pg.sprite.Sprite.__init__(self)
        #正常飞行的图片
        self.image1 = pg.image.load(image1).convert_alpha()
        self.image2 = pg.image.load(image2).convert_alpha()
        #被破坏时的图片
        self.destory_images = []
        self.destory_images.extend(
            [
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\hero_blowup_n1.png').convert_alpha(),
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\hero_blowup_n2.png').convert_alpha(),
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\hero_blowup_n3.png').convert_alpha(),
            pg.image.load(r'D:\python_code\pygame\plane\image\shoot\hero_blowup_n4.png').convert_alpha()
            ]
        )
        self.bg_width,self.bg_height = bg_size
        self.rect = self.image1.get_rect()
        self.rect.left,self.rect.top = (self.bg_width - self.rect.width) // 2,self.bg_height - self.rect.height - 60
        self.speed = 10
        #检测是否被破坏
        self.active = True
        #将图片非透明的部分标记为mask
        self.mask = pg.mask.from_surface(self.image1)
        #无敌状态
        self.invincible = False

    def reset(self):
        self.active = True
        self.invincible = True
        self.rect.left,self.rect.top = (self.bg_width - self.rect.width) // 2,self.bg_height - self.rect.height - 60

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < self.bg_height:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = self.bg_height

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.bg_width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.bg_width

