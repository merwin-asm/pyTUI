import cv2
import numpy as np
import math
from terminal_graphics import TerminalAscii
import time

class Shape3D:
    def __init__(self, filename, height, width, shape_color, edge_color, show_edges, bg_color, fill_color, x_axis_rotation, y_axis_rotation, z_axis_rotation):
        self.filename = filename
        self.height = height
        self.width = width
        self.shape_color = shape_color
        self.edge_color = edge_color if show_edges else fill_color
        self.show_edges = show_edges
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.x_axis_rotation = np.deg2rad(x_axis_rotation)
        self.y_axis_rotation = np.deg2rad(y_axis_rotation)
        self.z_axis_rotation = np.deg2rad(z_axis_rotation)

    def create_image(self):
        img_width, img_height = self.width * 2, self.height * 2
        return np.full((img_height, img_width, 3), self.bg_color, dtype=np.uint8)

    def save_image(self, image):
        cv2.imwrite(self.filename, image)

    def rotate_vertices(self, vertices):
        rx, ry, rz = self.x_axis_rotation, self.y_axis_rotation, self.z_axis_rotation
        Rx = np.array([[1, 0, 0],
                       [0, math.cos(rx), -math.sin(rx)],
                       [0, math.sin(rx), math.cos(rx)]])
        Ry = np.array([[math.cos(ry), 0, math.sin(ry)],
                       [0, 1, 0],
                       [-math.sin(ry), 0, math.cos(ry)]])
        Rz = np.array([[math.cos(rz), -math.sin(rz), 0],
                       [math.sin(rz), math.cos(rz), 0],
                       [0, 0, 1]])
        R = np.dot(Rz, np.dot(Ry, Rx))
        return np.dot(vertices, R.T)

    def project_vertices(self, vertices):
        img_width, img_height = self.width * 2, self.height * 2
        projected = vertices[:, :2]
        projected += [img_width / 2, img_height / 2]
        return projected.astype(int)

    def draw_edges(self, image, vertices, edges):
        for edge in edges:
            pt1 = tuple(vertices[edge[0]])
            pt2 = tuple(vertices[edge[1]])
            cv2.line(image, pt1, pt2, self.edge_color, 2)

    def draw_vertices(self, image, vertices):
        for vertex in vertices:
            cv2.circle(image, tuple(vertex), 5, self.shape_color, -1)

    def fill_shape(self, image, vertices, faces):
        for face in faces:
            pts = np.array([vertices[i] for i in face], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.fillPoly(image, [pts], self.fill_color)

class Cuboid(Shape3D):
    def draw(self, length, width, height):
        hs_l, hs_w, hs_h = length / 2.0, width / 2.0, height / 2.0
        vertices = np.array([[-hs_l, -hs_w, -hs_h],
                             [hs_l, -hs_w, -hs_h],
                             [hs_l, hs_w, -hs_h],
                             [-hs_l, hs_w, -hs_h],
                             [-hs_l, -hs_w, hs_h],
                             [hs_l, -hs_w, hs_h],
                             [hs_l, hs_w, hs_h],
                             [-hs_l, hs_w, hs_h]])

        rotated_vertices = self.rotate_vertices(vertices)
        projected_vertices = self.project_vertices(rotated_vertices)

        edges = [(0, 1), (1, 2), (2, 3), (3, 0),
                 (4, 5), (5, 6), (6, 7), (7, 4),
                 (0, 4), (1, 5), (2, 6), (3, 7)]

        faces = [(0, 1, 2, 3), (4, 5, 6, 7),
                 (0, 1, 5, 4), (2, 3, 7, 6),
                 (0, 3, 7, 4), (1, 2, 6, 5)]

        image = self.create_image()
        self.fill_shape(image, projected_vertices, faces)
        if self.show_edges:
            self.draw_edges(image, projected_vertices, edges)
        self.draw_vertices(image, projected_vertices)

        self.save_image(image)

class Sphere(Shape3D):
    def draw(self, radius, detail=20):
        def sphere_points(radius, detail):
            points = []
            for i in range(detail + 1):
                lat = (math.pi / detail) * i - (math.pi / 2)
                for j in range(detail + 1):
                    lon = (2 * math.pi / detail) * j
                    x = radius * math.cos(lat) * math.cos(lon)
                    y = radius * math.cos(lat) * math.sin(lon)
                    z = radius * math.sin(lat)
                    points.append((x, y, z))
            return np.array(points)

        vertices = sphere_points(radius, detail)
        rotated_vertices = self.rotate_vertices(vertices)
        projected_vertices = self.project_vertices(rotated_vertices)

        image = self.create_image()
        self.draw_vertices(image, projected_vertices)

        self.save_image(image)

class Pyramid(Shape3D):
    def draw(self, base_length, height):
        half_base = base_length / 2.0
        vertices = np.array([[0, 0, height],
                             [-half_base, -half_base, 0],
                             [half_base, -half_base, 0],
                             [half_base, half_base, 0],
                             [-half_base, half_base, 0]])

        rotated_vertices = self.rotate_vertices(vertices)
        projected_vertices = self.project_vertices(rotated_vertices)

        edges = [(0, 1), (0, 2), (0, 3), (0, 4),
                 (1, 2), (2, 3), (3, 4), (4, 1)]

        faces = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1), (1, 2, 3, 4)]

        image = self.create_image()
        self.fill_shape(image, projected_vertices, faces)
        if self.show_edges:
            self.draw_edges(image, projected_vertices, edges)
        self.draw_vertices(image, projected_vertices)

        self.save_image(image)

class Cylinder(Shape3D):
    def draw(self, radius, height, detail=20):
        def cylinder_points(radius, height, detail):
            points = []
            for i in range(detail):
                angle = (2 * math.pi / detail) * i
                x = radius * math.cos(angle)
                y = radius * math.sin(angle)
                points.append((x, y, -height / 2))
                points.append((x, y, height / 2))
            return np.array(points)

        vertices = cylinder_points(radius, height, detail)
        rotated_vertices = self.rotate_vertices(vertices)
        projected_vertices = self.project_vertices(rotated_vertices)

        edges = [(i, i + 1) for i in range(0, len(vertices) - 2, 2)]
        edges += [(i, i + 2) for i in range(0, len(vertices) - 2, 2)]

        image = self.create_image()
        if self.show_edges:
            self.draw_edges(image, projected_vertices, edges)
        self.draw_vertices(image, projected_vertices)

        self.save_image(image)
if __name__ == "__main__":
    # Example usage
    cuboid = Cuboid("cuboid.png", 300, 300, (0, 255, 0), (255, 0, 0), True, (0, 0, 0), (0, 0, 255), 30, 30, 30)
    cuboid.draw(100, 50, 150)

    # sphere = Sphere("sphere.png", 300, 300, (0, 255, 0), (255, 0, 0), False, (0, 0, 0), (0, 0, 255), 30, 30, 30)
    # sphere.draw(100)

    # pyramid = Pyramid("pyramid.png", 300, 300, (0, 255, 0), (255, 0, 0), True, (0, 0, 0), (0, 0, 255), 30, 30, 30)
    # pyramid.draw(100, 150)

    # cylinder = Cylinder("cylinder.png", 300, 300, (0, 255, 0), (255, 0, 0), True, (0, 0, 0), (0, 0, 255), 30, 30, 30)
    # cylinder.draw(50, 150)

    # # Display the image on the terminal
    # ascii_art = TerminalAscii()
    # ascii_art.draw_image("sphere.png", 10, 10, 100, 100, border=True, border_color=[255, 0, 255], colored=True)
    time.sleep(3)
