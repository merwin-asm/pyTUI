import math
from PIL import Image
from sty import fg, bg, rs
import terminal_utils

class TerminalAscii:
    def __init__(self):
        terminal_utils.set_font_size(5)
        

    def set_cursor(self, x, y):
        terminal_utils.set_cursor(x, y)

    def print_color(self, text, color):
        terminal_utils.print_color(text, color)

    def draw_line(self, x1, y1, x2, y2, color):
        if x1 == x2:  # Vertical line
            for y in range(min(y1, y2), max(y1, y2) + 1):
                self.set_cursor(x1, y)
                self.print_color('|', color)
        elif y1 == y2:  # Horizontal line
            for x in range(min(x1, x2), max(x1, x2) + 1):
                self.set_cursor(x, y1)
                self.print_color('—', color)
        else:
            # For simplicity, we handle only vertical and horizontal lines
            raise NotImplementedError("Only vertical and horizontal lines are supported.")

    def draw_rectangle(self, x, y, width, height, color, filled=False):
        if filled:
            for i in range(y, y + height):
                for j in range(x, x + width):
                    self.set_cursor(j, i)
                    self.print_color('#', color)
        else:
            # Top and bottom sides
            self.draw_line(x, y, x + width - 1, y, color)
            self.draw_line(x, y + height - 1, x + width - 1, y + height - 1, color)
            # Left and right sides
            self.draw_line(x, y, x, y + height - 1, color)
            self.draw_line(x + width - 1, y, x + width - 1, y + height - 1, color)

    def draw_oval(self, x, y, width, height, color, filled=False):
        a = width // 2
        b = height // 2
        xc = x + a
        yc = y + b

        if filled:
            for i in range(y, y + height):
                for j in range(x, x + width):
                    if ((j - xc)**2 / a**2) + ((i - yc)**2 / b**2) <= 1:
                        self.set_cursor(j, i)
                        self.print_color('*', color)
        else:
            for theta in range(0, 360):
                rad = math.radians(theta)
                x_pos = xc + int(a * math.cos(rad))
                y_pos = yc + int(b * math.sin(rad))
                self.set_cursor(x_pos, y_pos)
                self.print_color('*', color)

    def draw_circle(self, x, y, radius, color, filled=False):
        self.draw_oval(x - radius, y - radius, 2 * radius, 2 * radius, color, filled)
    
    def draw_image(self, image_path, x, y, width, height, border=False, border_color=[255, 255, 255], colored=False):
        # Load the image
        img = Image.open(image_path)
        # Resize the image
        img = img.resize((width, height))
        # Convert the image to RGB if needed
        if colored:
            img = img.convert('RGB')
        else:
            img = img.convert('L')

        # ASCII characters by density
        ascii_chars = "@%#*+=-:. "

        for i in range(height):
            for j in range(width):
                if colored:
                    r, g, b = img.getpixel((j, i))
                    brightness = (0.299*r + 0.587*g + 0.114*b)
                    self.set_cursor(x + j, y + i)
                    #self.print_color(ascii_char, [r, g, b])
                    print(f"{bg(r,g,b)} {bg.rs}", end="")
                else:
                    pixel = img.getpixel((j, i))
                    ascii_char = ascii_chars[pixel // 32]
                    self.set_cursor(x + j, y + i)
                    self.print_color(ascii_char, [255, 255, 255])

        if border:
            self.draw_rectangle(x - 1, y - 1, width + 2, height + 2, border_color, filled=False)

if __name__ == "__main__":
    # Usage example:
    ascii_art = TerminalAscii()
    """
    ascii_art.draw_line(10, 5, 10, 15, [255, 0, 0])  # Vertical red line
    ascii_art.draw_line(20, 5, 30, 5, [0, 255, 0])  # Horizontal green line
    ascii_art.draw_rectangle(5, 5, 10, 5, [0, 0, 255], filled=False)  # Blue unfilled rectangle
    ascii_art.draw_rectangle(5, 15, 10, 5, [0, 0, 255], filled=True)  # Blue filled rectangle
    ascii_art.draw_circle(40, 10, 5, [255, 255, 0], filled=False)  # Yellow unfilled circle
    ascii_art.draw_circle(60, 10, 5, [255, 255, 0], filled=True)  # Yellow filled circle
    ascii_art.draw_oval(50, 5, 8, 4, [255, 0, 255], filled=False)  # Magenta unfilled oval
    ascii_art.draw_oval(70, 5, 8, 4, [255, 0, 255], filled=True)  # Magenta filled oval
    """
    ascii_art.draw_image("t.png", 10, 10, 50, 50, border=True, border_color=[255, 0, 255], colored=True)  # Adjust path, width, and height as needed
    import time
    time.sleep(10)
