# pyTUI
TUI - Terminal User Interface | Python modules to code UI's for terminal!


`Make tabs , inputfields , inputbar , render video , have a videoplayer ,render image, render 2D objects,
render 3D Objects, select files, and more...`
<img src="https://komarev.com/ghpvc/?username=merwin-asm-pytui&label=Project%20views&color=0e75b6&style=flat" /> </p>


## Note :
  - Could change your terminal size and font etc, If it didnt change back automatically after the code exit , then make sure you know how to revert it back.
    
  - Only for linux


# Install :
```sh
git clone https://github.com/merwin-asm/pyTUI.git
pip install -r requirements.py
```

# Examples :
- example_3D_cube_rotate.py -  simple 3D cube rotation code!!
- example_text_editor.py -  simple text editor!!

# Documentation

### terminal.Terminal Class
- The Terminal class provides functionalities to control terminal output appearance and positioning using ANSI escape sequences in Python.

| Method              | Description                                                                                     | Parameters                                                                                                     |
|---------------------|-------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| `__init__`          | Constructor for initializing the Terminal class.                                                 | None                                                                                                           |
| `set_bg`            | Sets the background color of the terminal.                                                       | `color` (RGB string, e.g., "255,0,0")                                                                          |
| `set_cursor`        | Moves the cursor to the specified position.                                                      | `x` (column), `y` (row)                                                                                        |
| `text`              | Prints text with specified foreground and background colors.                                      | `text` (string), `fg_` (foreground RGB), `bg_` (background RGB)                                               |
| `draw_rect`         | Draws a filled rectangle at the specified position and size.                                      | `x` (left), `y` (top), `width`, `height`, `color` (RGB string), `filled` (boolean, default True)                |
| `draw_circle`       | Draws a rough circle (oval) at the specified position and diameter.                               | `x` (center), `y` (center), `diameter`, `color` (RGB string)                                                   |
| `draw_line`         | Draws a line between two points using Bresenham's algorithm.                                      | `x1`, `y1`, `x2`, `y2` (endpoints), `color` (RGB string)                                                       |
| `draw_pixel`        | Draws a single pixel at the specified position.                                                   | `x`, `y` (position), `color` (RGB string)                                                                       |
| `clear_terminal`    | Clears the terminal screen.                                                                      | None                                                                                                           |
| `_convert_color`    | Converts a string of RGB values to a list of integers.                                             | `color_string` (string, e.g., "255,0,0")                                                                       |
| `handle_event`      | Placeholder function for handling terminal events.                                                | `event` (event data)                                                                                           |
| `handle_keypress`   | Placeholder function for handling keypress events.                                                | `key` (key data)                                                                                               |

### terminal_3DObjects.py

- The terminal3DObjects module provides classes to generate and manipulate 3D shapes in a terminal

| Class      | Method             | Description                                                                                   | Parameters                                                                                                     |
|------------|--------------------|-----------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| `Shape3D`  | `__init__`         | Constructor for initializing a 3D shape with specified attributes.                            | `filename`, `height`, `width`, `shape_color`, `edge_color`, `show_edges`, `bg_color`, `fill_color`, `x_axis_rotation`, `y_axis_rotation`, `z_axis_rotation` |
|            | `create_image`     | Creates and returns a blank image of specified dimensions.                                     | None                                                                                                           |
|            | `save_image`       | Saves the provided image to a file with the specified filename.                                | `image` (numpy array)                                                                                         |
|            | `rotate_vertices`  | Rotates the vertices of the shape according to specified rotation angles.                      | `vertices` (numpy array)                                                                                      |
|            | `project_vertices` | Projects the 3D vertices onto a 2D plane for rendering.                                        | `vertices` (numpy array)                                                                                      |
|            | `draw_edges`       | Draws edges between vertices on the image.                                                      | `image` (numpy array), `vertices` (numpy array), `edges` (list of tuples)                                      |
|            | `draw_vertices`    | Draws vertices as circles on the image.                                                         | `image` (numpy array), `vertices` (numpy array)                                                                |
|            | `fill_shape`       | Fills the shape defined by vertices and faces with a specified fill color.                      | `image` (numpy array), `vertices` (numpy array), `faces` (list of tuples)                                      |
| `Cuboid`   | `draw`             | Draws a cuboid shape on the image.                                                             | `length`, `width`, `height`                                                                                   |
| `Sphere`   | `draw`             | Draws a sphere shape on the image.                                                              | `radius`, `detail` (optional, default=20)                                                                      |
| `Pyramid`  | `draw`             | Draws a pyramid shape on the image.                                                             | `base_length`, `height`                                                                                        |
| `Cylinder` | `draw`             | Draws a cylinder shape on the image.                                                            | `radius`, `height`, `detail` (optional, default=20)                                                            |

