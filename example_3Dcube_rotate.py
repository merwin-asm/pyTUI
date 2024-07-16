from terminal_3DObjects import Cuboid
import terminal_3Dcombiner
from terminal_graphics import TerminalAscii
import terminal_utils


import time

x = 0
y = 0
z = 0


while True:
    cuboid = Cuboid("cuboid.png", 100, 100, (0, 255, 0), (255, 0, 0), True, (0, 0, 0), (0, 0, 255), x, y, z)
    cuboid.draw(100, 50, 150)

    ascii_art = TerminalAscii()
    ascii_art.draw_image("cuboid.png", 10, 10, 100, 100, border=True, border_color=[255, 0, 255], colored=True)
    
    
    x+=10
    y+=10
    z+=10
     
    if x == 1000:
        break
