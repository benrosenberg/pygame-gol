'''
Conway's Game of Life simulation in pygame
Ben Rosenberg 3.4.2023

Instructions: 
 - Modify constants as desired
 - Run with `python gol_efficient.py`
 - Hit space to pause
   + When paused, draw on the screen to flip squares from alive to dead and vice versa.
   + Hit space to unpause and see what happens!
 - Quit with 'q' or Escape
 - Clear (and pause) with 'c'
 - Left/Right arrows increase/decrease framerate
 - Up/Down arrows increase/decrease scaling

'''

colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255,0,0),
    "blue": (0, 0, 255),
    "green": (0, 204, 0), # easier on the eyes
    "purple": (127, 0, 255),
    "cyan": (0, 255, 255),
    "yellow": (255, 255, 0),
    "orange": (255, 138, 0),
    "pink": (255, 0, 255),
    "hot pink": (255, 0, 127)
}

### CONSTANTS -- modify these as you see fit
size = width, height = 1920, 1080

# colors taken from above dictionary
dead_color = colors["black"]
alive_color = colors["hot pink"]

# scale should be chosen to be a moderately sized number (10 <= scale <= 50)
# so as to minimize performance hit (anything under 10 is pushing it)
scale = 10

# how fast time moves when paused (so as to better detect input)
fps = 1024
# how fast time moves when playing (input responsiveness not as important)
move_fps = 30

# whether or not to display a glider on window open
glider = True

### END CONSTANTS

color_schemes = [
    ('black', 'hot pink'),
    ('blue', 'yellow'),
    ('white', 'black'),
    ('purple', 'cyan'),
    ('yellow', 'hot pink'),
    ('green', 'blue'),
    ('red', 'green')
]

import sys, pygame, random
pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

def render_squares(squares):
    screen.fill(dead_color)
    try:
        for i,j in squares:
            screen.fill(alive_color, ((i*scale, j*scale), (scale, scale)))
    except Exception as e:
        print('squares was ', squares)
        raise e

pause_color = colors['white']
pause_background_color = colors['black']

def render_pause_icon():
    # top right corner
    pause_squares = set()
    pause_background = set()
    max_square_x = width//scale
    for i in range(max_square_x - 5, max_square_x):
        for j in range(5):
            pause_background.add((i,j))
            if 1 <= j <= 3 and (max_square_x - i) % 2 == 0:
                pause_squares.add((i,j))
    # render only when paused
    if pause:
        for i,j in pause_background:
            screen.fill(pause_background_color, ((i*scale, j*scale), (scale, scale)))
        for i,j in pause_squares:
            screen.fill(pause_color, ((i*scale, j*scale), (scale, scale)))

glider_pixels = {(0,1), (1, 2), (2, 0), (2, 1), (2, 2)} if glider else set()

squares = glider_pixels

def flip_square(squares, location):
    x, y = location
    return squares ^ {((x//scale), (y//scale))}

def surrounding(squares):
    temp = set()
    for i,j in squares:
        temp |= {
            (i-1, j-1),(i-1, j),(i-1, j+1),
            (i, j-1),(i, j+1),
            (i+1, j-1),(i+1,j),(i+1,j+1)
        }
    return temp

def update(squares): # Conway's game of life rules
    temp = set()
    for i,j in squares | surrounding(squares):
        # get all directions
        t = (i-1, j) in squares
        b = (i+1, j) in squares
        l = (i, j-1) in squares
        r = (i, j+1) in squares
        tl = (i-1, j-1) in squares
        tr = (i-1, j+1) in squares
        bl = (i+1, j-1) in squares
        br = (i+1, j+1) in squares
        directions = [t, b, l, r, tl, tr, bl, br]
        num_live_neighbors = sum(directions)
        if (i,j) in squares and num_live_neighbors in [2,3]:
            temp.add((i,j))
        elif (i,j) not in squares and num_live_neighbors == 3:
            temp.add((i,j))
    return temp

pause = False

while 1:
    pygame.display.flip()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_q, pygame.K_ESCAPE]:
                sys.exit()
            if event.key == pygame.K_SPACE:
                if pause:
                    pause = False
                else:
                    pause = True
            if event.key == pygame.K_c:
                squares = set()
                screen.fill(dead_color)
                pause = True
            if event.key == pygame.K_LEFT:
                if move_fps >= 6:
                    move_fps /= 2
            if event.key == pygame.K_RIGHT:
                if move_fps <= 100:
                    move_fps *= 2
            if event.key == pygame.K_r:
                dead_color, alive_color = random.choice(color_schemes)
            if event.key == pygame.K_UP:
                if scale < 45:
                    scale += 5
            if event.key == pygame.K_DOWN:
                if scale > 10:
                    scale -= 5

    if not pause:
        screen.fill(dead_color)

        squares = update(squares)

        # fill in squares
        render_squares(squares)

        clock.tick(move_fps)

    if pause:
        # check for mouse clicks
        down, _, _ = pygame.mouse.get_pressed(num_buttons=3)

        # only update visual if changes made
        if down:
            # flip squares that have been touched
            squares = flip_square(squares, pygame.mouse.get_pos())
            # update screen
            render_squares(squares)

        render_pause_icon()

        clock.tick(fps)