### terminal3Dcombiner.Combine Class

- adds multiple object images (cuboid, pyramid, cylinder) at different positions, and then saves the combined image

| Method                   | Description                                                                                     | Parameters                                                                                                          |
|--------------------------|-------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| `__init__`               | Constructor for initializing the Combine object with canvas dimensions and background color.   | `height`, `width`, `background_color` (RGB tuple, e.g., `(0, 0, 0)`)                                                |
| `add_obj`                | Adds an object image onto the canvas at specified coordinates, blending with the background.   | `obj_filename` (filename of object image), `x`, `y` (coordinates), `obj_bg_color` (RGB list, e.g., `[0, 0, 0]`)     |
| `save_combined_image`    | Saves the combined canvas image to a file.                                                      | `output_filename` (filename to save the combined image)                                                              |


### terminal_3Drenderer.`Terminal3DSpace` Class

#### Attributes

| Attribute          | Description                                                                                   |
|--------------------|-----------------------------------------------------------------------------------------------|
| `x`                | X-coordinate of the top-left corner of the terminal space.                                      |
| `y`                | Y-coordinate of the top-left corner of the terminal space.                                      |
| `width`            | Width of the terminal space.                                                                   |
| `height`           | Height of the terminal space.                                                                  |
| `border_color`     | RGB color values for the optional border around the terminal space.                             |
| `border`           | Boolean indicating whether to display a border around the terminal space.                       |
| `renderer`         | Instance of `TerminalAscii` used for rendering graphics on the terminal.                        |
| `frame_data`       | Placeholder for storing frame data.                                                             |
| `frame_file`       | Randomly generated filename for storing frames.                                                 |

#### Methods

| Method                               | Description                                                                                   |
|--------------------------------------|-----------------------------------------------------------------------------------------------|
| `__init__(self, x, y, width, height, border_color=[255,255,255], border=False, clear=True)`    | Initializes the `Terminal3DSpace` object with specified dimensions and optional border settings, optionally clearing the terminal screen. |
| `edit(self, x, y, width, height, border_color=[255,255,255], border=False, clear=True)`         | Modifies the dimensions and appearance parameters of the terminal space.                        |
| `update(self, wait=0.15)`            | Updates the terminal space, possibly rendering an image (`t.png` in this case) with specified attributes and waiting for a specified duration. |
| `add_obj(obj)`                       | Placeholder method for adding objects to the terminal space.                                     |

### terminal_file_selector.`TerminalFileSelector` Class

#### Attributes

| Attribute          | Description                                                                                   |
|--------------------|-----------------------------------------------------------------------------------------------|
| `fg_color`         | RGB values for the foreground color used in the terminal interface.                            |
| `bg_color_on`      | RGB values for the background color when a file is selected in the interface.                  |
| `cwd`              | Current working directory path.                                                                |
| `selected_index`   | Index of the currently selected file in the list.                                              |
| `files`            | List of files in the current directory.                                                        |
| `original_settings`| Original terminal settings before modifications for input handling.                            |
| `rows`, `columns`  | Terminal dimensions retrieved using `shutil.get_terminal_size()`.                              |

#### Methods

| Method               | Description                                                                                   |
|----------------------|-----------------------------------------------------------------------------------------------|
| `__init__(self, fg_color=[255, 255, 255], bg_color_on=[0, 0, 255], dir_=None)` | Initializes the `TerminalFileSelector` object with optional colors and directory.             |
| `_getch(self)`       | Reads a single character from input without waiting for a newline, handling escape sequences.  |
| `_clear_screen(self)`| Clears the terminal screen.                                                                   |
| `_move_cursor(self, x, y)` | Moves the cursor to the specified coordinates on the terminal.                                |
| `_render(self)`      | Renders the file selection interface on the terminal, highlighting the selected file.         |
| `_handle_input(self)`| Handles user input for navigating and selecting files in the terminal interface.              |
| `_update_files(self)`| Updates the list of files in the current directory based on user navigation.                   |
| `_exit_selector(self)`| Exits the file selector, restoring terminal settings and clearing the screen.                  |
| `select_file(self)`  | Displays the file selection interface, handles user input, and returns the selected file path. |

### terminal_gif_render.`GifRenderer` Class

- The GifRenderer class facilitates the rendering of GIF images as ASCII art in a terminal environment. 

#### Attributes

