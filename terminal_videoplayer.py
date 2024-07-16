import cv2
import time
import threading
import ffmpeg
from PIL import Image
from terminal_graphics import TerminalAscii as AsciiArt
import pygame
from pynput import keyboard
import os
import atexit


class VideoRender:
    def __init__(self, video_path, colored=True, x=0, y=0, width=80, height=40,skip_frame_rate=25, border=False, border_color=[255, 255, 255], show_timeline=False, played_color=[0, 255, 0], unplayed_color=[255, 0, 0]):
    
        self.video_path = video_path
        self.colored = colored
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border = border
        self.border_color = border_color
        self.show_timeline = show_timeline
        self.played_color = played_color
        self.unplayed_color = unplayed_color
        self.ascii_art = AsciiArt()
        self.cap = cv2.VideoCapture(video_path)
        self.audio_file = None
        self.already_played = 0
        self.audio_position = 0
        self.target_fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_duration = 1 / self.target_fps
        self.paused = False
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_frame = 0
        self.skip_frame_rate = skip_frame_rate


        atexit.register(self._exit)
    

    def _exit(self):
        os.system("clear")

    def _extract_audio(self):
        # Extract audio from video file
        audio_path = os.path.join(os.getcwd(), 'audio.wav')
    
        ffmpeg.input(self.video_path).output(audio_path).run(overwrite_output=True)
        return audio_path

    def _load_audio(self):
        audio_path = self._extract_audio()
        self.audio_file = audio_path

    def _play_audio(self):
        pygame.mixer.init()
        pygame.mixer.music.load(self.audio_file)

        while True:
            if not self.paused:
                if self.already_played == 0:
                    pygame.mixer.music.play(start=self.audio_position / 1000.0)
                    self.already_played = 1
                else:
                    pygame.mixer.music.unpause()
                while pygame.mixer.music.get_busy() and not self.paused:
                    #self.audio_position =pygame.mixer.music.get_pos()
                    
                    pygame.time.Clock().tick(10)  # adjust tick as needed
            else:
                
                #self.alread_played += pygame.mixer.music.get_pos()
                pygame.mixer.music.pause()
                pygame.time.Clock().tick(10)  # adjust tick as needed
                self.audio_position = pygame.mixer.music.get_pos()
    def _start_audio(self):
        self.audio_thread = threading.Thread(target=self._play_audio)
        self.audio_thread.start()

    def _pause_audio(self):
        self.paused = True

    def _resume_audio(self):
        self.paused = False

    def _close_audio(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    def _render_frame(self, frame):
        # Convert the frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Save frame as an image
        img_path = os.path.join(os.getcwd(), 'frame.jpg')
        Image.fromarray(frame).save(img_path)
        # Draw the image using AsciiArt class
        self.ascii_art.draw_image(img_path, self.x, self.y, self.width, self.height, border=self.border, border_color=self.border_color, colored=self.colored)

    def _draw_timeline(self, current_frame, total_frames):
        timeline_length = self.width - 4
        played_length = int((current_frame / total_frames) * timeline_length) 
        timeline = "[" + "#" * played_length + "-" * (timeline_length - played_length) + "]"
        
        played_color_str = f"\033[38;2;{self.played_color[0]};{self.played_color[1]};{self.played_color[2]}m"
        unplayed_color_str = f"\033[38;2;{self.unplayed_color[0]};{self.unplayed_color[1]};{self.unplayed_color[2]}m"
        reset_color = "\033[0m"

        print(f"\033[{self.y + self.height +1 };{self.x + 4}H" + played_color_str + "#" * played_length + unplayed_color_str + "-" * (timeline_length - played_length) + reset_color)
    def __draw_timeline(self, x, y):
        print(x, y)
        progress = x / y
        num_completed_dots = int(progress * (self.width -4))
        num_remaining_dots = self.width -4 - num_completed_dots
        progress_bar = '[' + '.' * num_completed_dots + ' ' * num_remaining_dots + ']'
        print(f'\r{progress_bar}', end='', flush=True)

    def _draw_play_pause_button(self):
        button = "⣿\t" if not self.paused else "▶\t"
        print(f"\033[{self.y + self.height + 1};{self.x}H{button}")

    def _toggle_pause(self, key):
        if key == keyboard.Key.space:
            self.paused = not self.paused
            self._draw_play_pause_button()

    def render_video(self):
        if not self.cap.isOpened():
            print("Error: Could not open video file.")
            return

        self._load_audio()
        self._start_audio()

        # Keyboard listener for pause and resume
        listener = keyboard.Listener(on_press=self._toggle_pause)
        listener.start()

        os.system("clear")
        
        # Draw the initial play/pause button
        self._draw_play_pause_button()
        
        while self.cap.isOpened():

            if self.paused:
                time.sleep(0.1)
                continue

            ret, frame = self.cap.read()
            self.current_frame += 1 + self.skip_frame_rate
            
            if not ret:
                break

            self._render_frame(frame)
            for e in range(0, self.skip_frame_rate):
                wdfwer, wedf = self.cap.read()
            if self.show_timeline:
                self._draw_timeline(self.current_frame, self.total_frames)


        self.cap.release()
        listener.stop()

        # Close audio playback
        self._close_audio()

# Usage example:
video_path = "test.mp4"
video_renderer = VideoRender(video_path, colored=True, x=30, y=10, width=80, height=40, border=True, border_color=[255, 0, 0], show_timeline=True, played_color=[0, 255, 0], unplayed_color=[255, 0, 0])
video_renderer.render_video()

