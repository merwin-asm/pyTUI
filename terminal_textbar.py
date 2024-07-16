import sys
import re
import emoji
import termios
import tty
import time
import shutil
import atexit
import threading
from sty import fg, bg, rs

class TerminalTextbar:
    """
    position can be 0/1 , 0 means on the top aka y = 0 , 1 means in the end of the terminal. ( default is 1 )
    """
    def __init__(self,position=1, suggestions = [""], data_bg_color =0,data_fg_color=0, bg_color=(0, 0, 0), fg_color = (255,255,255) , end_key = "\t", data="Test DATA : ", scroll = []):
        self.x1 = 0
        
        if position == 0:
            self.y1 = 0
        else:
            _, self.y1 = shutil.get_terminal_size()
        
        if data_bg_color == 0:
            self.data_color_bg = bg_color
        else:
            self.data_color_bg = data_bg_color
        if data_fg_color == 0:
            self.data_color_fg = fg_color
        else:
            self.data_color_fg = data_fg_color
        self.x2 = _
        self.y2 = self.y1
        self.end_key = end_key
        self.bg_color = bg_color
        self.border = False
        self.border_color = (0,0,0)
        self.fg_color = fg_color
        self.current_line_index = 0
        self.current_pos = 0
        self.delete_ = False
        self.data = data
        self.roller = [""] + scroll
        self.index = 0
        self.word_list = suggestions
        # Initialize the text field area with background color and optional border
        self.clear_text_field()

        self.input = ""
        self.initial_data(data)
    
    def initial_data(self, x):
        self.current_pos += self.char_len(x)
        sys.stdout.write(f'{bg(*self.data_color_bg)}{fg(*self.data_color_fg)}{x}{rs.all}')
        sys.stdout.flush()
        return [""]

    def is_emoji(self, char):
        return (
            (0x1F600 <= ord(char) <= 0x1F64F) or  # Emoticons
            (0x1F300 <= ord(char) <= 0x1F5FF) or  # Misc Symbols and Pictographs
            (0x1F680 <= ord(char) <= 0x1F6FF) or  # Transport and Map
            (0x1F700 <= ord(char) <= 0x1F77F) or  # Alchemical Symbols
            (0x1F780 <= ord(char) <= 0x1F7FF) or  # Geometric Shapes Extended
            (0x1F800 <= ord(char) <= 0x1F8FF) or  # Supplemental Arrows-C
            (0x1F900 <= ord(char) <= 0x1F9FF) or  # Supplemental Symbols and Pictographs
            (0x1FA00 <= ord(char) <= 0x1FA6F) or  # Chess Symbols
            (0x1FA70 <= ord(char) <= 0x1FAFF) or  # Symbols and Pictographs Extended-A
            (0x2600 <= ord(char) <= 0x26FF) or    # Miscellaneous Symbols
            (0x2700 <= ord(char) <= 0x27BF)       # Dingbats
        )

    def char_len(self, s):
        alpha_count = len(re.findall(r'[a-zA-Z]', s))
        num_count = len(re.findall(r'\d', s))
        symbol_count = len(re.findall(r'[^a-zA-Z0-9\s]', s))
        emoji_count = sum(1 for char in s if self.is_emoji(char))
        return emoji_count + num_count + symbol_count + alpha_count

    def getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            if ch == '\x1b':  # Start of an escape sequence
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    return ch + ch2 + ch3

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def move_cursor(self, x, y):
        sys.stdout.write(f'\033[{y};{x}H')
        sys.stdout.write('\033[3 q')  # Change cursor to '|'
        sys.stdout.flush()
        
    def clear_line(self, y):
        self.move_cursor(self.x1, y)
        sys.stdout.write(bg(*self.bg_color) + ' ' * (self.x2 - self.x1 + 1) + rs.bg)
        sys.stdout.flush()

    def clear_text_field(self):
        # Clear the entire text field area
        self.move_cursor(self.x1, self.y1)
        sys.stdout.write(bg(*self.bg_color) + ' ' * self.x2 + rs.bg)

        self.move_cursor(self.x1, self.y1)

    def start_input(self):
        self.move_cursor(len(self.data), self.y1)

        while True:
            ch = self.getch()

            if ch == '\x7f':  # Backspace
                if self.current_pos > len(self.data):
    
                    self.input = self.input[:-1]
                    self.current_pos -= 1
                    self.move_cursor(len(self.data) + len(self.input), self.y1 + self.current_line_index)
                    sys.stdout.write(bg(*self.bg_color) + ' ' + rs.bg)
                    self.move_cursor(len(self.data) + len(self.input), self.y1 + self.current_line_index)
                    sys.stdout.flush()
        
            elif ch == self.end_key:  # Tab
                sys.stdout.write('\033[0 q')
                break
            elif ch == self.delete_:
                return

            elif ch == "\x1b[A":
                v = self.get_roller_value(0)
                self.input = v
                self.current_pos = len(self.data) +  len(self.input)
                self.move_cursor(len(self.data), self.y1)
                sys.stdout.write(bg(*self.bg_color) + ' ' * (self.x2 - len(self.data) + 1) + rs.bg)
                self.move_cursor(len(self.data), self.y1)


                sys.stdout.write(f'{bg(*self.bg_color)}{fg(*self.fg_color)}{v}{rs.all}')
                sys.stdout.flush()
            elif ch == "\x1b[B":

                v = self.get_roller_value(1)
                self.input = v
                self.current_pos = len(self.data) + len(self.input)
                
                self.move_cursor(len(self.data), self.y1)
                sys.stdout.write(bg(*self.bg_color) + ' ' * (self.x2 - len(self.data) + 1) + rs.bg)
                self.move_cursor(len(self.data), self.y1)

                sys.stdout.write(f'{bg(*self.bg_color)}{fg(*self.fg_color)}{v}{rs.all}')
                sys.stdout.flush()
            
            elif ch == "\x1b[C":
                s = self.predict(self.input)
                if s != None:
                    self.current_pos = len(self.data) + len(s)
                    self.move_cursor(self.current_pos - len(s), self.y1)
                    sys.stdout.write(f'{bg(*self.bg_color)}{fg(*self.fg_color)}{s}{rs.all}')
                    sys.stdout.flush()
                    self.input = s


            elif ch == '\n' or ch == '\r':  # Enter
                pass

            else:
                if self.current_pos < (self.x2 - self.x1):
                    self.input =  self.input + ch
                    self.current_pos += 1
                    sys.stdout.write(f'{bg(*self.bg_color)}{fg(*self.fg_color)}{ch}{rs.all}')
                    sys.stdout.flush()

    def predict(self, prefix):
        matches = [word for word in self.word_list if word.startswith(prefix)]
        if len(matches) == 1:
            return matches[0]
        return None

    def get_roller_value(self, direction):
        if direction == 0:
            self.index = (self.index + 1) % len(self.roller)
        elif direction == 1:
            self.index = (self.index - 1) % len(self.roller)
        
        return self.roller[self.index]

    def get_input(self):
        self.start_input()
        return self.input

    def delete(self):
        sys.stdout.write('\033[0 q')
        self.delete_ = True
        return self.input

if __name__ == "__main__":
    import os

    init_data = "Select the file : "
    
    textbar = TerminalTextbar(data= init_data,data_bg_color = (95, 245, 105), scroll=os.listdir(), suggestions=os.listdir())
    
    print(textbar.get_input())

