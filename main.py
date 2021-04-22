
import pygame as py
import random
import HandTrackingModule as htm
import cv2
import math

def floor_scroll():
    screen.blit(floor, (floor_x, 365))
    screen.blit(floor, (floor_x + 1080, 365))

def background_scroll():
    screen.blit(background, (background_x, 0))
    screen.blit(background, (background_x + 1080, 0))

def create_coin():
    new_coin = coin.get_rect(center=(1100, random.randint(400, 500)))
    return new_coin

def draw_coins(coins):
    for coin_rect in coins:
        screen.blit(coin, coin_rect)

def create_bird():
    new_bird = bird[0].get_rect(center=(1100, random.randint(450, 525)))
    return new_bird

def move_birds(birds):
    for bird_rect in birds:
        bird_rect.centerx -= 5 * game_speed
    return birds

def draw_birds(birds):
    for bird_rect in birds:
        screen.blit(bird[bird_index], bird_rect)

def create_chain():
    new_chain = chain.get_rect(center=(1100, 270))
    return new_chain

def draw_chains(chains):
    for chains_rect in chains:
        screen.blit(chain, chains_rect)

def create_dummy():
    new_dummy = dummy.get_rect(center=(1100, 520))
    return new_dummy

def move_dummies(dummies):
    for dummy in dummies:
        dummy.centerx -= 3 * game_speed
    return dummies

def draw_dummies(dummies):
    for dummy_rect in dummies:
        screen.blit(dummy, dummy_rect)

def collision_check_dummies(dummies):

    for dummy_rect in dummies:
        if slashing:
            if 135 < dummy_rect.centerx < 140 and ninja_rectangle.bottom > 490:
                dummies.remove(dummy_rect)
                dummy_slash_sound.play()
                return False
        if dummy_rect.centerx < 140 and dummy_rect.centerx > 90:
            if ninja_rectangle.bottom > 520:
                hit_sound.play()
                return True
    else:
         return False

def collision_check_chains(chains):

    for chain_rect in chains:
        if 120 < chain_rect.centerx <= 130:
            if sliding:
                return False
            else:
                hit_sound.play()
                return True

def collision_coins(coinslist, coinsIn):
    for coin_rect in coinslist:
        if 90 < coin_rect.centerx < 140:
            if coin_rect.centery < ninja_rectangle.centery + 25 and coin_rect.centery > ninja_rectangle.centery - 25:
                coinsIn += 1
                coin_sound.play()
                coinslist.remove(coin_rect)
    return coinslist, coinsIn

def collision_check_birds(birds):
    y_slide = 25
    for bird_rect in birds:
        if 90 < bird_rect.centerx < 140:
            if sliding:
                y_slide = 0
            if bird_rect.centery < ninja_rectangle.centery + 25 and bird_rect.centery > ninja_rectangle.centery - y_slide:
                hit_sound.play()
                return True
    return False
def ninja_animation():
    if running:
        new_ninja = ninja_run[ninja_run_index]
    if jumping:
        new_ninja = ninja_jump[ninja_jump_index]
    if slashing:
        new_ninja = ninja_slash
    new_ninja_rect = new_ninja.get_rect(center=(100, ninja_rectangle.centery))
    if sliding:
        new_ninja = ninja_slide
        new_ninja_rect = new_ninja.get_rect(center=(100, ninja_rectangle.bottom))

    return new_ninja, new_ninja_rect

def get_ninja_jump_index():
    index = 0

    if ninja_rectangle.centery <= 525:
        index = 0
    if ninja_rectangle.centery <= 470 and ninja_movement < 0:
        index = 0
    if ninja_rectangle.centery <= 460 and ninja_movement > 0:
        index = 3
    elif ninja_rectangle.centery <= 525 and ninja_movement > 0:
        index = 3
    return index

def score(dummies, birds, chains):
    s = 0
    for dummy_rect in dummies:
        if dummy_rect.centerx < 90:
            s += 1
    for bird_rect in birds:
        if bird_rect.centerx < 90:
            s += 2
    for chain_rect in chains:
        if chain_rect.centerx < 90:
            s += 3
    s = s + coins*5
    return s

def show_score():
    score_surface = game_font.render('Score: '+str(current_score), False, (255, 255, 255))
    score_rectangle = score_surface.get_rect(center=(540, 75))
    screen.blit(score_surface, score_rectangle)

def display_hi_score():
    hi_score_surface = game_font.render('High Score: '+str(hi_score), False, (255, 255, 255))
    hi_score_rectangle = hi_score_surface.get_rect(center=(540, 250))
    screen.blit(hi_score_surface, hi_score_rectangle)

def save_hi_score(s):
    file = open('hi_score.bin', 'wb')
    file.write(s.to_bytes(1, byteorder='big'))

def load_hi_score():
    file = open('hi_score.bin', 'rb')
    s = int.from_bytes(file.read(1), byteorder='big')
    return s

