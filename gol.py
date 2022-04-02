'''
Conway's Game of Life simulation in pygame
Ben Rosenberg 4.1.2022

Instructions: 
 - Modify constants as desired
 - Run with `python gol.py`
 - Hit space to pause
   + When paused, use the left mouse button to toggle squares
   + Hit space to unpause and see what happens!
 - Quit with 'q' or Escape

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
dead_color = colors["blue"]
alive_color = colors["yellow"]

# scale should be chosen to be a moderately sized number (10 <= scale <= 50)
# so as to minimize performance hit (anything under 10 is pushing it)
scale = 20

# how fast time moves when paused (so as to better detect input)
fps = 60
# how fast time moves when playing (input responsiveness not as important)
move_fps = 10

# whether or not to display a glider on window open
glider = True

### END CONSTANTS

import sys, pygame
pygame.init()

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

if glider:
    add_scale_mul_scale = lambda x : (scale*x[0] + scale, scale*x[1] + scale)
    glider_pixels = list(map(add_scale_mul_scale,
        [(0,1), (1, 2), (2, 0), (2, 1), (2, 2)]))

squares = [[(i,j,dead_color) if not glider or (i,j) not in glider_pixels
    else (i,j,alive_color)
    for i in range(0, width, scale)]
    for j in range(0, height, scale)]

def flip_square(squares, location):
    def location_to_indices(location):
        x, y = location
        return (x//scale * scale), (y//scale * scale)
    indices = location_to_indices(location)
    flip = lambda color : alive_color if color == dead_color else dead_color
    flip_s = lambda square : (square[0], square[1], flip(square[2]))
    temp = [[s if (s[0],s[1]) != indices else flip_s(s)
        for s in row]
        for row in squares]
    return temp


def update(squares): # Conway's game of life rules
    color = lambda x : x[2]
    temp = [[i for i in j] for j in squares] # avoid shallow copy errors
    for i,row in enumerate(squares):
        for j,square in enumerate(row):
            # get all directions (being mindful of edges)
            t = squares[i-1][j] if i >= 1 else None
            b = squares[i+1][j] if i < len(squares) - 1 else None
            l = squares[i][j-1] if j >= 1 else None
            r = squares[i][j+1] if j < len(row) - 1 else None
            tl = squares[i-1][j-1] if None not in [t, l] else None
            tr = squares[i-1][j+1] if None not in [t, r] else None
            bl = squares[i+1][j-1] if None not in [b, l] else None
            br = squares[i+1][j+1] if None not in [b, r] else None
            directions = [t, b, l, r, tl, tr, bl, br]
            # get the number of non-None white neighbors
            num_live_neighbors = len(list(filter(lambda x : color(x) == alive_color, 
                                          filter(lambda x : x != None, directions))))
            if num_live_neighbors not in [2,3] and color(square) == alive_color: # alive
                temp[i][j] = (square[0], square[1], dead_color)
            elif num_live_neighbors == 3 and color(square) == dead_color: # dead
                temp[i][j] = (square[0], square[1], alive_color)

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

    if not pause:
        screen.fill(dead_color)

        squares = update(squares)

        # fill in squares
        for row in squares:
            for square in row:
                color = square[2]
                pos = p1, p2 = square[0], square[1]
                screen.fill(color, (pos, (scale, scale)))

        clock.tick(move_fps)

    if pause:
        # check for mouse clicks
        location = None
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                location = pygame.mouse.get_pos()

        # only update visual if changes made
        if location != None:
            # flip squares that have been touched
            squares = flip_square(squares, location)
            # update screen
            for row in squares:
                for square in row:
                    color = square[2]
                    pos = p1, p2 = square[0], square[1]
                    screen.fill(color, (pos, (scale, scale)))

        clock.tick(fps)


