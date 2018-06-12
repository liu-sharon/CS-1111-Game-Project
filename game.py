# Sharon Liu (spl4kv) and Ji In Han (jh8yc)

'''
Just to clarify, we changed our game around from the first checkpoint.
Now the goal is to catch fish and coin within a time limit (15 sec) and to avoid picking up garbage.
The garbage will harm the health of fish caught, shown by the Healthy Fish Meter.
Speeds of game objects (fish, coin, trash) are set to random (up to 30 in each direction.)
'''

import pygame
import gamebox
import random


# Create camera frame
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
camera = gamebox.Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
background = gamebox.from_image(300, 300, "underseagraphic.jpg")

# Build grids
side_box = gamebox.from_color(670, 250, "#42d7f4", 200, 400)

# Create start screen objects
start_screen = [gamebox.from_text(400, 100, "Fish Frenzy", "Arial", 64, "white"),
                gamebox.from_text(400, 160, "Sharon Liu (spl4kv) and Ji Han (jh8yc)", "Arial", 30, "white"),
                gamebox.from_text(400, 290, "Instructions: Click to catch the swimming fish and coins. ", "Arial", 25, "white"),
                gamebox.from_text(400, 320, "But be careful!  Your catch can't survive in pollution,", "Arial", 25, "white"),
                gamebox.from_text(400, 350, "so DON'T pick up the garbage...", "Arial", 25, "white"),
                gamebox.from_text(400, 400, "You have 15 seconds.", "Arial", 25, "white"),
                gamebox.from_text(400, 500, "- Hold down Enter to begin -", "Arial", 50, "white", bold=True)]

# Declare score and time
splash = 1
score = 0
time = 0

# Create health meter:
health_text = gamebox.from_text(670, 65, "Healthy Fish Meter", "comic sans", 25, "white")
health_box = gamebox.from_color(670, 100, "gray", 180, 50)
heart = [gamebox.from_image(620, 100, "heart.png"),
         gamebox.from_image(670, 100, "heart.png"),
         gamebox.from_image(720, 100, "heart.png")]

# Create sprites
SPRITE_SIZE = 100              # sprite image size is 100 x 100
MAX_SPRITE_SPEED = 30          # measured in pixels, equates to pixels per tick
MIN_SPRITE_SPEED = -30
sprite_list = []
evilsprite_list = []
fish_list = ["fish1", "fish2", "fish3", "fish4", "fish5", "fish6", "coin"]
evilfish_list = ["bottle","metal","scrap"]
for fish in fish_list:
    sprite_list.append([gamebox.from_image(WINDOW_WIDTH + 100, WINDOW_HEIGHT, fish + '.png')])
for fish in evilfish_list:
    evilsprite_list.append([gamebox.from_image(WINDOW_WIDTH + 100, WINDOW_HEIGHT, fish + '.png')])

# set THE GAMEBOX item's sprite[0] to a randomly generated center within grid_box, and randomly generated speedx.
for sprite in sprite_list:
    sprite[0].center = [random.randint(SPRITE_SIZE / 2, 600 - SPRITE_SIZE / 2),
                        random.randint(SPRITE_SIZE / 2, 400 - SPRITE_SIZE / 2)]
    sprite[0].speedx = random.randint(MIN_SPRITE_SPEED, MAX_SPRITE_SPEED)
for sprite in evilsprite_list:
    sprite[0].center = [random.randint(SPRITE_SIZE / 2, 600 - SPRITE_SIZE / 2),
                        random.randint(SPRITE_SIZE / 2, 400 - SPRITE_SIZE / 2)]
    sprite[0].speedx = random.randint(MIN_SPRITE_SPEED, MAX_SPRITE_SPEED)

# Create audio
music = gamebox.load_sound("ocean.wav")
glug = gamebox.load_sound("glug.wav")

musicplayer3 = music.play(-1)

