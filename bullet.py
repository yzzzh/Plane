'''
子弹类：
属性：图片，速度，位置
方法：移动，重置
'''

import pygame as pg

class Bullet1(pg.sprite.Sprite):
    def __init__(self,pos):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\bullet1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = pos
        self.speed = 15
        self.mask = pg.mask.from_surface(self.image)
        self.active = True

    def move(self):
        #超出界外，子弹消失
        if self.rect.bottom <= 0:
            self.active = False
        else:
            self.rect.top -= self.speed

    def reset(self,pos):
        self.active = True
        self.rect.left,self.rect.top = pos

#超级子弹
class Bullet2(pg.sprite.Sprite):
    def __init__(self,pos):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\bullet2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = pos
        self.speed = 20
        self.mask = pg.mask.from_surface(self.image)
        self.active = True

    def move(self):
        #超出界外，子弹消失
        if self.rect.bottom <= 0:
            self.active = False
        else:
            self.rect.top -= self.speed

    def reset(self,pos):
        self.active = True
        self.rect.left,self.rect.top = pos