def display_game_over():
    game_over_surface1 = game_font.render('Press Space To', False, (255, 255, 255))
    game_over_rectangle1 = game_over_surface1.get_rect(center=(540, 420))
    screen.blit(game_over_surface1, game_over_rectangle1)
    game_over_surface2 = game_font.render('Play Again', False, (255, 255, 255))
    game_over_rectangle2 = game_over_surface2.get_rect(center=(540, 500))
    screen.blit(game_over_surface2, game_over_rectangle2)

py.init()

gravity = 0.25
ninja_movement = 0
game_speed = 1


screen = py.display.set_mode((1080, 600))
clock = py.time.Clock()

background = py.image.load('images/background.png').convert()
background = py.transform.scale(background, (1080, 600))
background_x = 0

floor = py.image.load('images/Floor.png').convert_alpha()
floor = py.transform.scale(floor, (1080, 200))
floor_x = 0

#ninja = py.image.load('images/NinjaStand.png').convert_alpha()

#ninja = py.transform.scale(ninja, (50, 50))
#ninja_rectangle = ninja.get_rect(center=(100, 525))
ninja_run1 = py.transform.scale(py.image.load('images/NinjaRun1.png').convert_alpha(), (50, 50))
ninja_run2 = py.transform.scale(py.image.load('images/NinjaRun2.png').convert_alpha(), (50, 50))
ninja_run3 = py.transform.scale(py.image.load('images/NinjaRun3.png').convert_alpha(), (50, 50))
ninja_run = [ninja_run1, ninja_run2, ninja_run3]
ninja_run_index = 0
ninja = ninja_run[ninja_run_index]
ninja_rectangle = ninja.get_rect(center=(100, 525))
NINJARUN = py.USEREVENT + 1
py.time.set_timer(NINJARUN, 150)

ninja_jump1 = py.transform.scale(py.image.load('images/NinjaJump1.png').convert_alpha(), (60, 60))
ninja_jump2 = py.transform.scale(py.image.load('images/NinjaJump2.png').convert_alpha(), (60, 60))
ninja_jump3 = py.transform.scale(py.image.load('images/NinjaJump3.png').convert_alpha(), (60, 60))
ninja_jump4 = py.transform.scale(py.image.load('images/NinjaJump4.png').convert_alpha(), (60, 60))
ninja_jump = [ninja_jump1, ninja_jump2, ninja_jump3, ninja_jump4]
ninja_jump_index = 0

ninja_slide = py.transform.scale(py.image.load('images/NinjaSlide.png').convert_alpha(), (60, 30))

bird_1 = py.transform.scale(py.image.load('images/Bird1.png').convert_alpha(), (30, 30))
bird_2 = py.transform.scale(py.image.load('images/Bird2.png').convert_alpha(), (30, 30))
bird_3 = py.transform.scale(py.image.load('images/Bird3.png').convert_alpha(), (30, 30))
bird_4 = py.transform.scale(py.image.load('images/Bird4.png').convert_alpha(), (30, 30))
bird_5 = py.transform.scale(py.image.load('images/Bird5.png').convert_alpha(), (30, 30))
bird = [bird_1, bird_2, bird_3, bird_4, bird_5]
bird_index = 0
bird_list = []
CREATEBIRD = py.USEREVENT + 4
py.time.set_timer(CREATEBIRD, random.randint(3000, 8000))


ninja_slash = py.transform.scale(py.image.load('images/NinjaSlash.png').convert_alpha(), (80, 50))

dummy = py.image.load('images/Dummy.png').convert_alpha()
dummy = py.transform.scale(dummy, (35, 60))
dummy_list = []
CREATEDUMMY = py.USEREVENT
py.time.set_timer(CREATEDUMMY, random.randint(750, 3000))

coin = py.image.load('images/Coin.png').convert_alpha()
coin = py.transform.scale(coin, (15, 20))
CREATECOIN = py.USEREVENT + 3
py.time.set_timer(CREATECOIN, random.randint(5000, 12000))
coin_list = []

chain = py.transform.scale(py.image.load('images/ChainSpike.png').convert_alpha(), (30, 520))
CREATECHAIN = py.USEREVENT + 5
py.time.set_timer(CREATECHAIN, random.randint(10000, 15000))
chain_list = []


JUMPGESTURE = py.USEREVENT + 2
jump_gesture_event = py.event.Event(JUMPGESTURE, message='jump')

hit_sound = py.mixer.Sound('sounds/hit.wav')
jump_sound = py.mixer.Sound('sounds/jump.wav')
dummy_slash_sound = py.mixer.Sound('sounds/dummyslash.wav')
coin_sound = py.mixer.Sound('sounds/coin.wav')

game_font = py.font.Font('slkscr.ttf', 80)

game_over = False
gesture_active = False
current_score = 0
coins = 0
hi_score = load_hi_score()
running = True
jumping = False
slashing = False
sliding = False
slash_cooldown = py.time.get_ticks()
slide_cooldown = py.time.get_ticks()

