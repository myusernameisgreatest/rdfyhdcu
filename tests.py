import pygame
import random

# image_path = '/data/data/ghost_knight.game.gkgame/files/app/'

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 422
fps = 25
x = 250
y = 332
speed = 0
bg_x = 0
score = 0
go = 1
defence = 100
hp = 100
def_timer = fps/2
shield_regen = fps*2
invulnerability_timer = fps*2
running = True
right = False
left = False
jump = False
drop = False
fight = False
block = False
gameplay = True
cd = False
invulnerability = False
high = 8
music_play = False
turn = False
clock = pygame.time.Clock()
size = [SCREEN_WIDTH, SCREEN_HEIGHT]
player_anim_count = 0

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 1000)

cooldown = pygame.USEREVENT + 2
pygame.time.set_timer(cooldown, 10000)

screen = pygame.display.set_mode(size, flags=pygame.NOFRAME)  # до convert!

pygame.display.set_caption("Ghost Knight")
icon = pygame.image.load('images/icon2.png')

bg = pygame.image.load('images/bg_6.png').convert()
bg_sound = pygame.mixer.Sound('13 - Deviate From The Form.mp3')
font = pygame.font.Font('ClimateCrisis-Regular.ttf', 40)
enemy = pygame.image.load('images/enemy1.png').convert()
fireball = pygame.image.load('images/fireball.png').convert_alpha()

ghost_list = []
fireballs = []

stay = [
    pygame.image.load('images/stop1/stop1.png').convert_alpha(),
    pygame.image.load('images/stop1/stop2.png').convert_alpha(),
    pygame.image.load('images/stop1/stop3.png').convert_alpha(),
    pygame.image.load('images/stop1/stop4.png').convert_alpha()
]
walk_right = [
    pygame.image.load('images/right1/animation1.png').convert_alpha(),
    pygame.image.load('images/right1/animation2.png').convert_alpha(),
    pygame.image.load('images/right1/animation3.png').convert_alpha(),
    pygame.image.load('images/right1/animation4.png').convert_alpha()
]
walk_left = [
    pygame.image.load('images/left1/left1.png').convert_alpha(),
    pygame.image.load('images/left1/left2.png').convert_alpha(),
    pygame.image.load('images/left1/left3.png').convert_alpha(),
    pygame.image.load('images/left1/left4.png').convert_alpha()
]
attack = [
    pygame.image.load('images/attack1/attack1.png').convert_alpha(),
    pygame.image.load('images/attack1/attack2.png').convert_alpha(),
    pygame.image.load('images/attack1/attack3.png').convert_alpha(),
    pygame.image.load('images/attack1/attack4.png').convert_alpha(),
]
defend = pygame.image.load('images/block1/block1.png').convert_alpha()
stay_left = pygame.image.load('images/stop_left1/stay_left.png').convert_alpha()
block_right = pygame.image.load('images/block_right1/block_right.png').convert_alpha()

player = stay[player_anim_count]

