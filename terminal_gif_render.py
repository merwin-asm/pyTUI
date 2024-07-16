import time
from PIL import Image
from terminal_graphics import TerminalAscii as AsciiArt
import os

class GifRenderer:
    def __init__(self, gif_path, x=0, y=0, width=80, height=40, border=False, border_color=[255, 255, 255]):
        self.gif_path = gif_path
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border = border
        self.border_color = border_color
        self.ascii_art = AsciiArt()
        self.running = False

    def _convert_to_rgb(self, image):
        if image.mode == 'P':
            image = image.convert('RGB')
        return image

    def _render_frame(self, image):
        # Convert to RGB mode if necessary
        image = self._convert_to_rgb(image)
        
        # Resize image to fit within specified width and height
        resized_image = image.resize((self.width, self.height), Image.ANTIALIAS)
        
        # Save resized image as temporary file
        img_path = os.path.join(os.getcwd(), 'temp_frame.jpg')
        resized_image.save(img_path)
        
        # Draw the image using AsciiArt class
        self.ascii_art.draw_image(img_path, self.x, self.y, self.width, self.height, colored=True,border=self.border, border_color=self.border_color)

    def render_gif(self):
        gif = Image.open(self.gif_path)
        gif.seek(0)
        self.running = True

        while self.running:
            try:
                self._render_frame(gif.copy())
                time.sleep(gif.info['duration'] / 1000.0)
                gif.seek(gif.tell() + 1)
            except EOFError:
                gif.seek(0)

    def __del__(self):
        os.system("clear")

# Usage example:
gif_path = "example.gif"
gif_renderer = GifRenderer(gif_path, x=10, y=10, width=100, height=60, border=True, border_color=[255, 0, 0])
gif_renderer.render_gif()

