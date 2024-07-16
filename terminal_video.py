import cv2
import time
import threading
import ffmpeg
from PIL import Image
from terminal_graphics import TerminalAscii as AsciiArt
import simpleaudio as sa
import keyboard


class VideoRender:
    def __init__(self, video_path, colored=True, x=0, y=0, width=80, height=40, border=False, border_color=[255, 255, 255]):
        self.video_path = video_path
        self.colored = colored
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.border = border
        self.border_color = border_color
        self.ascii_art = AsciiArt()
        self.cap = cv2.VideoCapture(video_path)
        self.audio_thread = None
        self.audio = None
        self.target_fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_duration = 1 / self.target_fps
    
    def _play_audio(self):
        # Extract audio from video file
        audio_path = '/tmp/audio.wav'
        ffmpeg.input(self.video_path).output(audio_path).run(overwrite_output=True)
        # Play the extracted audio
        wave_obj = sa.WaveObject.from_wave_file(audio_path)
        self.audio = wave_obj.play()
        self.audio.wait_done()

    def _render_frame(self, frame):
        # Convert the frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Save frame as an image
        img_path = "/tmp/frame.jpg"
        Image.fromarray(frame).save(img_path)
        # Draw the image using AsciiArt class
        self.ascii_art.draw_image(img_path, self.x, self.y, self.width, self.height, border=self.border, border_color=self.border_color, colored=self.colored)

    def render_video(self):
        if not self.cap.isOpened():
            print("Error: Could not open video file.")
            return

        # Start the audio in a separate thread
        self.audio_thread = threading.Thread(target=self._play_audio)
        self.audio_thread.start()

        while self.cap.isOpened():
            start_time = time.time()
            ret, frame = self.cap.read()

            if not ret:
                break

            self._render_frame(frame)

            elapsed_time = time.time() - start_time
            time_to_wait = self.frame_duration - elapsed_time

            if time_to_wait > 0:
                time.sleep(time_to_wait)

        self.cap.release()
        
class VideoPlayer:
    def __init__(self, video_path, colored=True, x=0, y=0, width=80, height=40, border=False, border_color=[255, 255, 255], show_timeline=False, played_color=[0, 255, 0], unplayed_color=[255, 0, 0]):
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
        self.audio_thread = None
        self.audio = None
        self.target_fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.frame_duration = 1 / self.target_fps
        self.paused = False

    def _play_audio(self):
        # Extract audio from video file
        audio_path = '/tmp/audio.wav'
        ffmpeg.input(self.video_path).output(audio_path).run(overwrite_output=True)
        # Play the extracted audio
        wave_obj = sa.WaveObject.from_wave_file(audio_path)
        self.audio = wave_obj.play()
        self.audio.wait_done()

    def _render_frame(self, frame):
        # Convert the frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Save frame as an image
        img_path = "/tmp/frame.jpg"
        Image.fromarray(frame).save(img_path)
        # Draw the image using AsciiArt class
        self.ascii_art.draw_image(img_path, self.x, self.y, self.width, self.height, border=self.border, border_color=self.border_color, colored=self.colored)

    def _draw_timeline(self, current_frame, total_frames):
        timeline_length = self.width
        played_length = int((current_frame / total_frames) * timeline_length)
        timeline = "[" + "#" * played_length + "-" * (timeline_length - played_length) + "]"
        
        played_color_str = f"\033[38;2;{self.played_color[0]};{self.played_color[1]};{self.played_color[2]}m"
        unplayed_color_str = f"\033[38;2;{self.unplayed_color[0]};{self.unplayed_color[1]};{self.unplayed_color[2]}m"
        reset_color = "\033[0m"

        print(self.x * " " + played_color_str + "#" * played_length + unplayed_color_str + "-" * (timeline_length - played_length) + reset_color)

    def render_video(self):
        if not self.cap.isOpened():
            print("Error: Could not open video file.")
            return

        # Total number of frames
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Start the audio in a separate thread
        self.audio_thread = threading.Thread(target=self._play_audio)
        self.audio_thread.start()

        # Keyboard listener for pause and resume
        def toggle_pause(event):
            if event.name == 'space':
                self.paused = not self.paused

        keyboard.on_press(toggle_pause)

        current_frame = 0

        while self.cap.isOpened():
            start_time = time.time()

            if self.paused:
                time.sleep(0.1)
                continue

            ret, frame = self.cap.read()
            current_frame += 1

            if not ret:
                break

            self._render_frame(frame)

            if self.show_timeline:
                self._draw_timeline(current_frame, total_frames)

            elapsed_time = time.time() - start_time
            time_to_wait = self.frame_duration - elapsed_time

            if time_to_wait > 0:
                time.sleep(time_to_wait)

        self.cap.release()

def main():
    # Usage example:
    import time

    x =  time.time()
    video_path = "test.mp4"
    video_renderer = VideoRender(video_path, colored=True, x=25, y=10, width=80, height=40, border=True, border_color=[255, 250, 0])
    video_renderer.render_video()
    print("TOTAL TIME TOOK : ", x-time.time())

video_path = "test.mp4"
video_renderer = VideoPlayer(video_path, colored=True, x=0, y=0, width=80, height=40, border=True, border_color=[255, 0, 0], show_timeline=True, played_color=[0, 255, 0], unplayed_color=[255, 0, 0])
video_renderer.render_video()