| Attribute          | Description                                                                                   |
|--------------------|-----------------------------------------------------------------------------------------------|
| `gif_path`         | Path to the GIF file to be rendered.                                                          |
| `x`, `y`           | Coordinates for positioning the GIF rendering in the terminal.                                 |
| `width`, `height`  | Dimensions for resizing the GIF frames to fit within the terminal.                             |
| `border`           | Boolean indicating whether to draw a border around the rendered GIF.                           |
| `border_color`     | RGB values for the color of the border, if enabled.                                            |
| `ascii_art`        | Instance of `TerminalAscii` for rendering images as ASCII art in the terminal.                 |
| `running`          | Boolean indicating if the GIF rendering loop is active.                                         |

#### Methods

| Method               | Description                                                                                   |
|----------------------|-----------------------------------------------------------------------------------------------|
| `__init__(self, gif_path, x=0, y=0, width=80, height=40, border=False, border_color=[255, 255, 255])` | Initializes the `GifRenderer` object with GIF path and rendering parameters.                   |
| `_convert_to_rgb(self, image)` | Converts image to RGB mode if it's in indexed mode (`'P'`).                                    |
| `_render_frame(self, image)` | Renders a single frame of the GIF, resizing and drawing it using ASCII art in the terminal.    |
| `render_gif(self)`   | Main method that renders the entire GIF, looping through frames and displaying them sequentially. |
| `__del__(self)`      | Destructor method that clears the terminal screen upon deletion of the `GifRenderer` object.  |


### terminal_graphics.`TerminalAscii` Class

- The TerminalAscii class provides methods to draw various shapes and render images as ASCII art in a terminal using Python. 

| Method                                                     | Description                                                                                                                                               |
|------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `__init__(self)`                                          | Initializes the `TerminalAscii` object, setting the font size using `terminal_utils.set_font_size`.                                                        |
| `set_cursor(self, x, y)`                                  | Sets the cursor position in the terminal to `(x, y)`.                                                                                                      |
| `print_color(self, text, color)`                          | Prints colored `text` in the terminal using specified `color` (`[r, g, b]`).                                                                                |
| `draw_line(self, x1, y1, x2, y2, color)`                   | Draws a line from `(x1, y1)` to `(x2, y2)` with specified `color`.                                                                                          |
| `draw_rectangle(self, x, y, width, height, color, filled)` | Draws a rectangle starting at `(x, y)` with given `width`, `height`, `color`, and optional `filled` flag (`True` for filled, `False` for outline).        |
| `draw_oval(self, x, y, width, height, color, filled)`      | Draws an oval centered at `(x, y)` with specified `width`, `height`, `color`, and optional `filled` flag (`True` for filled, `False` for outline).        |
| `draw_circle(self, x, y, radius, color, filled)`           | Draws a circle centered at `(x, y)` with specified `radius`, `color`, and optional `filled` flag (`True` for filled, `False` for outline).                |
| `draw_image(self, image_path, x, y, width, height, border, border_color, colored)` | Renders an image located at `image_path` as ASCII art at position `(x, y)` with specified `width`, `height`, optional `border`, `border_color`, and `colored` mode. |


### terminal_tabs.py

- interactive tabbed terminal interface where multiple tabs can run concurrently, each potentially executing its own background task, providing a robust foundation for building interactive terminal applications.

| Class           | Method Signature                                                                 | Description                                                                                                                                                 |
|-----------------|----------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `Tab`           | `__init__(self, tab_id, name, fg_color, bg_color, fg_open, bg_open, tab_function)` | Initializes a tab with specified attributes including colors and an optional function to run asynchronously.                                              |
|                 | `write(self, *args, sep='', end='\n')`                                              | Appends text to the tab's content.                                                                                                                          |
|                 | `start_tab_function(self)`                                                         | Starts the tab's asynchronous function if defined.                                                                                                          |
|                 | `stop_tab_function(self)`                                                          | Stops the tab's asynchronous function if running.                                                                                                           |
|                 | `_run_tab_function(self)`                                                          | Internal method to execute the tab's asynchronous function.                                                                                                 |
| `TabularTerminal` | `__init__(self, change_tab_key='tab', size=1)`                                      | Initializes a tabular terminal with default settings and tab size.                                                                                         |
|                   | `add_tab(self, name, fg_color, bg_color, fg_open, bg_open, tab_function=None)`      | Adds a new tab with specified attributes and an optional asynchronous function to run. Returns the tab's ID.                                               |
|                   | `remove_tab(self, tab_id)`                                                          | Removes a tab by its ID, stopping its function if it's active.                                                                                              |
|                   | `close_current(self)`                                                               | Closes the current tab.                                                                                                                                     |
|                   | `close_tabular(self)`                                                               | Closes the tabular terminal and restores terminal settings.                                                                                                 |
|                   | `_clear_screen(self)`                                                               | Clears the terminal screen.                                                                                                                                 |
|                   | `_move_cursor(self, x, y)`                                                          | Moves the cursor to the specified position in the terminal.                                                                                                 |
|                   | `_render_tabs(self)`                                                                | Renders the tabs and their content in the terminal.                                                                                                          |
|                   | `_handle_input(self)`                                                               | Handles user input to switch tabs or exit the terminal.                                                                                                      |
|                   | `_change_tab(self)`                                                                 | Changes the current active tab.                                                                                                                              |
|                   | `_get_cursor_position(self)`                                                        | Retrieves the current cursor position in the terminal.                                                                                                        |
|                   | `run(self)`                                                                         | Runs the tabular terminal, handling input and rendering tabs.                                                                                                |

