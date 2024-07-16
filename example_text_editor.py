import terminal_textfield as tf
import shutil
import os
import sys
from sty import rs, bg
initial_data = ""
filename = sys.argv[1]
if os.path.exists(filename):
    f = open(filename, "r")
    initial_data += f.read()
    f.close()
x, y = shutil.get_terminal_size()
tf =  tf.TerminalTextfield(0, 0, x, y, bg_color=(18, 43, 54),initial_data=initial_data)
data = tf.get_input()
os.system("clear")
f = open(filename, "w")
f.write(data)
f.close()
print(f"Saved - {len(data)} Bytes")
