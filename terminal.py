import os
import sys
import time

class Terminal:
    ESC = "\x1b"

    def __init__(self):
        pass

    def set_bg(self, color):
        rgb = self._convert_color(color)
        sys.stdout.write(f"{self.ESC}[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m")
        sys.stdout.flush()

    def set_cursor(self, x, y):
        sys.stdout.write(f"{self.ESC}[{y};{x}H")
        sys.stdout.flush()

    def text(self, text, fg_, bg_):
        fg_color = self._convert_color(fg_)
        bg_color = self._convert_color(bg_)
        sys.stdout.write(f"{self.ESC}[38;2;{fg_color[0]};{fg_color[1]};{fg_color[2]}m")
        sys.stdout.write(f"{self.ESC}[48;2;{bg_color[0]};{bg_color[1]};{bg_color[2]}m")
        sys.stdout.write(text)
        sys.stdout.write(f"{self.ESC}[0m")
        sys.stdout.flush()

    def draw_rect(self, x, y, width, height, color, filled=True):
        color_rgb = self._convert_color(color)
        self.set_cursor(x, y)
        for i in range(height):
            self.set_cursor(x, y + i)
            for j in range(width):
                sys.stdout.write(f"{self.ESC}[48;2;{color_rgb[0]};{color_rgb[1]};{color_rgb[2]}m ")
            sys.stdout.write(f"{self.ESC}[0m")
            sys.stdout.flush()

    def draw_circle(self, x, y, diameter, color):
        # Simplified version of a circle, more of a rough oval representation
        radius = diameter // 2
        for i in range(diameter):
            for j in range(diameter):
                if (i - radius)**2 + (j - radius)**2 < radius**2:
                    self.set_cursor(x + j, y + i)
                    self.draw_pixel(x,y,color)

    def draw_line(self, x1, y1, x2, y2, color):
        color_rgb = self._convert_color(color)
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        x_inc = dx / steps
        y_inc = dy / steps
        x, y = x1, y1
        for _ in range(steps):
            self.set_cursor(int(round(x)), int(round(y)))
            sys.stdout.write(f"{self.ESC}[48;2;{color_rgb[0]};{color_rgb[1]};{color_rgb[2]}m ")
            sys.stdout.write(f"{self.ESC}[0m")
            x += x_inc
            y += y_inc
        sys.stdout.flush()

    def draw_pixel(self, x, y, color):
        color_rgb = self._convert_color(color)
        self.set_cursor(x, y)
        sys.stdout.write(f"{self.ESC}[48;2;{color_rgb[0]};{color_rgb[1]};{color_rgb[2]}m ")
        sys.stdout.write(f"{self.ESC}[0m")
        sys.stdout.flush()

    def clear_terminal(self):
        sys.stdout.write(f"{self.ESC}[2J")
        sys.stdout.flush()

    def _convert_color(self, color_string):
        color_list = color_string.split(",")
        color = []
        for c in color_list:
            color.append(int(c))
        return color

    # Example functions to handle events (placeholders)
    def handle_event(event):
        print(f"Terminal event: {event}")

    def handle_keypress(key):
        print(f"Key pressed: {key}")