capture = cv2.VideoCapture(0)
detector = htm.Hand(maxHands=1)

score_surface = game_font.render(str(current_score), False, (255, 255, 255))

while True:

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()
        if event.type == py.KEYDOWN or event.type == JUMPGESTURE:
            if event.type == JUMPGESTURE or event.key == py.K_SPACE:
                if ninja_rectangle.centery == 525:
                    jumping = True
                    jump_sound.play()
                    running = False
                    ninja_movement = 0
                    ninja_movement -= 7


                if game_over:
                    game_over = False
                    game_speed = 1
                    current_score = 0
                    coins = 0
                    dummy_list.clear()
                    coin_list.clear()
                    bird_list.clear()
                    chain_list.clear()
                    ninja_rectangle.center = (100, 525)
                    ninja_movement = 0
            if event.type == py.KEYDOWN and event.key == py.K_g:
                gesture_active = not gesture_active
            if event.type == py.KEYDOWN and event.key == py.K_s:
                slashing = True
                ninja = ninja_slash
                slash_cooldown = py.time.get_ticks()
                running = False
            if event.type == py.KEYDOWN and event.key == py.K_d:
                if not jumping:
                    sliding = True

                    slide_cooldown = py.time.get_ticks()
                    running = False

        if event.type == CREATEDUMMY:
            dummy_list.append(create_dummy())
            py.time.set_timer(CREATEDUMMY, random.randint(750, 3000))
        if event.type == NINJARUN:
            if running:
                ninja_run_index += 1
                if ninja_run_index > 2:
                    ninja_run_index = 0
            bird_index += 1
            if bird_index > 4:
                bird_index = 0

        if event.type == CREATECOIN:
            coin_list.append(create_coin())
            py.time.set_timer(CREATECOIN, random.randint(5000, 12000))
        if event.type == CREATEBIRD:
            bird_list.append(create_bird())
            py.time.set_timer(CREATEBIRD, random.randint(3000, 8000))
        if event.type == CREATECHAIN:
            chain_list.append(create_chain())
            py.time.set_timer(CREATECHAIN, random.randint(10000, 15000))




    background_x -= 0.5 * game_speed
    background_scroll()
    if background_x <= -1080:
         background_x = 0
    floor_x -= 3 * game_speed
    floor_scroll()
    if floor_x <= -1080:
        floor_x = 0
    if not game_over:
        if current_score >= 50:
            game_speed = 1.25
        if current_score >= 100:
             game_speed = 1.5
        if current_score >= 150:
            game_speed = 1.75
        if current_score >= 200:
             game_speed = 2
        ninja_movement += gravity

        ninja_rectangle.centery += ninja_movement
        if ninja_rectangle.centery >= 525:
            ninja_rectangle.centery = 525
            jumping = False
            running = True

        ninja_jump_index = get_ninja_jump_index()
        ninja, ninja_rectangle = ninja_animation()
        screen.blit(ninja, ninja_rectangle)
        game_over = collision_check_dummies(dummy_list)
        if not game_over:
            game_over = collision_check_chains(chain_list)
        if not game_over:
            game_over = collision_check_birds(bird_list)
        coin_list, coins = collision_coins(coin_list, coins)

        current_score = score(dummy_list, bird_list, chain_list)
        show_score()


        if (slash_cooldown-py.time.get_ticks()) < -150:
            slashing = False
            running = True

        if (slide_cooldown-py.time.get_ticks()) < -250:
            sliding = False
            running = True

        dummy_list = move_dummies(dummy_list)
        draw_dummies(dummy_list)

        coin_list = move_dummies(coin_list)
        draw_coins(coin_list)

        bird_list = move_birds(bird_list)
        draw_birds(bird_list)

        chain_list = move_dummies(chain_list)
        draw_chains(chain_list)

        py.display.update()
        clock.tick(60)

        if(gesture_active):
            success, img = capture.read()
            if success:
                img = detector.findHands(img)
                #img = cv2.flip(img, 1)
                lmlist = []
                lmlist = detector.findPos(img)

                length = 100
                if len(detector.findPos(img)) > 0 and gesture_active:
                    x1, y1 = lmlist[4][1], lmlist[4][2]
                    x2, y2 = lmlist[8][1], lmlist[8][2]
                    x3, y3 = lmlist[12][1], lmlist[12][2]
                    length = math.hypot(x2-x1, y2-y1)
                    if y1 < y2:
                        print("Slide")
                    elif length < 30:
                        py.event.post(jump_gesture_event)
                    elif math.hypot(x3-x1, y3-y1) < 30:
                        print("Slash")

                #cv2.imshow("Hand Tracking", img)
                #cv2.waitKey(1)
    else:
        if current_score > hi_score:
            hi_score = current_score
            save_hi_score(hi_score)
        show_score()
        display_hi_score()
        display_game_over()
        clock.tick(60)
        py.display.update()

