import tkinter as tk
import math
import numpy as np

class TopologicalVisualizer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Топологическая визуализация")
        self.window.geometry("640x600")
        self.window.resizable(False, False)

        self.DETAIL = 30
        self.CANVAS_WIDTH = 640
        self.CANVAS_HEIGHT = 481
        self.COLOR_FACTOR = 10

        self.setup_interface()
        self.setup_transforms()
        self.generate_geometry()

    def setup_interface(self):
        self.display = tk.Canvas(bg="white", width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)
        
        self.param1 = tk.Scale(orient=tk.HORIZONTAL, length=200, 
                              from_=1.0, to=3.0, resolution=0.2,
                              command=self.update_visualization)
        self.param2 = tk.Scale(orient=tk.HORIZONTAL, length=200,
                              from_=0.5, to=2.0, resolution=0.1,
                              command=self.update_visualization)
        
        self.param1.pack(anchor=tk.CENTER, expand=1)
        self.param2.pack(anchor=tk.CENTER, expand=1)
        self.display.pack(anchor=tk.CENTER, expand=1)

    def setup_transforms(self):
        # Initialize transformation matrix with scaling
        self.transform_matrix = self.scale_matrix(50, 50, 50)
        

    def create_shape(self, theta, radius, param1, param2):
        return np.array([
            (param1 + radius * math.cos(theta / 2)) * math.cos(theta),
            (param1 + radius * math.cos(theta / 2)) * math.sin(theta),
            param2 * radius * math.sin(theta / 2)
        ])

    def generate_geometry(self):
        self.geometry = []
        max_theta = 2 * math.pi
        min_radius = -0.5
        max_radius = 0.5
        
        for i in range(self.DETAIL):
            for j in range(self.DETAIL):
                # Первый треугольник
                self.geometry.append((
                    self.create_shape(
                        (i) * max_theta / self.DETAIL,
                        (j - self.DETAIL/2) * (max_radius - min_radius) / self.DETAIL,
                        float(self.param1.get()),
                        float(self.param2.get())
                    ),
                    self.create_shape(
                        (i) * max_theta / self.DETAIL,
                        (j + 1 - self.DETAIL/2) * (max_radius - min_radius) / self.DETAIL,
                        float(self.param1.get()),
                        float(self.param2.get())
                    ),
                    self.create_shape(
                        (i+1) * max_theta / self.DETAIL,
                        (j + 1 - self.DETAIL/2) * (max_radius - min_radius) / self.DETAIL,
                        float(self.param1.get()),
                        float(self.param2.get())
                    )
                ))
                
                # Второй треугольник
                self.geometry.append((
                    self.create_shape(
                        (i) * max_theta / self.DETAIL,
                        (j - self.DETAIL/2) * (max_radius - min_radius) / self.DETAIL,
                        float(self.param1.get()),
                        float(self.param2.get())
                    ),
                    self.create_shape(
                        (i+1) * max_theta / self.DETAIL,
                        (j - self.DETAIL/2) * (max_radius - min_radius) / self.DETAIL,
                        float(self.param1.get()),
                        float(self.param2.get())
                    ),
                    self.create_shape(
                        (i+1) * max_theta / self.DETAIL,
                        (j + 1 - self.DETAIL/2) * (max_radius - min_radius) / self.DETAIL,
                        float(self.param1.get()),
                        float(self.param2.get())
                    )
                ))

    # Custom 3D transformation functions
    def scale_matrix(self, sx, sy, sz):
        """Create a scaling matrix"""
        return np.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])

    def rotate_x_matrix(self, angle):
        """Create a rotation matrix around X axis"""
        c = math.cos(angle)
        s = math.sin(angle)
        return np.array([
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ])

    def rotate_y_matrix(self, angle):
        """Create a rotation matrix around Y axis"""
        c = math.cos(angle)
        s = math.sin(angle)
        return np.array([
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ])

    def rotate_z_matrix(self, angle):
        """Create a rotation matrix around Z axis"""
        c = math.cos(angle)
        s = math.sin(angle)
        return np.array([
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def multiply_matrices(self, a, b):
        """Multiply two 4x4 matrices"""
        return np.dot(a, b)

    def transform_point(self, point, matrix):
        """Transform a 3D point using a 4x4 transformation matrix"""
        # Convert point to homogeneous coordinates
        homogeneous = np.append(point, 1)
        # Apply transformation
        transformed = np.dot(matrix, homogeneous)
        # Convert back to 3D coordinates
        return transformed[:3]

    def render_coordinate_system(self):
        for i in range(21):
            line_x = [[-10, -10 + i, 0], [10, -10 + i, 0]]
            line_y = [[10 - i, -10, 0], [10 - i, 10, 0]]
            line_z = [[0, 0, -10], [0, 0, 10]]
            
            # Transform and draw X axis lines
            p1 = self.transform_point(line_x[0], self.transform_matrix)
            p2 = self.transform_point(line_x[1], self.transform_matrix)
            self.display.create_line(
                int(p1[0] + self.CANVAS_WIDTH / 2),
                int(p1[1] + self.CANVAS_HEIGHT / 2),
                int(p2[0] + self.CANVAS_WIDTH / 2),
                int(p2[1] + self.CANVAS_HEIGHT / 2)
            )
            
            # Transform and draw Y axis lines
            p1 = self.transform_point(line_y[0], self.transform_matrix)
            p2 = self.transform_point(line_y[1], self.transform_matrix)
            self.display.create_line(
                int(p1[0] + self.CANVAS_WIDTH / 2),
                int(p1[1] + self.CANVAS_HEIGHT / 2),
                int(p2[0] + self.CANVAS_WIDTH / 2),
                int(p2[1] + self.CANVAS_HEIGHT / 2)
            )
            
            # Transform and draw Z axis lines
            p1 = self.transform_point(line_z[0], self.transform_matrix)
            p2 = self.transform_point(line_z[1], self.transform_matrix)
            self.display.create_line(
                int(p1[0] + self.CANVAS_WIDTH / 2),
                int(p1[1] + self.CANVAS_HEIGHT / 2),
                int(p2[0] + self.CANVAS_WIDTH / 2),
                int(p2[1] + self.CANVAS_HEIGHT / 2)
            )

        # Draw Z axis marks
        for i in range(-10, 11):
            z_marks = [[-0.125, 0, i], [0.125, 0, i]]
            p1 = self.transform_point(z_marks[0], self.transform_matrix)
            p2 = self.transform_point(z_marks[1], self.transform_matrix)
            self.display.create_line(
                int(p1[0] + self.CANVAS_WIDTH / 2),
                int(p1[1] + self.CANVAS_HEIGHT / 2),
                int(p2[0] + self.CANVAS_WIDTH / 2),
                int(p2[1] + self.CANVAS_HEIGHT / 2)
            )

    def render(self):
        self.display.delete("all")
        self.render_coordinate_system()
        
        # Sort polygons by their average Z depth for proper rendering order
        self.geometry.sort(key=lambda poly: np.mean([self.transform_point(p, self.transform_matrix)[2] for p in poly]))
        
        for polygon in self.geometry:
            # Transform all points of the polygon
            points = []
            for point in polygon:
                transformed = self.transform_point(point, self.transform_matrix)
                points.append((
                    int(transformed[0] + self.CANVAS_WIDTH / 2),
                    int(transformed[1] + self.CANVAS_HEIGHT / 2)
                ))
            
            # Calculate color based on depth
            avg_z = np.mean([self.transform_point(p, self.transform_matrix)[2] for p in polygon])
            color_value = min(255, abs(int(self.COLOR_FACTOR * avg_z)))
            hex_color = "#0000" + format(color_value, "02X")
            
            # Draw the polygon
            self.display.create_polygon(
                points[0][0], points[0][1],
                points[1][0], points[1][1],
                points[2][0], points[2][1],
                fill=hex_color, outline="#000000"
            )
        
    def update_visualization(self, _=None):
        self.generate_geometry()
        self.render()

    def handle_input(self, event):
        if event.char == "w":
            self.transform_matrix = self.multiply_matrices(self.scale_matrix(1.1, 1.1, 1.1), self.transform_matrix)
        elif event.char == "s":
            self.transform_matrix = self.multiply_matrices(self.scale_matrix(1/1.1, 1/1.1, 1/1.1), self.transform_matrix)
        elif event.keycode == 111:  # Up arrow
            self.transform_matrix = self.multiply_matrices(self.rotate_x_matrix(math.pi / 16), self.transform_matrix)
        elif event.keycode == 116:  # Down arrow
            self.transform_matrix = self.multiply_matrices(self.rotate_x_matrix(-math.pi / 16), self.transform_matrix)
        elif event.keycode == 113:  # Left arrow
            self.transform_matrix = self.multiply_matrices(self.rotate_y_matrix(math.pi / 16), self.transform_matrix)
        elif event.keycode == 114:  # Right arrow
            self.transform_matrix = self.multiply_matrices(self.rotate_y_matrix(-math.pi / 16), self.transform_matrix)
        
        self.render()

    def run(self):
        self.window.bind("<KeyPress>", self.handle_input)
        self.window.mainloop()

if __name__ == "__main__":
    app = TopologicalVisualizer()
    app.run()