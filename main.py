import pygame as pg
from pygame.locals import *
import sys
import traceback
import myPlane
import enemy
import bullet
import  supply
import os
from random import *
#添加敌机
def add_small_enemies(group1,group2,num,bg_size):
    for each in range(num):
        e1 = enemy.smallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1,group2,num,bg_size):
    for each in range(num):
        e1 = enemy.midEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_big_enemies(group1,group2,num,bg_size):
    for each in range(num):
        e1 = enemy.bigEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

#重启程序
def restart_program():
  python = sys.executable
  os.execl(python, python, * sys.argv)

#加速
def speed_inc(target,speed):
    target.speed += speed

def main():
    #初始化
    pg.init()
    pg.mixer.init()
    #载入屏幕
    bg_size = width,height = 400,680
    screen = pg.display.set_mode(bg_size)
    pg.display.set_caption('飞机大战')
    #颜色
    BLACK = (0,0,0)
    GREEN = (0,255,0)
    RED = (255,0,0)
    WHITE = (255,255,255)
    #载入背景
    background = pg.image.load(r'image\shoot_background\background.png')
    #载入音乐
    #背景音乐
    pg.mixer.music.load(r'sound\game_music.mp3')
    pg.mixer.music.play(-1)
    #音效
    bullet_sound = pg.mixer.Sound(r'sound\bullet.wav')
    bomb_sound = pg.mixer.Sound(r'sound\bomb.wav')
    supply_sound = pg.mixer.Sound(r'sound\supply.wav')
    get_bomb_sound = pg.mixer.Sound(r'sound\getBomb.wav')
    get_bullet_sound = pg.mixer.Sound(r'sound\getBullet.wav')
    upgrade_sound = pg.mixer.Sound(r'sound\upgrade.wav')
    enemy3_fly_sound = pg.mixer.Sound(r'sound\enemy1_fly.wav')
    enemy1_down_sound = pg.mixer.Sound(r'sound\enemy1_down.wav')
    enemy2_down_sound = pg.mixer.Sound(r'sound\enemy2_down.wav')
    enemy3_down_sound = pg.mixer.Sound(r'sound\enemy3_down.wav')
    me_down_sound = pg.mixer.Sound(r'sound\me_down.wav')

    #暂停按钮
    pause_nor = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\game_pause_nor.png').convert_alpha()
    pause_pressed = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\game_pause_pressed.png').convert_alpha()
    resume_nor = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\game_resume_nor.png').convert_alpha()
    resume_pressed = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\game_resume_pressed.png').convert_alpha()
    pause_rect = pause_nor.get_rect()
    pause_rect.left,pause_rect.top = width - pause_rect.width - 10 ,10
    pause_image = pause_nor

    #暂停键
    pause = False

    #是否将数据写入
    is_record = False

    #游戏结束的画面
    again_image = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\game_again.png').convert_alpha()
    again_rect = again_image.get_rect()
    again_rect.left,again_rect.top = 50,400
    continue_image = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\game_continue.png').convert_alpha()
    continue_rect = continue_image.get_rect()
    continue_rect.left,continue_rect.top = 50,450
    quit_image = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\game_over.png').convert_alpha()
    quit_rect = quit_image.get_rect()
    quit_rect.left,quit_rect.top = 50,500
    my_score_font = pg.font.Font(r'D:\python_code\pygame\plane\font\myfont.ttf',40)
    best_score_font = pg.font.Font(r'D:\python_code\pygame\plane\font\myfont.ttf',40)

    #全屏炸弹,放在右下角
    bomb_num = 3
    bomb_image = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_rect.left,bomb_rect.top = 10,height - bomb_rect.height - 10
    bomb_font = pg.font.Font(r'D:\python_code\pygame\plane\font\myfont.ttf',38)
    bomb_num_text = bomb_font.render(' X %d'%bomb_num,True,BLACK)
    bomb_num_rect = bomb_num_text.get_rect()
    bomb_num_rect.left,bomb_num_rect.top = bomb_rect.width + 20,height - bomb_num_rect.height - 20

    #补给
    bomb_supply = supply.Bomb_Supply(bg_size)
    bullet_supply = supply.Bullet_Supply(bg_size)

    #自定义补给事件，每30秒触发一次
    SUPPLY_TIMER = USEREVENT
    pg.time.set_timer(SUPPLY_TIMER,30 * 1000)

    #生命值
    life_image = pg.image.load(r'D:\python_code\pygame\plane\image\shoot\plane.png').convert_alpha()
    life_num = 3
    life_rect = life_image.get_rect()

    running = True

    #初始化我方飞机
    myPlane_image1 = r'D:\python_code\pygame\plane\image\shoot\hero1.png'
    myPlane_image2 = r'D:\python_code\pygame\plane\image\shoot\hero2.png'
    my_plane = myPlane.myPlane(myPlane_image1,myPlane_image2,bg_size)

    #初始化敌方飞机
    enemies = pg.sprite.Group()

    small_enemies = pg.sprite.Group()
    add_small_enemies(small_enemies,enemies,15,bg_size)

    mid_enemies = pg.sprite.Group()
    add_mid_enemies(mid_enemies,enemies,10,bg_size)

    big_enemies = pg.sprite.Group()
    add_big_enemies(big_enemies,enemies,5,bg_size)

    #检索破坏时的图片，以便切换
    small_destory_images_index = 0
    mid_destory_images_index = 0
    big_destory_images_index = 0
    me_destory_images_index = 0

    #难度等级
    level = 1
    level_font = pg.font.Font(r'D:\python_code\pygame\plane\font\myfont.ttf',38)
    level_text = level_font.render('Level : %d'%level,True,BLACK)
    level_rect = level_text.get_rect()
    level_rect.left,level_rect.top = width - level_rect.width - 5,height - level_rect.height - 20

    #无敌状态
    INVINCIBLE = USEREVENT + 2

    #初始化子弹
    #普通子弹
    bullets = []
    bullets1 = []
    BULLET1_NUM = 8
    bullet1_index = 0
    #超级子弹
    bullets2 = []
    BULLET2_NUM = 16
    bullet2_index = 0
    is_double_bullet = False
    for i in range(BULLET2_NUM // 2):
        #一组子弹
        bullets2.append(bullet.Bullet2((my_plane.rect.centerx-33,my_plane.rect.centery)))
        bullets2.append(bullet.Bullet2((my_plane.rect.centerx+30,my_plane.rect.centery)))

    for i in range(BULLET1_NUM):
        bullets1.append(bullet.Bullet1(my_plane.rect.center))

    #超级子弹使用时间，一次20秒
    DOUBLE_BULLET_STOP = USEREVENT + 1

    #计分器
    score_font = pg.font.Font(r'D:\python_code\pygame\plane\font\myfont.ttf',36)
    score = 0

    #两种状态的切换
    is_switch = False

    #延迟变量
    delay = 100

    #时钟
    clock = pg.time.Clock()

    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                #按下重来键
                if event.button == 1 and again_rect.collidepoint(event.pos) and life_num == 0:
                    restart_program()
                #继续键
                if event.button == 1 and continue_rect.collidepoint(event.pos) and life_num == 0:
                    #重新赋予3次生命
                    life_num = 3
                    pg.mixer.unpause()
                    pg.mixer.music.unpause()
                    pg.time.set_timer(SUPPLY_TIMER,30 * 1000)
                    is_record = True
                #结束键
                if event.button == 1 and quit_rect.collidepoint(event.pos) and life_num == 0:
                    pg.quit()
                    sys.exit()
                    #移动到暂停按钮上并点击
                if event.button == 1 and pause_rect.collidepoint(event.pos) and life_num != 0:
                    pause = not pause
                    #暂停，停止各种音乐
                    if pause:
                        pg.time.set_timer(SUPPLY_TIMER,0)
                        pg.mixer.pause()
                        pg.mixer.music.pause()
                    else:
                        pg.time.set_timer(SUPPLY_TIMER,30 * 1000)
                        pg.mixer.unpause()
                        pg.mixer.music.unpause()
                #各种暂停图片的切换
            elif event.type == MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    if pause:
                        pause_image = resume_pressed
                    else:
                        pause_image = pause_pressed
                else:
                    if pause:
                        pause_image = resume_nor
                    else:
                        pause_image = pause_nor
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num >= 1:
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
                        bomb_num -= 1
            #投放补给
            elif event.type == SUPPLY_TIMER:
                supply_sound.play()
                if False:
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            #超级子弹计时器
            elif event.type == DOUBLE_BULLET_STOP:
                is_double_bullet = False
                pg.time.set_timer(DOUBLE_BULLET_STOP,0)

            #无敌状态到时间
            elif event.type == INVINCIBLE:
                my_plane.invincible = False
                pg.time.set_timer(INVINCIBLE,0)




        #绘制背景
        screen.blit(background,(0,0))

        #难度设置:
        # 1w以下：1级
        # 1w~5w：2级
        # 5w~20w：3级
        # 20w~50w：4级
        # 50w+：5级
        #每升一级，增加3部小型机，2部中型机，1部大型机,并相应地增加速度
        if score < 10000:
            level = 1

        if level == 1 and score >= 10000:
            upgrade_sound.play()

            level = 2

            add_big_enemies(big_enemies,enemies,2,bg_size)
            add_mid_enemies(mid_enemies,enemies,4,bg_size)
            add_small_enemies(small_enemies,enemies,6,bg_size)

            for each in small_enemies:
                speed_inc(each,1)

        if level == 2 and score >= 50000:
            upgrade_sound.play()

            level = 3

            add_big_enemies(big_enemies,enemies,2,bg_size)
            add_mid_enemies(mid_enemies,enemies,4,bg_size)
            add_small_enemies(small_enemies,enemies,6,bg_size)

            for each in small_enemies:
                speed_inc(each,1)
            for each in mid_enemies:
                speed_inc(each,1)

        if level == 3 and score >= 200000:
            upgrade_sound.play()

            level = 4

            add_big_enemies(big_enemies,enemies,2,bg_size)
            add_mid_enemies(mid_enemies,enemies,4,bg_size)
            add_small_enemies(small_enemies,enemies,6,bg_size)

            for each in small_enemies:
                speed_inc(each,1)
            for each in big_enemies:
                speed_inc(each,1)

        if level == 4 and score >= 500000:
            upgrade_sound.play()

            level = 5

            add_big_enemies(big_enemies,enemies,2,bg_size)
            add_mid_enemies(mid_enemies,enemies,4,bg_size)
            add_small_enemies(small_enemies,enemies,6,bg_size)

            for each in small_enemies:
                speed_inc(each,1)
            for each in mid_enemies:
                speed_inc(each,1)
            for each in big_enemies:
                speed_inc(each,1)


        if not pause and life_num > 0:
            #获取按键（用于频繁触发的事件）
            key_pressed = pg.key.get_pressed()
            #使用键盘操作飞机
            if key_pressed[K_w] or key_pressed[K_UP]:
                my_plane.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                my_plane.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                my_plane.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                my_plane.moveRight()



            #碰撞检测
            #mask部分撞击才算是有效撞击，需要对象有一个mask属性
            enemies_down = pg.sprite.spritecollide(my_plane,enemies,False,pg.sprite.collide_mask)
            if enemies_down:
                if not my_plane.invincible:
                    my_plane.active = False
                for each in enemies_down:
                    each.active = False

            #发射子弹,每10帧发射一颗子弹,每10帧一颗子弹重新装入
            if delay % 5 == 0:
                if is_double_bullet:
                    #左边的子弹和右边的子弹
                    print(bullets2)
                    bullets2[bullet2_index].reset((my_plane.rect.centerx-33,my_plane.rect.centery))
                    bullets2[bullet2_index + 1].reset((my_plane.rect.centerx+30,my_plane.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET2_NUM
                    bullets = bullets2
                else:
                    bullets1[bullet1_index].reset(my_plane.rect.center)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM
                    bullets = bullets1

            #检测子弹是否击中敌机，并绘制子弹
            for each in bullets:
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                    hit_enemies = pg.sprite.spritecollide(each,enemies,False,pg.sprite.collide_mask)
                    if hit_enemies:
                        each.active = False
                        for i in hit_enemies:
                            if i in mid_enemies or i in big_enemies:
                                i.hit = True
                                i.energy -= 1
                                #能量为0时才消失
                                if i.energy == 0:
                                    i.active = False
                            else:
                                i.active = False

            #绘制敌机
            #大飞机也有两种状态
            for each in big_enemies:
                #未被击落，绘制正常飞行的图片
                if each.active:
                    #飞机飞行自带声音
                    if each.rect.bottom == 0:
                        enemy3_fly_sound.play()
                    each.move()
                    #绘制血槽
                    #黑线做背景
                    pg.draw.line(screen,BLACK,(each.rect.left,each.rect.top - 5),(each.rect.right,each.rect.top - 5),3)
                    #血量多于40%为绿色，低于为红色
                    energy_perc = each.energy / enemy.bigEnemy.energy
                    if energy_perc <= 0.4:
                        energy_color = RED
                    else:
                        energy_color = GREEN
                    #再画出剩余血量
                    pg.draw.line(screen,energy_color,(each.rect.left,each.rect.top - 5),(each.rect.left + each.rect.width * energy_perc,each.rect.top - 5),3)
                    #未被击中
                    if not each.hit:
                        if is_switch:
                            screen.blit(each.image1,each.rect)
                        else:
                            screen.blit(each.image2,each.rect)
                    else:
                    #被击中
                        screen.blit(each.image_hit,each.rect)
                        each.hit = False
                #飞机被击落
                else:
                    #每3帧切换一次
                    if delay % 3 == 0:
                        #只播放一次声音
                        if big_destory_images_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destory_images[big_destory_images_index],each.rect)
                        #依次从0到5进行检索，5后回到0
                        big_destory_images_index = (big_destory_images_index + 1 ) % 6
                        #所有图片播放完毕，重新生成
                        if big_destory_images_index == 0:
                            score += 10000
                            each.reset()


            for each in mid_enemies:
                if each.active:
                    each.move()
                    if not each.hit:
                        screen.blit(each.image,each.rect)
                    else:
                        screen.blit(each.image_hit,each.rect)
                        each.hit = False
                #绘制血槽
                    #黑线做背景
                    pg.draw.line(screen,BLACK,(each.rect.left,each.rect.top - 5),(each.rect.right,each.rect.top - 5),3)
                    #血量多于40%为绿色，低于为红色
                    energy_perc = each.energy / enemy.midEnemy.energy
                    if energy_perc <= 0.4:
                        energy_color = RED
                    else:
                        energy_color = GREEN
                    #再画出剩余血量
                    pg.draw.line(screen,energy_color,(each.rect.left,each.rect.top - 5),(each.rect.left + each.rect.width * energy_perc,each.rect.top - 5),3)
                #飞机被击落
                else:
                    #每3帧切换一次
                    if delay % 3 == 0:
                        if mid_destory_images_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destory_images[mid_destory_images_index],each.rect)
                        #依次从0到3进行检索，3后回到0
                        mid_destory_images_index = (mid_destory_images_index + 1 ) % 4
                        #所有图片播放完毕，重新生成
                        if mid_destory_images_index == 0:
                            score += 5000
                            each.reset()

            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                #飞机被击落
                else:
                    #每3帧切换一次
                    if delay % 3 == 0:
                        if small_destory_images_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destory_images[small_destory_images_index],each.rect)
                        #依次从0到3进行检索，3后回到0
                        small_destory_images_index = (small_destory_images_index + 1 ) % 4
                        #所有图片播放完毕，重新生成
                        if small_destory_images_index == 0:
                            score += 1000
                            each.reset()

            #绘制我方飞机，两种状态之间的切换
            if my_plane.active:
                if is_switch:
                    screen.blit(my_plane.image1,my_plane.rect)
                else:
                    screen.blit(my_plane.image2,my_plane.rect)
            #飞机被击落
            else:
                #每3帧切换一次
                if delay % 3 == 0:
                    if me_destory_images_index == 0:
                            me_down_sound.play()
                    screen.blit(my_plane.destory_images[me_destory_images_index],my_plane.rect)
                    #依次从0到3进行检索，3后回到0
                    me_destory_images_index = (me_destory_images_index + 1 ) % 4
                    #所有图片播放完毕，重新生成
                    if me_destory_images_index == 0:
                        life_num -= 1
                        my_plane.reset()
                        pg.time.set_timer(INVINCIBLE,3 * 1000)

            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pg.sprite.collide_mask(bomb_supply,my_plane):
                    bomb_supply.active = False
                    if bomb_num < 3:
                        bomb_num += 1
            #若撞击的是两个单独的对象，用 collide_mask()
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pg.sprite.collide_mask(bullet_supply,my_plane):
                    bullet_supply.active = False
                    is_double_bullet = True
                    pg.time.set_timer(DOUBLE_BULLET_STOP,20 * 1000)

            #每5帧切换一次，也就是一秒切换6次
            if delay % 5 == 0:
                is_switch = not is_switch

            #绘制炸弹
            screen.blit(bomb_image,bomb_rect)

            #绘制炸弹数量
            bomb_num_text = bomb_font.render(' X %d'%bomb_num,True,BLACK)
            screen.blit(bomb_num_text,bomb_num_rect)

            #绘制生命值\
            for i in range(life_num):
                screen.blit(life_image,(5+i*life_rect.width,height - bomb_rect.height - life_rect.height - 5))

            #绘制难度等级
            level_text = level_font.render('Level : %d'%level,True,BLACK)
            screen.blit(level_text,level_rect)

            #绘制分数
            score_text = score_font.render('Score : %d'%score,True,BLACK)
            screen.blit(score_text,(10,10))

            #绘制暂停图片
            screen.blit(pause_image,pause_rect)

        elif life_num == 0:
            #关闭所有音效
            pg.mixer.pause()
            pg.mixer.music.pause()
            pg.time.set_timer(SUPPLY_TIMER,0)

            if is_record == False:
                #读取最好成绩
                best_score = 0
                with open('record.txt','r') as f:
                    #文件指针！！！！
                    s = f.read()
                    if s != '':
                        best_score = int(s)
                #比较成绩
                if score >= best_score:
                    best_score = score
                    with open('record.txt','w') as f:
                        f.write(str(score))

                is_record = True

            #绘制背景
            best_score_text = best_score_font.render('Best Score : %d'%(best_score) ,True,BLACK)
            my_score_text = my_score_font.render('Your Score : %d'%score,True,BLACK)
            screen.blit(best_score_text,(30,150))
            screen.blit(my_score_text,(30,200))
            screen.blit(again_image,again_rect)
            screen.blit(continue_image,continue_rect)
            screen.blit(quit_image,quit_rect)




        delay -= 1
        #复原
        if not delay:
            delay = 100

        pg.display.flip()

        #一秒30帧
        clock.tick(30)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pg.quit()
        input()
