import sys,pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y=pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)
            
def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)
    
    if button_clicked and not stats.game_active:
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active=True

        #重置积分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()


        
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并让飞船居中
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()



        
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_RIGHT:
            ship.moving_right=True
        elif event.key==pygame.K_LEFT:
            ship.moving_left=True
        elif event.key==pygame.K_SPACE:
            #创建一颗子弹，并将其加入到编组bullets中
            #限制子弹数目
            fire_bullet(ai_settings,screen,ship,bullets)
        elif event.key==pygame.K_q:
            sys.exit()
            
def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets)<ai_settings.bullets_allowed:
        new_bullet=Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)
            
            

def check_keyup_events(event,ship):
    if event.type==pygame.KEYUP:
        if event.key==pygame.K_RIGHT:
            ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            ship.moving_left=False
                

        
def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,play_button):
    screen.fill(ai_settings.bg_color)
    #在飞创和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    #如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    #更新子弹的位置
    bullets.update()
    #删除已消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom<=0:
            bullets.remove(bullet)

    check_bullets_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_bullets_alien_collisions(ai_settings,screen,stats,sb,ship,aliens,bullets):
    
    #检查是否有子弹击中了外星人
    #如果击中，就删除相应的子弹和外星人
    collisions=pygame.sprite.groupcollide(bullets,aliens,True,True)
    if len(aliens)==0:
        #删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        #提高等级
        stats.level+=1
        sb.prep_level()
        creat_fleet(ai_settings,screen,ship,aliens)
        
    if collisions:
        for aliens in collisions.values():
            stats.score+=ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats,sb)
    

def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets):
    #响应被外星人撞到的飞船
    if stats.ships_left>0:
        stats.ships_left-=1

        #更新计分牌
        sb.prep_ships()
        
        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        #创建一群新的外星人，并将飞船放到屏幕的底端中央
        creat_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #暂停
        sleep(0.5)
    else:
        stats.game_active=False
        pygame.mouse.set_visible(True)
    

def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
    #检查是否有外星人碰到屏幕底端
    screen_rect=screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom>=screen_rect.bottom:
            ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
            break
            
def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
    check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)



def get_number_aliens_x(ai_settings,alien_width):
    available_space_x=ai_settings.screen_width-3*alien_width
    number_aliens_x=int(available_space_x/(3*alien_width))
    return number_aliens_x

def creat_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien=Alien(ai_settings,screen)
    alien_width=alien.rect.width
    alien.x=2*alien_width+3*alien_width*alien_number
    alien.rect.x=alien.x
    alien.rect.y=2*alien.rect.height+2*alien.rect.height*row_number
    aliens.add(alien)

    
def creat_fleet(ai_settings,screen,ship,aliens):
    alien=Alien(ai_settings,screen)
    number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            creat_alien(ai_settings,screen,aliens,alien_number,row_number)

def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y=(ai_settings.screen_height-(3*alien_height)-ship_height)
    number_rows=int(available_space_y/(3*alien_height))
    return number_rows

def check_fleet_edges(ai_settings,aliens):
    #有外星人到达边缘采取相应的措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break
def change_fleet_direction(ai_settings,aliens):
    #将郑群外星人下移，并改变他们的方向
    for alien in aliens.sprites():
        alien.rect.y+=ai_settings.fleet_drop_speed
    ai_settings.fleet_direction*=-1

def check_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score=stats.score
        sb.prep_high_score()
