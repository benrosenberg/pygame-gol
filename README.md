# pygame-gol
Conway's Game of Life in Python using pygame.

NOTE: the implementation in `gol.py` is a really naive implementation which iterates through every square on the screen each generation. A more efficient implementation can be found in `gol_efficient.py`, which only checks the squares which are currently alive, and the set of neighbors of all those squares.

# instructions

 - Modify constants (colors, window size, scale, speed, etc.) in `gol.py` or `gol_efficient.py` as desired
 - Run with `python gol.py` or `python gol_efficient.py`
 - Hit space to pause
   + When paused, use the left mouse button (or click and drag, in `gol_efficient.py`) to toggle squares
   + Hit space to unpause and see what happens!
 - Quit with 'q' or Escape

`gol_efficient.py` only:

 - Clear (and pause) with 'c'
 - Left/Right arrows increase/decrease framerate
 - Up/Down arrows increase/decrease scaling
