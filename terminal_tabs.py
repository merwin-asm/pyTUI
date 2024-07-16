import os
import sys
import tty
import termios
import threading
import time
from sty import fg, bg, rs

class Tab:
    def __init__(self, tab_id, name, fg_color, bg_color, fg_open, bg_open, tab_function=None):
        self.tab_id = tab_id
        self.name = name
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.fg_open = fg_open
        self.bg_open = bg_open
        self.content = ""
        self.cursor_pos = (0, 0)
        self.tab_function = tab_function
        self.thread = None
        self.active_event = threading.Event()

    def write(self, *args, sep='', end='\n'):
        text = sep.join(map(str, args)) + end
        self.content += text

    def start_tab_function(self):
        if self.tab_function and not self.thread:
            self.active_event.set()
            self.thread = threading.Thread(target=self._run_tab_function)
            self.thread.start()

    def stop_tab_function(self):
        if self.thread:
            self.active_event.clear()
            self.thread.join()
            self.thread = None

    def _run_tab_function(self):
        self.tab_function(self)

class TabularTerminal:
    def __init__(self, change_tab_key='tab', size=1):
        self.change_tab_key = change_tab_key
        self.size = size
        self.tabs = []
        self.current_tab_index = 0
        self.original_settings = termios.tcgetattr(sys.stdin)
        self.running = True

    def _getch(self):
        tty.setraw(sys.stdin)
        ch = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.original_settings)
        return ch

    def add_tab(self, name, fg_color, bg_color, fg_open, bg_open, tab_function=None):
        tab_id = len(self.tabs)
        tab = Tab(tab_id, name, fg_color, bg_color, fg_open, bg_open, tab_function)
        tab.cursor_pos = (0, self.size+1)
        self.tabs.append(tab)
        self._render_tabs()
        if len(self.tabs) == 1:
            self.current_tab_index = 0
            try:
                self.tabs[self.current_tab_index].start_tab_function()
            except:
                pass
            self._render_tabs()

        return tab_id

    def remove_tab(self, tab_id):
        if tab_id == self.tabs[self.current_tab_index].tab_id:
            self.tabs[self.current_tab_index].stop_tab_function()
        self.tabs = [tab for tab in self.tabs if tab.tab_id != tab_id]
        if self.current_tab_index >= len(self.tabs):
            self.current_tab_index = 0
        self._render_tabs()

    def close_current(self):
        if self.tabs:
            self.remove_tab(self.tabs[self.current_tab_index].tab_id)

    def close_tabular(self):
        self.running = False
        self._clear_screen()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.original_settings)
        print(rs.all, end='')

    def _clear_screen(self):
        os.system("clear")

    def _move_cursor(self, x, y):
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()

    def _render_tabs(self):
        self._clear_screen()
        for line in range(self.size):
            for i, tab in enumerate(self.tabs):
                if i == self.current_tab_index:
                    sys.stdout.write(bg(*tab.bg_open) + fg(*tab.fg_open))
                else:
                    sys.stdout.write(bg(*tab.bg_color) + fg(*tab.fg_color))
                if line == 0 and self.size == 1:
                    sys.stdout.write(' ' +tab.name + ' ')
                elif line == 0 and self.size == 2:
                    sys.stdout.write(" "*(len(tab.name)+2))
                elif line == 0 and self.size == 3:
                    sys.stdout.write(" "*(len(tab.name)+2))
                elif line == 1 and self.size == 2:
                    sys.stdout.write(' ' +tab.name + ' ')
                elif line == 1 and self.size == 3:
                    sys.stdout.write(' ' +tab.name + ' ')
                elif line == 2 and self.size == 3:
                    sys.stdout.write(" "*(len(tab.name)+2))
                else:
                    sys.stdout.write(' ' * (len(tab.name) + 2))
                sys.stdout.write(rs.all)
        sys.stdout.flush()
        
        self._move_cursor(*self.tabs[self.current_tab_index].cursor_pos)
        sys.stdout.write(self.tabs[self.current_tab_index].content)
        sys.stdout.flush()
    

    def _handle_input(self):
        while self.running:
            ch = self._getch()
            if ch == '\t':  # Tab key
                self._change_tab()
            elif ch == '\x03':  # Ctrl+C
                self.close_tabular()
                break

    def _change_tab(self):
        self.tabs[self.current_tab_index].stop_tab_function()
        self.current_tab_index = (self.current_tab_index + 1) % len(self.tabs)
        try:
            self.tabs[self.current_tab_index].start_tab_function()
        except:
            pass
        self._render_tabs()

    def _get_cursor_position(self):
        sys.stdout.write("\033[6n")
        sys.stdout.flush()
        pos = ''
        while True:
            ch = self._getch()
            if ch == 'R':
                break
            pos += ch
        try:
            _, coords = pos.split('[')
            y, x = coords.split(';')
            return int(x), int(y)
        except ValueError:
            return 1, 1

    def run(self):
        self._render_tabs()
        self._handle_input()


# Example usage
def tab_function_example(s):
    while s.active_event.is_set():
        time.sleep(1)
        print("Tab function running...")
        time.sleep(1)
if __name__ == "__main__":
    tabular = TabularTerminal(size=1)

    tab1 = tabular.add_tab("Home", [255, 255, 255], [0, 0, 255], [255, 255, 255], [0, 0, 0], tab_function_example)
    tab2 = tabular.add_tab("Settings", [255, 255, 255], [0, 255, 0], [255, 255, 255], [0, 0, 0])

    try:
        tabular.run()
    except KeyboardInterrupt:
        tabular.close_tabular()
