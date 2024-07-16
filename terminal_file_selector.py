import os
import sys
import tty
import termios
import shutil
from sty import fg, bg, rs

class TerminalFileSelector:
    def __init__(self, fg_color=[255, 255, 255], bg_color_on=[0, 0, 255], dir_=None):
        self.fg_color = fg_color
        self.bg_color_on = bg_color_on

        if dir_ == None:
            self.cwd = os.getcwd()
        else:
            self.cwd =  dir_

        self.selected_index = 0
        self.files = []
        self.original_settings = termios.tcgetattr(sys.stdin)
        self.rows, self.columns = shutil.get_terminal_size()

    def _getch(self):
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

    def _clear_screen(self):
        sys.stdout.write("\033[2J")
        sys.stdout.flush()

    def _move_cursor(self, x, y):
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()

    def _render(self):
        self._clear_screen()
        sys.stdout.write(fg(*self.fg_color))
        sys.stdout.write(f"Current Directory: {self.cwd}\n\n")
        row_length = max(len(filename) for filename in self.files) + 2
        num_columns = self.columns // row_length
        for i, filename in enumerate(self.files):
            row = i // num_columns
            col = i % num_columns
        
            self._move_cursor(col * row_length, row + 3)
            if self.selected_index == i:
                sys.stdout.write(f"{bg(*self.bg_color_on)}{filename:<{row_length - 1}}{bg.rs}")
            else:
                sys.stdout.write(f"{filename:<{row_length - 1}}")
        sys.stdout.flush()

    def _handle_input(self):
        while True:
            ch = self._getch()

            if ch == '\x1b[A':  # Up arrow key
                if self.selected_index > 0:
                    self.selected_index -= 1
                    self._render()

            elif ch == '\x1b[B':  # Down arrow key
                if self.selected_index < len(self.files) - 1:
                    self.selected_index += 1
                    self._render()

            elif ch == '\r':  # Enter key
                return os.path.join(self.cwd, self.files[self.selected_index])

            elif ch == '\x03':  # Ctrl+C to exit
                self._exit_selector()
                break

    def _update_files(self):
        self.files = [filename for filename in os.listdir(self.cwd) if os.path.isfile(os.path.join(self.cwd, filename))]
        self.selected_index = min(self.selected_index, len(self.files) - 1)

    def _exit_selector(self):
        self._clear_screen()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.original_settings)
        print(rs.all, end='')

    def select_file(self):
        self._update_files()
        self._render()
        return self._handle_input()

# Example usage
if __name__ == "__main__":
    selector = TerminalFileSelector()
    selected_file = selector.select_file()
    print(f"Selected file: {selected_file}")
