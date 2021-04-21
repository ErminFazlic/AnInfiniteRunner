
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

def create_dummy():
    new_dummy = dummy.get_rect(center=(1100, 520))
    return new_dummy

def move_dummies(dummies):
    for dummy in dummies:
        dummy.centerx -= 3
    return dummies

def draw_dummies(dummies):
    for dummy_rect in dummies:
        screen.blit(dummy, dummy_rect)

def collision_check(dummies):

    for dummy_rect in dummies:
        if dummy_rect.centerx < 140 and dummy_rect.centerx > 90:
            if ninja_rectangle.bottom > 520:
                return True
    else:
        return False

def collision_coins(coinslist, coinsIn):
    for coin_rect in coinslist:
        if 90 < coin_rect.centerx < 140:
            if coin_rect.centery < ninja_rectangle.centery + 25 and coin_rect.centery > ninja_rectangle.centery - 25:
                coinsIn += 1
                coinslist.remove(coin_rect)
    return coinslist, coinsIn

def ninja_animation():
    new_ninja = ninja_run[ninja_run_index]
    new_ninja_rect = new_ninja.get_rect(center=(100, ninja_rectangle.centery))
    return new_ninja, new_ninja_rect

def score(dummies):
    s = 0
    for dummy_rect in dummies:
        if dummy_rect.centerx < 90:
            s += 1
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
    s=int.from_bytes(file.read(1), byteorder='big')
    return s

py.init()

gravity = 0.25
ninja_movement = 0



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
ninja_run_index = 2
ninja = ninja_run[ninja_run_index]
ninja_rectangle = ninja.get_rect(center=(100, 525))
NINJARUN = py.USEREVENT + 1
py.time.set_timer(NINJARUN, 150)


dummy = py.image.load('images/Dummy.png').convert_alpha()
dummy = py.transform.scale(dummy, (35, 60))
dummy_list = []
CREATEDUMMY = py.USEREVENT
py.time.set_timer(CREATEDUMMY, random.randint(750, 3000))

coin = py.image.load('images/NinjaStand.png').convert_alpha()
coin = py.transform.scale(coin, (30, 30))
CREATECOIN = py.USEREVENT + 3
py.time.set_timer(CREATECOIN, random.randint(5000, 12000))
coin_list = []

JUMPGESTURE = py.USEREVENT + 2
jump_gesture_event = py.event.Event(JUMPGESTURE, message='jump')


game_font = py.font.Font('slkscr.ttf', 80)

game_over = False
gesture_active = False
current_score = 0
coins = 0
hi_score = load_hi_score()

capture = cv2.VideoCapture(0)
detector = htm.Hand()

score_surface = game_font.render(str(current_score), False, (255, 255, 255))

while True:

    for event in py.event.get():
        if event.type == py.QUIT:
            py.quit()
            exit()
        if event.type == py.KEYDOWN or event.type == JUMPGESTURE:
            if event.type == JUMPGESTURE or event.key == py.K_SPACE:
                if ninja_rectangle.centery == 525:
                    ninja_movement = 0
                    ninja_movement -= 7
                if game_over:
                    game_over = False
                    dummy_list.clear()
                    coin_list.clear()
                    ninja_rectangle.center = (100, 525)
                    ninja_movement = 0
            if event.type == py.KEYDOWN and event.key == py.K_g:
                gesture_active = not gesture_active
        if event.type == CREATEDUMMY:
            dummy_list.append(create_dummy())
            py.time.set_timer(CREATEDUMMY, random.randint(750, 3000))
        if event.type == NINJARUN:
            ninja_run_index += 1
            if ninja_run_index > 2:
                ninja_run_index = 0
            ninja, ninja_rectangle = ninja_animation()
        if event.type == CREATECOIN:
            coin_list.append(create_coin())
            py.time.set_timer(CREATECOIN, random.randint(5000, 12000))


    if not game_over:
        background_x -= 0.5
        background_scroll()
        if background_x <= -1080:
            background_x = 0
        floor_x -= 3
        floor_scroll()
        if floor_x <= -1080:
            floor_x = 0

        ninja_movement += gravity
        ninja_rectangle.centery += ninja_movement
        if ninja_rectangle.centery >= 525:
            ninja_rectangle.centery = 525
        screen.blit(ninja, ninja_rectangle)
        game_over = collision_check(dummy_list)
        coin_list, coins = collision_coins(coin_list, coins)

        current_score = score(dummy_list)
        show_score()


        dummy_list = move_dummies(dummy_list)
        draw_dummies(dummy_list)

        coin_list = move_dummies(coin_list)
        draw_coins(coin_list)

        py.display.update()
        clock.tick(60)

        if(gesture_active):
            success, img = capture.read()
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
        display_hi_score()
        py.display.update()

