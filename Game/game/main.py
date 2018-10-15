#飞机大战主程序

import pygame
import traceback
from pygame.locals import *
import myplane
import enemy
import bullet
import random
import supply
pygame.init()
pygame.mixer.init()

#设置游戏窗口的尺寸
bg_size = width,height = 480,852
screen = pygame.display.set_mode(bg_size)

#设置窗口名称
pygame.display.set_caption('飞机大战')


#血槽颜色RGB
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
yellow = (215,176,19)

#分数文字颜色
white = (255,255,255)

#加载游戏背景图片
background = pygame.image.load('Game/game/images/background.png')

#载入游戏音乐Game/game/sound/game_music.ogg
pygame.mixer.music.load('Game/game/sound/game_music.ogg') #背景音乐
pygame.mixer.music.set_volume(0.4)  #背景音乐声音大小

#其他音效
bullet_sound = pygame.mixer.Sound('Game/game/sound/bullet.wav')
bullet_sound.set_volume(0.3)

bomb_sound = pygame.mixer.Sound('Game/game/sound/use_bomb.wav')
bomb_sound.set_volume(0.6)

supply_sound = pygame.mixer.Sound('Game/game/sound/supply.wav')
supply_sound.set_volume(0.6)

get_bomb_sound = pygame.mixer.Sound('Game/game/sound/get_bomb.wav')
get_bomb_sound.set_volume(0.6)

get_bullet_sound = pygame.mixer.Sound('Game/game/sound/get_bullet.wav')
get_bullet_sound.set_volume(0.6)

upgrade_sound = pygame.mixer.Sound('Game/game/sound/upgrade.wav')
upgrade_sound.set_volume(0.6)

enemy1_down_sound = pygame.mixer.Sound('Game/game/sound/enemy1_down.wav')
enemy1_down_sound.set_volume(0.6)

enemy2_down_sound = pygame.mixer.Sound('Game/game/sound/enemy2_down.wav')
enemy2_down_sound.set_volume(0.6)

enemy3_down_sound = pygame.mixer.Sound('Game/game/sound/enemy3_down.wav')
enemy3_down_sound.set_volume(0.8)

enemy3_fly_sound = pygame.mixer.Sound('Game/game/sound/enemy3_flying.wav')
enemy3_fly_sound.set_volume(0.8)

me_down_sound = pygame.mixer.Sound('Game/game/sound/me_down.wav')
me_down_sound.set_volume(0.2)