def tick(keys):
    global score, splash, time

    # calculate timer
    time += 1
    seconds = str(int((time/ticks_per_second)))
    time_box = gamebox.from_text(670, 400, "Time: " + seconds + "s", "arial", 36, "white", bold=True)

    # make score box
    score_box = gamebox.from_text(670, 150, "Score: ", "Arial", 26, "white", bold=True)
    score_box2 = gamebox.from_text(670, 200, str(score), "Arial", 36, "white", bold=True)

    # Display objects
    camera.draw(background)
    camera.draw(side_box)
    camera.draw(score_box)
    camera.draw(score_box2)
    camera.draw(time_box)
    camera.draw(health_box)
    camera.draw(health_text)

    # Splash screen code snippets used from here: https://cs1110.cs.virginia.edu/code/gamebox-staff/startmenu.py
    if splash == 1:
        camera.clear("#42d7f4")
        for line in start_screen:
            camera.draw(line)
        if pygame.K_RETURN in keys:
            splash = 0
        camera.display()
        return

    # Losing Conditions & Display
    if int(seconds) >= 30:
        time_screen = gamebox.from_text(400, 300, "Time's Up", "arial", 100, "red", bold=True)
        camera.draw(time_screen)
        gamebox.pause()
    if len(heart) == 0:
        lose_screen1 = gamebox.from_text(400, 250, "Oh no!", "arial", 120, "red", bold=True)
        lose_screen2 = gamebox.from_text(400, 350, "All your fish are dead!", "arial", 60, "red", bold=True)
        camera.draw(lose_screen1)
        camera.draw(lose_screen2)
        gamebox.pause()

    # Winning Conditions & Display
    if len(sprite_list) == 0:
        win_screen1 = gamebox.from_text(400, 250, "You Win", "arial", 120, "red", bold=True)
        win_screen2 = gamebox.from_text(400, 350, "You caught all the fish!", "arial", 60, "red", bold=True)
        camera.draw(win_screen1)
        camera.draw(win_screen2)
        gamebox.pause()

    # Set game objects' motions & boundaries
    for sprite in sprite_list:
        sprite[0].move_speed() # Set the gamebox item (sprite[0]) motion
        # wrap motion boundaries
        if sprite[0].right >= 570:
            sprite[0].left = 30
        elif sprite[0].left <= 30:
            sprite[0].right = 570
        # handle_collisions()
        camera.draw(sprite[0])

    for sprite in evilsprite_list:
        sprite[0].move_speed()
        if sprite[0].right >= 570:
            sprite[0].left = 30
        elif sprite[0].left <= 30:
            sprite[0].right = 570
        camera.draw(sprite[0])

    # Mouse click to get rid of fish
    if camera.mouseclick:
        x, y = camera.mouse
        for sprite in sprite_list:
            if sprite[0].contains(x, y):
                global musicplayer3
                musicplayer3 = glug.play(0)
                sprite_list.remove(sprite)
                score += 10
                score_notice = gamebox.from_text(x, y, "+" + str(10), "arial", 30, "white", bold=True)
                camera.draw(score_notice)
    if camera.mouseclick:
        x, y = camera.mouse
        for sprite in evilsprite_list:
            if sprite[0].contains(x, y):
                musicplayer3 = glug.play(0)
                evilsprite_list.remove(sprite)
                score -= 10
                score_notice = gamebox.from_text(x, y, "-" + str(10), "arial", 30, "white", bold=True)
                camera.draw(score_notice)

    for life in heart:
        camera.draw(life)
        if len(evilsprite_list) == 2:
            while len(heart) > 2:
                heart.remove(life)
        elif len(evilsprite_list) == 1:
            while len(heart) > 1:
                heart.remove(life)
        elif len(evilsprite_list) == 0:
            heart.remove(life)

    camera.display()

    def tick2(keys):
        camera.display()

ticks_per_second = 10
ticks_per_second2 = 5

gamebox.timer_loop(ticks_per_second, tick)