while running:

    clock.tick(fps)

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + SCREEN_WIDTH, 0))
    player_rect = stay[player_anim_count].get_rect(topleft=(x, y))
    # screen_rect = bg.get_rect(topleft=(bg_x, 0))

    if gameplay:
        if invulnerability and invulnerability_timer % 2 == 0:
            pass
        elif left:
            screen.blit(walk_left[player_anim_count], (x, y))
        elif right:
            screen.blit(walk_right[player_anim_count], (x, y))
        elif fight:
            screen.blit(attack[player_anim_count], (x, y))
            if player_anim_count == 3:
                fight = False
        elif block and not turn:
            screen.blit(block_right, (x, y))
        elif block and turn:
            screen.blit(defend, (x, y))
        elif turn and not block:
            screen.blit(stay_left, (x, y))
        else:
            screen.blit(stay[player_anim_count], (x, y))


        hp_surface = font.render('Health: '+str(hp), True, 'Red')
        defence_surface = font.render('Defence: '+str(defence), True, 'Blue')
        screen.blit(hp_surface, (15, 15))
        screen.blit(defence_surface, (15, 65))

        if jump and high > 0 and not drop:
            y -= (high ** 2)/2
            high -= 1
            if high == 0:
                drop = True
        if drop:
            y += (high ** 2)/2
            high += 1
            if high > 8:
                jump = False
                drop = False
                high = 8

        if ghost_list:
            for element in ghost_list:
                screen.blit(enemy, element)
                element.x -= 6

                if player_rect.colliderect(element):
                    if fight:
                        if element.y < 300:
                            score += 100
                        ghost_list.remove(element)
                        score += 100
                    elif block and not turn:
                        defence -= 50
                        element.x += 150
                    elif not invulnerability:
                        hp -= 25
                        invulnerability = True
                        if hp <= 0:
                            gameplay = False

                if element.x < -30:
                    ghost_list.remove(element)
                    score += 10

                if fireballs:
                    for ball in fireballs:
                        screen.blit(fireball, ball)
                        ball.x += 15
                        if ball.x > x + SCREEN_WIDTH:
                            fireballs.remove(ball)
                        if ball.colliderect(element):
                            if element.y < 300:
                                score += 100
                            ghost_list.remove(element)
                            fireballs.remove(ball)
                            score += 100

        # if player_rect.colliderect(screen_rect):
        #     if x <= 0:
        #         player_rect.left = screen_rect.left
        #     if x >= SCREEN_WIDTH:
        #         player_rect.right = screen_rect.right



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # if x > 50:
                    speed = -8
                    # else:
                    #     x = 50
                    left = True
                    right = False
                    turn = False

                if event.key == pygame.K_RIGHT:
                    # if x < SCREEN_WIDTH-50:
                    speed = 8
                    # else:
                    #     x = SCREEN_WIDTH-50
                    right = True
                    left = False
                    turn = False

                if event.key == pygame.K_UP and not jump:
                    jump = True

                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_q:
                    fps -= 5

                if event.key == pygame.K_e:
                    fps += 5

                if event.key == pygame.K_SPACE:
                    if not music_play:
                        bg_sound.play()
                        music_play = True
                    else:
                        bg_sound.stop()
                        music_play = False

                if event.key == pygame.K_LCTRL:
                    fight = True
                    right = False
                    left = False
                    turn = False
                    player_anim_count = 0

                if event.key == pygame.K_LALT and not cd:
                    fireballs.append(fireball.get_rect(topleft=(x+30, y)))
                    cd = True

                if event.key == pygame.K_LSHIFT and defence > 0:
                    block = True
                    fight = False
                    right = False
                    left = False

            if event.type == ghost_timer:
                go = random.randrange(0, 2, 1)
                if go == 1:
                    ghost_list.append(enemy.get_rect(topleft=(SCREEN_WIDTH+40, y)))

            if event.type == cooldown:
                cd = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and speed < 0:
                    speed = 0
                    player = stay[player_anim_count]
                    left = False
                    right = False
                    turn = True

                if event.key == pygame.K_RIGHT and speed > 0:
                    speed = 0
                    player = stay[player_anim_count]
                    left = False
                    right = False

                if event.key == pygame.K_LSHIFT:
                    block = False
                    def_timer = fps / 2

        x += speed

        if block:
            def_timer -= 1
            if def_timer <= 0 or defence <= 0:
                block = False
                def_timer = fps/2

        if defence < 100:
            shield_regen -= 1
            if shield_regen <= 0:
                defence = 100
                shield_regen = fps*2

        if invulnerability:
            invulnerability_timer -= 1
            if invulnerability_timer <= 0:
                invulnerability = False
                invulnerability_timer = fps*2
        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= speed/4
        if bg_x <= -SCREEN_WIDTH:
            bg_x += SCREEN_WIDTH
        if bg_x >= 0:
            bg_x -= SCREEN_WIDTH

    else:
        screen.fill('Grey')
        text_surface = font.render('YOU DIED', True, 'Red')
        score_surface = font.render('SCORES: '+str(score), True, 'Black')
        restart_surface = font.render('RESTART', True, 'Blue')
        restart_surface_rect = restart_surface.get_rect(topleft=(SCREEN_WIDTH/3.5+50, SCREEN_HEIGHT/2-50))
        screen.blit(text_surface, (SCREEN_WIDTH/3.5+50, SCREEN_HEIGHT/2))
        screen.blit(score_surface, (SCREEN_WIDTH / 3.5, SCREEN_HEIGHT / 2+50))
        screen.blit(restart_surface, restart_surface_rect)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_r:
                    gameplay = True
                    x = 250
                    y = 332
                    high = 8
                    speed = 0
                    score = 0
                    player_anim_count = 0
                    defence = 100
                    hp = 100
                    def_timer = fps / 2
                    shield_regen = fps * 2
                    invulnerability_timer = fps * 2
                    right = False
                    left = False
                    jump = False
                    drop = False
                    fight = False
                    cd = False
                    invulnerability = False
                    bg_sound.stop()
                    music_play = False
                    turn = False
                    ghost_list.clear()
                    fireballs.clear()

        mouse = pygame.mouse.get_pos()
        if restart_surface_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            x = 250
            y = 332
            high = 8
            speed = 0
            score = 0
            player_anim_count = 0
            defence = 100
            hp = 100
            def_timer = fps / 2
            shield_regen = fps * 2
            invulnerability_timer = fps * 2
            right = False
            left = False
            jump = False
            drop = False
            fight = False
            cd = False
            invulnerability = False
            bg_sound.stop()
            music_play = False
            turn = False
            ghost_list.clear()
            fireballs.clear()

    pygame.display.update()

pygame.quit()
