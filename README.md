# pyTUI
TUI - Terminal User Interface | Python modules to code UI's for terminal!

<img src="https://komarev.com/ghpvc/?username=merwin-asm-pytui&label=Project%20views&color=0e75b6&style=flat" /> </p>

# Install :
```sh
pip install -r requirements.py
git clone https://github.com/merwin-asm/pyTUI.git
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


# Note :
  - Could change your terminal size and font etc, If it didnt change back automatically after the code exit , then make sure you know how to revert it back.
    
