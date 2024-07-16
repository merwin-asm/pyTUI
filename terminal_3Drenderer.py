import os
import time
import random
from terminal_graphics import TerminalAscii
import termianl_3DObjects

class Terminal3DSpace:
    def __init__(self, x, y, width, height, border_color=[255,255,255], border=False, clear=True):
        if clear:
           os.system("clear")

        self.x = x
        self.y = y
        self.width =  width
        self.height = height
        self.border = border
        self.border_color = border_color
        
        self.renderer = TerminalAscii()
        self.frame_data = 
        self.frame_file = str(random.randint(0,100000000000)) + ".png"

    def edit(self, x, y, width, height, border_color=[255,255,255], border=False, clear=True):
                self.x = x
        self.y = y
        self.width =  width
        self.height = height
        self.border = border
        self.border_color = border_color

    def update(self, wait=0.15):
        self.renderer.draw_image("t.png", 10, 10, 50, 50, border=True, border_color=[255, 0, 255], colored=True)
        time.sleep(wait)

    def add_obj(obj):
        pass
