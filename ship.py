import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_settings,screen):
        super(Ship,self).__init__()
        self.screen=screen
        self.ai_settings=ai_settings

        self.image=pygame.image.load("ship.gif")
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()

        #将每艘飞船置于底部中心
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom

        #在飞船的属性center中存储小数值
        self.center=float(self.rect.centerx)
       
        #移动标志
        self.moving_right=False
        self.moving_left=False

    def update(self):
        if self.moving_right and self.rect.right<self.screen_rect.right:
            self.center+=self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left>0:
            self.center-=self.ai_settings.ship_speed_factor

        #根据self.center更新rect对象
        self.rect.centerx=self.center
        
    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def center_ship(self):
        self.center=self.screen_rect.centerx