#创建小型飞机
def add_small_enemies(group,group1,num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group.add(e1)
        group1.add(e1)

#创建中型飞机
def add_mid_enemies(group,group1,num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group.add(e2)
        group1.add(e2)

#创建大型飞机
def add_max_enemies(group,group1,num):
    for i in range(num):
        e3 = enemy.MaxEnemy(bg_size)
        group.add(e3)
        group1.add(e3)

#提升敌机的速度
def inc_speed(target,inc):
    for each in target:
        each.speed += inc
#主函数
def main():
    #播放背景音乐,-1代表循环播放
    pygame.mixer.music.play(-1)

    #生成玩家飞机
    me = myplane.MyPlane(bg_size)
    
    #生成敌方飞机
    enemies = pygame.sprite.Group()

    #生成敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15)

    #生成敌方中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies,enemies,8)

    #生成敌方大型飞机
    max_enemies = pygame.sprite.Group()
    add_max_enemies(max_enemies,enemies,4)

    #生成普通子弹
    bulletlist = []
    bullet_index = 0
    bullet_num = 4
    for i in range(bullet_num):
        bulletlist.append(bullet.Bullet(me.rect.midtop))

    #生成双发子弹
    bulletlist1 = []
    bullet1_index = 0
    bullet1_num = 8
    for i in range(bullet1_num // 2):
        bulletlist1.append(bullet.Bullet1((me.rect.centerx-33, me.rect.centery)))
        bulletlist1.append(bullet.Bullet1((me.rect.centerx+33, me.rect.centery)))   

    clock = pygame.time.Clock()

    #中弹后图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0
    

    #统计得分
    score = 0

    #分数字体以及字体大小
    score_font = pygame.font.SysFont('STCAIYUN ',36)
    
    #是否暂停判断
    paused = False

    #加载暂停与恢复图片
    pause_nor_image = pygame.image.load('Game/game/images/pause_nor.png').convert_alpha()
    pause_pressed_image = pygame.image.load('Game/game/images/pause_pressed.png').convert_alpha()
    resume_nor_image = pygame.image.load('Game/game/images/resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load('Game/game/images/resume_pressed.png').convert_alpha()
    
    #获取定位尺寸
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10,10
    paused_image = pause_nor_image

    #用于切换图片
    switch_image = True

    #用于延迟,让玩家飞机的图形切换更有规律
    delay = 100
    
    #设置难度
    level = 1

    #全屏炸弹
    bomb_image = pygame.image.load('Game/game/images/bomb.png').convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.SysFont('STCAIYUN',48)
    bomb_num = 3

    #设定一个随机数，用来达到随机秒的时候投放道具
    randomSum = random.randint(10,20)
    
    #定时投放补给
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    supply_time = USEREVENT
    pygame.time.set_timer(supply_time,randomSum * 1000)
    
    #双发子弹定时器
    double_bullet_time = USEREVENT + 1

    #是否使用双发子弹
    is_double_bullet = False
    
    #无敌解除定时
    invincible_time = USEREVENT + 2

    #生命数量
    life_image = pygame.image.load('Game/game/images/life.png').convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    #阻止重复打开文件
    recorded = False

    #判断游戏是否结束
    gameover = False
    #结束图片
    gameover_font = pygame.font.SysFont('STCAIYUN',48)
    again_image = pygame.image.load('Game/game/images/again.png').convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load('Game/game/images/gameover.png').convert_alpha()
    gameover_rect = gameover_image.get_rect()

    running = True

    while running:
        #判断用户是否点击窗口关闭
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #判断玩家是否点击暂停或恢复按钮elif event.type == MOUSEBUTTONDOWN:
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(supply_time,0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(supply_time, randomSum * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            elif event.type == supply_time:
                supply_sound.play()
                #随机产生道具包choice([True, False])
                if random.choice([True,False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            elif event.type == double_bullet_time:
                is_double_bullet = False
                pygame.time.set_timer(double_bullet_time,0)
            elif event.type == invincible_time:
                me.invincible = False
                pygame.time.set_timer(invincible_time,0)
        #根据用户得分增加难度
        if level == 1 and score > 50000:
            level = 2
            upgrade_sound.play()
            #增加小型飞机和中型飞机，以及大型飞机的数量,并提升它们的速度
            add_small_enemies(small_enemies,enemies,6)
            add_mid_enemies(mid_enemies,enemies,3)
            add_max_enemies(max_enemies,enemies,1)
            #提升小型飞机的速度
            inc_speed(small_enemies,1)
        elif level == 2 and score > 100000:
            level = 3
            upgrade_sound.play()
            #增加小型飞机和中型飞机，以及大型飞机的数量,并提升它们的速度
            add_small_enemies(small_enemies,enemies,10)
            add_mid_enemies(mid_enemies,enemies,5)
            add_max_enemies(max_enemies,enemies,2)
            #提升小型飞机的速度和中型飞机的速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
        elif level == 3 and score > 250000:
            level = 4
            upgrade_sound.play()
            #增加小型飞机和中型飞机，以及大型飞机的数量,并提升它们的速度
            add_small_enemies(small_enemies,enemies,13)
            add_mid_enemies(mid_enemies,enemies,7)
            add_max_enemies(max_enemies,enemies,4)
            #提升小型飞机的速度和中型飞机以及大型飞机的速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
            inc_speed(max_enemies,1)
        elif level == 4 and score > 500000:
            level = 5
            upgrade_sound.play()
            #增加小型飞机和中型飞机，以及大型飞机的数量,并提升它们的速度
            add_small_enemies(small_enemies,enemies,15)
            add_mid_enemies(mid_enemies,enemies,10)
            add_max_enemies(max_enemies,enemies,5)
            #提升小型飞机的速度和中型飞机以及大型飞机的速度
            inc_speed(small_enemies,1)
            inc_speed(mid_enemies,1)
            inc_speed(max_enemies,1)
        #将背景图片画到窗口
        screen.blit(background,(0,0))
        if life_num and not paused:
            #检测用户键盘操作
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()
            #绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply,me):
                    get_bomb_sound.play()
                    bomb_num += 1
                    bomb_supply.active = False

            #绘制双发子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply,me):
                    get_bullet_sound.play()
                    #发射双发子弹
                    is_double_bullet = True
                    pygame.time.set_timer(double_bullet_time,50 * 1000)
                    bullet_supply.active = False

            #发射子弹
            if not(delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bulletlist1
                    bullets[bullet1_index].reset((me.rect.centerx - 33,me.rect.centery))
                    bullets[bullet1_index+1].reset((me.rect.centerx + 33,me.rect.centery))
                    bullet1_index = (bullet1_index + 2) % bullet1_num
                else:
                    bullets = bulletlist
                    bulletlist[bullet_index].reset(me.rect.midtop)
                    bullet_index = (bullet_index + 1) % bullet_num
                
            
            #检测子弹是否命中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b,enemies,False,pygame.sprite.collide_mask)

                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if (e in mid_enemies) or (e in max_enemies):
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False
            #绘制敌方飞机
            #绘制大型飞机
            for each in max_enemies:
                if each.active:
                    each.move()

                    #如果飞机被命中时，绘制被命中时的图片
                    if each.hit:
                        screen.blit(each.image_hit,each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image,each.rect)
                        else:
                            screen.blit(each.image1,each.rect)

                    #绘制血槽
                    pygame.draw.line(screen,black,(each.rect.left,each.rect.top - 5),(each.rect.right,each.rect.top - 5),2)
                    
                    #当生命值大于百分之二十显示绿色，如果小于0.6并且大于0.2为黄色，否则为红色
                    energy_remain = each.energy / enemy.MaxEnemy.energy
                    if energy_remain > 0.6:
                        energy_color = green
                    elif energy_remain > 0.2 and energy_remain < 0.6:
                        energy_color = yellow
                    else:
                        energy_color = red
                    pygame.draw.line(screen,energy_color,(each.rect.left,each.rect.top - 5),(each.rect.left + each.rect.width * energy_remain,each.rect.top - 5),2)
                    
                    #大型飞机出现之前播放音效
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)
                else:
                    #毁灭,播放毁灭音效
                    if not(delay % 3):
                        if e3_destroy_index == 0:
                            #大型敌机被毁灭后的加分
                            score += 1000
                            enemy3_down_sound.play()                        
                        screen.blit(each.destroy_images[e3_destroy_index],each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            #当大型飞机被毁灭后，停止音效
                            enemy3_fly_sound.stop()
                            each.reset()

            #绘制中型飞机
            for each in mid_enemies:
                if each.active:
                    each.move()

                    #如果飞机被命中时，绘制被命中时的图片
                    if each.hit:
                        screen.blit(each.image_hit,each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image,each.rect)

                    #绘制血槽
                    pygame.draw.line(screen,black,(each.rect.left,each.rect.top - 5),(each.rect.right,each.rect.top - 5),2)
                    
                    #当生命值大于百分之二十显示绿色，如果小于0.6并且大于0.2为黄色，否则为红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.6:
                        energy_color = green
                    elif energy_remain > 0.2 and energy_remain < 0.6:
                        energy_color = yellow
                    else:
                        energy_color = red
                    pygame.draw.line(screen,energy_color,(each.rect.left,each.rect.top - 5),(each.rect.left + each.rect.width * energy_remain,each.rect.top - 5),2)
                    
                else:
                    #毁灭,播放毁灭音效
                    if not(delay % 3):
                        if e2_destroy_index == 0:
                            #中型敌机被毁灭后的加分
                            score += 800
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index],each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            each.reset()
            #绘制小型飞机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                else:
                    #毁灭,播放毁灭音效
                    if not(delay % 3):
                        if e1_destroy_index == 0:
                            #小型敌机被毁灭后的加分
                            score += 500
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index],each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            each.reset()
            #检测玩家飞机是否发生碰撞
            enemies_down = pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                #改为true作为作弊
                # me.active = True
                me.active = False
                for e in enemies_down:
                    e.active = False

            #绘制玩家飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image,me.rect)
                else:
                    screen.blit(me.image1,me.rect)
            else:
                #毁灭,播放毁灭音效
                if not(delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(each.destroy_images[me_destroy_index],me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(invincible_time,3*1000)

            #绘制炸弹图片
            bomb_text = bomb_font.render('X {}'.format(bomb_num),True,white)
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image,(10,height - 10 - text_rect.height))
            screen.blit(bomb_text,(20 + bomb_rect.width,height - 5 - text_rect.height))
            
            #绘制分数字体
            score_text = score_font.render('分数:{}'.format(score),True,white)
            screen.blit(score_text,(10,10))

            #绘制剩余生命
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image,(width-10-(i+1)*life_rect.width,height-10-life_rect.height))
        
        #绘制结束画面
        elif life_num == 0:
            gameover = True
            #去掉音效
            pygame.mixer.music.stop()
            pygame.mixer.stop()

            #停止发放补给
            pygame.time.set_timer(supply_time,0)

            if not recorded:
                recorded = True
                #读取历史最高得分record_score 
                with open('Game/game/re.txt','r') as f:
                    record_score = f.read()
                    if record_score != '':
                        record_score = int(record_score) 
                    else:
                        record_score = 0
                #判断是否高于历史分，并存档
                if score > record_score:
                    with open('Game/game/re.txt','w') as f:
                        f.write(str(score))
            # 绘制结束画面最高分
            record_score_text = score_font.render("最高分:{}".format(record_score), True, (255, 255, 255))
            screen.blit(record_score_text, (10, 10))
            
            gameover_text1 = gameover_font.render("你的分数", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                                 (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)
            
            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                                 (width - gameover_text2_rect.width) // 2, \
                                 gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                             (width - again_rect.width) // 2, \
                             gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                                (width - again_rect.width) // 2, \
                                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击“重新开始”
                if again_rect.left < pos[0] < again_rect.right and \
                   again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    main()
                # 如果用户点击“结束游戏”            
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                     gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    exit()      

            gameover_text1 = gameover_font.render('你的分数'.format(score),True,(255,255,10))
        #绘制暂停按钮
        if not gameover:
            screen.blit(paused_image,paused_rect)
        #切换图片
        if not (delay % 5):
            switch_image = not switch_image
        delay -= 1
        if not delay:
            delay = 100
        #更新图像到窗口
        pygame.display.flip()

        #设置游戏帧数
        clock.tick(120)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    #打印异常退出信息
    except:
        traceback.print_exc()
        pygame.quit()
        input()