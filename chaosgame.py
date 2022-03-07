import tkinter as tk
import random

from chaosgame_utils import inter_point, is_contained, polygon_from_center, get_random_point

class FractalGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.root = master

    def create_canvas(self, width, height):
        canvas = tk.Canvas(self.root, bg="black", width=width, height=height)
        return canvas

    def create_image(self, width, height):
        canvas = self.create_canvas(width=width, height=height)
        canvas.pack()
        img = tk.PhotoImage(width=width, height=height)
        canvas.create_image((width//2, height//2), image=img, state="normal")
        return img

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
    root = tk.Tk()
    gui = FractalGUI(master=root)
    canvas_image = gui.create_image(900,900)
    btn_test = tk.Button(root, bg="white", text="Test")

    game = ChaosGameFractal(center=(450, 450), radius=400, num_vertices=6)
    
    i = 1
    while True:
        point = game.generate_point(i=i, jump_factor=0.5, skip_n=0)
        print(f'Iteration {i}; point is {point}')
        canvas_image.put('white', point)
        gui.update()
        i += 1
    # canvas_image.put('white', )