### terminal_textbar.TerminalTextbar Class

The `TerminalTextbar` class provides a customizable text input interface for terminal applications, supporting features like emoji detection, text prediction, and scrollable suggestions.


| Function Name     | Description |
|-------------------|-------------|
| `__init__`        | Constructor method; initializes the TerminalTextbar object with customizable parameters for terminal positioning, colors, and input handling. |
| `initial_data`    | Initializes the data display area with initial text and styling. |
| `is_emoji`        | Checks if a given character is an emoji. |
| `char_len`        | Calculates the length of a string considering emojis and other characters. |
| `getch`           | Reads a single character from standard input without echoing it to the screen. |
| `move_cursor`     | Moves the cursor to a specified position in the terminal. |
| `clear_line`      | Clears a specified line in the terminal. |
| `clear_text_field`| Clears the entire text field area in the terminal. |
| `start_input`     | Handles the input loop for capturing user input with support for backspace, tab, arrow keys, and predictions. |
| `predict`         | Predicts and suggests completions based on user input. |
| `get_roller_value`| Retrieves values from a scrollable list based on direction. |
| `get_input`       | Initiates input handling and returns the final user input. |
| `delete`          | Handles deletion and cleanup operations. |


### terminal_textfield.TerminalTextfield Class
- The TerminalTextfield class provides a customizable text input area within a terminal environment. It supports dynamic input handling, cursor movement, and text rendering with options for background color and optional borders. 

| Function Name     | Description |
|-------------------|-------------|
| `__init__`        | Constructor method; initializes the TerminalTextfield object with specified coordinates, colors, and optional border settings. |
| `initial_data`    | Initializes the text field with initial data, handling newline characters and ensuring text fits within specified dimensions. |
| `getch`           | Reads a single character from standard input without echoing it to the screen. |
| `move_cursor`     | Moves the cursor to a specified position in the terminal. |
| `clear_line`      | Clears a specified line in the terminal. |
| `clear_text_field`| Clears the entire text field area, optionally drawing a border around it. |
| `start_input`     | Handles user input loop, supporting backspace, arrow keys, and newline characters. |
| `get_input`       | Initiates input handling and returns the final text input as a single string. |
| `delete`          | Handles deletion and cleanup operations, returning the final text input as a single string. |

### terminal_textinput.TerminalTextinput Class

- The TerminalTextinput class provides a text input field in a terminal environment, allowing users to interactively input and edit text.

| Method         | Description                                                                                         |
|----------------|-----------------------------------------------------------------------------------------------------|
| `__init__(x, y, width, bg_color, end_key='\t', border=False, border_color=(255, 255, 255), initial_data="")` | Initializes the text input field with specified coordinates, background color, optional border, and initial data. |
| `getch()`      | Reads a single character from standard input, supporting special key sequences like arrow keys.      |
| `move_cursor(x, y)` | Moves the cursor to a specified position within the terminal screen.                                 |
| `clear_line(y)` | Clears a specific line within the terminal screen.                                                   |
| `clear_text_field()` | Clears the entire text input field area, optionally drawing a border around it.                      |
| `start_input()` | Manages the input loop, allowing users to type, edit, and navigate text within the input field.      |
| `get_input()`   | Initiates input handling and returns the final text input as a single string, including multiple lines if entered. |
| `delete()`      | Handles deletion operations and cleans up the input field, returning the final text input as a single string. |


### terminal_utils.py Functions
- Basic terminal related functions

| Function Name     | Description                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------|
| `clear_terminal()` | Clears the terminal screen using the `clear` command.                                           |
| `print_color(text, color)` | Prints `text` in the specified RGB color using ANSI escape sequences.                          |
| `set_cursor(x, y)` | Sets the cursor position to `(x, y)` in the terminal window.                                    |
| `set_back_font_size()` | Sets the terminal font size back to the previous size recorded.                                 |
| `set_font_size(size)` | Sets the terminal font size to `size` and registers a function to revert it on exit.           |

