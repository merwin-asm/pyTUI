import sys
import termios
import tty
import time
import shutil
import atexit
import threading
from sty import fg, bg, rs

class TerminalTextinput:
    def __init__(self, x, y, width, bg_color=(0, 0, 0),end_key = "\t", border=False, border_color=(255, 255, 255), initial_data=""):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width 
        self.y2 = y
        self.end_key = end_key
        self.bg_color = bg_color
        self.border = border
        self.border_color = border_color
        self.current_line_index = 0
        self.current_pos = 0
        self.delete_ = False
        
        # Initialize the text field area with background color and optional border
        self.clear_text_field()

        self.input_lines =  self.initial_data(initial_data)
    
    def initial_data(self, x):
        data = []
        for e in x.split("\n"):
            data.append(e)

        for ch in x:
            if ch == '\n' or ch == '\r':  # Enter
                pass

            if self.current_pos < (self.x2 - self.x1):
                self.current_pos += 1
                sys.stdout.write(f'{bg(*self.bg_color)}{fg.white}{ch}{rs.all}')
                sys.stdout.flush()

            else:  # If the line is full, move to the next line if there is space
                if self.current_line_index < (self.y2 - self.y1):
                    self.current_line_index += 1
                    self.current_pos = 1
                    self.move_cursor(self.x1 + self.current_pos, self.y1 + self.current_line_index)
                    sys.stdout.write(f'{bg(*self.bg_color)}{fg.white}{ch}{rs.all}')
                    sys.stdout.flush()

        return [x]

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
        sys.stdout.write('\033[5 q')  # Change cursor to '|'
        sys.stdout.flush()
        
    def clear_line(self, y):
        self.move_cursor(self.x1, y)
        sys.stdout.write(bg(*self.bg_color) + ' ' * (self.x2 - self.x1 + 1) + rs.bg)
        sys.stdout.flush()

    def clear_text_field(self):
        # Clear the entire text field area
        for y in range(self.y1, self.y2 + 1):
            self.move_cursor(self.x1, y)
            sys.stdout.write(bg(*self.bg_color) + ' ' * (self.x2 - self.x1 + 1) + rs.bg)

        # Draw optional border
        if self.border and self.x1 > 0 and self.y1 > 0:
            # Draw top border
            self.move_cursor(self.x1, self.y1 - 1)
            sys.stdout.write(bg(*self.border_color) + ' ' * (self.x2 - self.x1 + 1) + rs.bg)
            
            # Draw bottom border
            self.move_cursor(self.x1, self.y2 + 1)
            sys.stdout.write(bg(*self.border_color) + ' ' * (self.x2 - self.x1 + 1) + rs.bg)

            # Draw left and right borders for each line
            for y in range(self.y1, self.y2 + 1):
                if self.x1 <= 0:
                    pass
                else:
                    self.move_cursor(self.x1 - 1, y)
                    sys.stdout.write(bg(*self.border_color) + ' ' + rs.bg)
                
                columns, _ = shutil.get_terminal_size()

                if self.x2 >= columns:
                    pass
                else:
                    self.move_cursor(self.x2 + 1, y)
                    sys.stdout.write(bg(*self.border_color) + ' ' + rs.bg)

        self.move_cursor(self.x1, self.y1)

    def start_input(self):
        self.move_cursor(self.x1, self.y1)

        while True:
            ch = self.getch()

            if ch == '\x7f':  # Backspace
                if self.current_pos > 0:
                    self.input_lines[self.current_line_index] = (
                        self.input_lines[self.current_line_index][:self.current_pos - 1] +
                        self.input_lines[self.current_line_index][self.current_pos:]
                    )
                    self.current_pos -= 1
                    self.move_cursor(self.x1 + self.current_pos, self.y1 + self.current_line_index)
                    sys.stdout.write(bg(*self.bg_color) + ' ' + rs.bg)
                    self.move_cursor(self.x1 + self.current_pos, self.y1 + self.current_line_index)
                    sys.stdout.flush()
                elif self.current_line_index > 0:
                    self.current_line_index -= 1
                    self.current_pos = len(self.input_lines[self.current_line_index])
                    self.move_cursor(self.x1 + self.current_pos, self.y1 + self.current_line_index)
            elif ch == self.end_key:  # Tab
                sys.stdout.write('\033[0 q')
                break
            elif ch == self.delete_:
                return

            elif ch == "\x1b[D":
                if self.current_pos > 1:
                    self.current_pos -= 1
                    self.move_cursor(self.x1 + self.current_pos, self.y1 + self.current_line_index)
            elif ch == "\x1b[C":
                if self.current_pos < self.x2:
                    self.current_pos += 1
                    self.move_cursor(self.x1 + self.current_pos, self.y1 + self.current_line_index)

            elif ch == '\n' or ch == '\r':  # Enter
                pass
            else:
                if self.current_pos < (self.x2 - self.x1):
                    self.input_lines[self.current_line_index] = (
                        self.input_lines[self.current_line_index][:self.current_pos] + ch +
                        self.input_lines[self.current_line_index][self.current_pos:]
                    )
                    self.current_pos += 1
                    sys.stdout.write(f'{bg(*self.bg_color)}{fg.white}{ch}{rs.all}')
                    sys.stdout.flush()
                else:  # If the line is full, move to the next line if there is space
                    if self.current_line_index < (self.y2 - self.y1):
                        self.input_lines.append(ch)
                        self.current_line_index += 1
                        self.current_pos = 1
                        self.move_cursor(self.x1 + self.current_pos, self.y1 + self.current_line_index)
                        sys.stdout.write(f'{bg(*self.bg_color)}{fg.white}{ch}{rs.all}')
                        sys.stdout.flush()

    def get_input(self):
        self.start_input()
        return '\n'.join(self.input_lines)

    def delete(self):
        sys.stdout.write('\033[0 q')
        self.delete_ = True
        return '\n'.join(self.input_lines)

if __name__ == "__main__":
    textinput = TerminalTextinput(10,2, 10, (100,100,100))
    print(textinput.get_input())

