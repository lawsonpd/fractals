import tkinter as tk
import random

from chaosgame_utils import inter_point, is_contained, polygon_from_center, get_random_point

class FractalGUI(tk.Tk):
    def __init__(self, width, height):
        super().__init__()

        self.title("Fractal chaos game")

        self.main_frame = tk.Frame(self, width=width, height=height, bg="black")
        self.main_frame.pack(expand=True)

        self.ui_frame = tk.Frame(self.main_frame, height=height, width=200, bg="black")
        self.ui_frame.pack(fill=tk.BOTH, side=tk.LEFT)

        self.canvas = tk.Canvas(self.main_frame, bg="black", width=width, height=height)
        self.canvas.pack(fill=tk.BOTH, side=tk.RIGHT)

        self.img = tk.PhotoImage(width=width, height=height)
        self.canvas_img = self.canvas.create_image((width//2, height//2), image=self.img, state="normal")

class ChaosGameFractal:
    def __init__(self, center:tuple, radius:float, num_vertices:int): # Will add more params in time
        self.center, self.radius = center, radius
        self.vertices = polygon_from_center(center, radius, num_vertices)
        print(self.vertices)
        self.fractal_pts = {}

        ## Setting initial random point
        # Construct a square around the polygon
        min_x, max_x, min_y, max_y = \
            min(self.vertices, key=lambda point: point[0])[0], \
            max(self.vertices, key=lambda point: point[0])[0], \
            min(self.vertices, key=lambda point: point[1])[1], \
            max(self.vertices, key=lambda point: point[1])[1]
        self.init_rand_point = get_random_point(min_x, max_x, min_y, max_y)
        while not is_contained(self.vertices, self.init_rand_point):
            self.init_rand_point = get_random_point(min_x, max_x, min_y, max_y)
        self.fractal_pts[0] = self.init_rand_point

    def generate_point(self, i:int, jump_factor:float, skip_n:int=0) -> tuple:
        rand_vertex = random.choice(self.vertices)
        new_point = inter_point(rand_vertex, self.fractal_pts[i-1], jump_factor=jump_factor)
        print(f'Next point generated: {new_point}')
        self.fractal_pts[i] = new_point
        return new_point

if __name__ == '__main__':
    # root = tk.Tk()
    gui = FractalGUI(900, 900)
    game = ChaosGameFractal(center=(450, 450), radius=400, num_vertices=6)

    i = 1
    while True:
        point = game.generate_point(i=i, jump_factor=0.5, skip_n=0)
        print(f'Iteration {i}; point is {point}')
        gui.img.put('white', point)
        gui.update()
        i += 1