### terminal_video.VideoRender Class

- Render video in both ASCII and Color Mode

| Class/Function                          | Parameters                                                                                                              | Description                                                                                       |
|-----------------------------------------|-------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `VideoRender.__init__`                   | `video_path`: str<br>`colored`: bool (default: True)<br>`x`: int (default: 0)<br>`y`: int (default: 0)<br>`width`: int (default: 80)<br>`height`: int (default: 40)<br>`border`: bool (default: False)<br>`border_color`: list (default: [255, 255, 255]) | Initializes the `VideoRender` object with video path, position, dimensions, and optional settings.|
| `VideoRender.render_video`              | None                                                                                                                    | Renders the video as ASCII art using the specified parameters.                                   |
| `VideoPlayer.__init__`                   | `video_path`: str<br>`colored`: bool (default: True)<br>`x`: int (default: 0)<br>`y`: int (default: 0)<br>`width`: int (default: 80)<br>`height`: int (default: 40)<br>`border`: bool (default: False)<br>`border_color`: list (default: [255, 255, 255])<br>`show_timeline`: bool (default: False)<br>`played_color`: list (default: [0, 255, 0])<br>`unplayed_color`: list (default: [255, 0, 0]) | Initializes the `VideoPlayer` object with video path, position, dimensions, and optional settings.|
| `VideoPlayer.render_video`              | None                                                                                                                    | Renders the video as interactive ASCII art with optional timeline display.                        |
| `VideoPlayer.toggle_pause(event)`        | `event`: keyboard event                                                                                                | Keyboard listener to pause or resume the video playback using the spacebar key.                |
| `VideoPlayer._play_audio()`              | None                                                                                                                    | Extracts and plays audio from the video file in a separate thread.                                |
| `VideoPlayer._render_frame(frame)`       | `frame`: numpy array                                                                                                    | Converts and renders a video frame as ASCII art.                                             |
| `VideoPlayer._draw_timeline(current_frame, total_frames)` | `current_frame`: int<br>`total_frames`: int                                                                             | Draws a timeline showing played and unplayed portions of the video.                         |

### terminal_videoplayer.VideoRender Class

- Render a video as in a video player build into the terminal with pause / play , the timeline, Both ASCII and color mode supported.

| Function         | Parameters                                                                                                 | Description                                                                                                         |
|------------------|------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| `__init__`       | `video_path: str`, `colored: bool=True`, `x: int=0`, `y: int=0`, `width: int=80`, `height: int=40`,          | Initializes the VideoRender object with video path and optional display parameters.                                |
|                  | `skip_frame_rate: int=25`, `border: bool=False`, `border_color: List[int]=[255, 255, 255]`,                  |                                                                                                                     |
|                  | `show_timeline: bool=False`, `played_color: List[int]=[0, 255, 0]`, `unplayed_color: List[int]=[255, 0, 0]` |                                                                                                                     |
| `_exit`          | None                                                                                                       | Clears the terminal on exit.                                                                                        |
| `_extract_audio` | None                                                                                                       | Extracts audio from the video file and returns the path to the audio file.                                          |
| `_load_audio`    | None                                                                                                       | Loads the extracted audio file for playback.                                                                         |
| `_play_audio`    | None                                                                                                       | Starts playing the audio in a separate thread and manages pause/resume functionality.                               |
| `_start_audio`   | None                                                                                                       | Starts the audio playback thread.                                                                                   |
| `_pause_audio`   | None                                                                                                       | Pauses the audio playback.                                                                                          |
| `_resume_audio`  | None                                                                                                       | Resumes the paused audio playback.                                                                                  |
| `_close_audio`   | None                                                                                                       | Stops and closes the audio playback.                                                                                |
| `_render_frame`  | `frame: numpy.ndarray`                                                                                     | Converts and renders a frame using ASCII art to the terminal.                                                        |
| `_draw_timeline` | `current_frame: int`, `total_frames: int`                                                                   | Draws a timeline indicating the progress of the video playback.                                                      |
| `__draw_timeline`| `x: int`, `y: int`                                                                                         | Draws a simplified timeline progress bar.                                                                           |
| `_draw_play_pause_button` | None                                                                               | Draws the play/pause button in the terminal interface.                                                              |
| `_toggle_pause`  | `key: pynput.keyboard.Key`                                                                                 | Toggles between play and pause based on keyboard input.                                                              |
| `render_video`   | None                                                                                                       | Renders the video frames, handles user input for pause/resume, and manages audio synchronization and timeline display.|



