# terminal_utils.py

from sty import fg, RgbFg
import atexit
import sys
import os

PREV_FONT_SIZE = None
FONT = 'Monospace size'


def clear_terminal():
    os.system("clear")
def print_color(text, color):
    """
    Prints text in the specified RGB color.

    :param text: The text to be printed.
    :param color: A list or tuple of three integers (r, g, b).
    """
    r, g, b = color
    colored_text = f"{fg(r, g, b)}{text}{fg.rs}"
    sys.stdout.write(colored_text)
    sys.stdout.flush()

def set_cursor(x, y):
    """
    Sets the cursor position in the terminal.

    :param x: The x-coordinate (column).
    :param y: The y-coordinate (row).
    """
    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()
def set_back_font_size():

    os.system(f"gsettings set org.gnome.desktop.interface monospace-font-name {PREV_FONT_SIZE}")
    print("..SETING BAK ", PREV_FONT_SIZE)
def set_font_size(size):
    global PREV_FONT_SIZE
    os.system("gsettings get org.gnome.desktop.interface monospace-font-name > .terminal.fontsize.before")
    f = open(".terminal.fontsize.before", "r")
    PREV_FONT_SIZE = f.read().replace("\n", "")
    f.close()
    
    os.system(f"gsettings set org.gnome.desktop.interface monospace-font-name '{FONT.replace('size', str(size))}'")
    
    atexit.register(set_back_font_size)
