import tkinter as tk
from tkinter import Tk
import math
import random

def euc_dist(point1:tuple, point2:tuple) -> tuple:
    return math.sqrt((point2[1] - point1[1])**2 + (point2[0] - point1[0])**2)

def midpoint(point1:tuple, point2:tuple) -> tuple:
    return ((point1[0] + point2[0])/2, (point1[1] + point2[1])/2)

def inter_point(point1:tuple, point2:tuple, jump_factor:float) -> tuple:
    return ((point1[0] + point2[0]) * jump_factor, (point1[1] + point2[1]) * jump_factor)

def polygon_height(polygon:tuple) -> float:
    '''
    Return "height" (distance from top vertex to baseline).
    NOTE: Assumes polygon has one side that's parallel to the x-axis.
    '''
    return max(polygon, key=lambda p: p[1])[1] - min(polygon, key=lambda p: p[1])[1]

def special_dist(polygon:tuple, point:tuple) -> bool:
    '''
    Determines whether a point is less than D distance from
    all vertices in polygon, where D is shortest distance
    across the polygon.
    '''
    d = polygon_height(polygon)
    for vertex in polygon:
        if euc_dist(point, vertex) > d:
            return False
    return True

def is_contained(polygon:tuple, point:tuple) -> bool:
    '''
    This is believed to be true for equilateral triangles but isn't known
    to work for other kinds of triangles.
    '''
    dists = [euc_dist(vertex, point) for vertex in polygon]
    d = 2 * euc_dist(polygon[0], polygon[1])
    return sum(dists) <= d

def polygon_from_center(center:tuple, radius:tuple) -> tuple:
    '''
    NOTE: currently defines a 3-polygon (triangle). Will generalize in time.

    Assume triangle is equilateral.

    Given a center and a radius, and assuming the baseline of the triangle is
    parallel to the x-axis, we can easily compute the "top" point of the
    triangle. This is simply (cx, cy+r), where cx and cy are the coordinates
    of the center point. (Effectively we're just drawing a straight line of
    length r up from the center point.)

    To compute the other two points of the triangle, we can use trigonometry
    to compute the center point of the baseline of the triangle, then compute
    the length of the baseline, and finally determine points out to the left
    and right from that center baseline point by respectively adding and
    subtracting half the length of the baseline tothe x-coord of the center
    baseline point.

    Returns triangle coordinates := (a, b, c), where a is top center point
    and b & c are other points moving clockwise.
    '''

    # Alias math.radians for using trig functions, which assume values are
    # in radians
    rad = math.radians

    # Calculated based on fact that the right triangle formed by the center
    # of triangle, the center of the baseline, and either of the other
    # two points is a 30-60-90 triangle.
    center_to_baseline = radius * math.sin(rad(30))
    baseline_center_point = center[0], center[1] - center_to_baseline

    len_half_baseline = center_to_baseline / math.tan(rad(30))

    a = center[0], center[1] + radius
    b = baseline_center_point[0] + len_half_baseline, baseline_center_point[1]
    c = baseline_center_point[0] - len_half_baseline, baseline_center_point[1]

    return a, b, c

class FractalGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

    def create_canvas(self, width, height):
        canvas = tk.Canvas(self.master, bg="black", width=width, height=height)
        img = tk.PhotoImage(width=self.canvas_width, height=self.canvas_height)
        canvas.create_image((self.canvas_width/2, self.canvas_height/2), image=self.img, state="normal")
        return canvas

    def fill_point(self, coords):
        pass

class ChaosGameFractal:
    def __init__(self, center:tuple, radius:float, window_width:int, window_height:int): # Will add more params in time
        self.center, self.radius, self.canvas_width, self.canvas_height = center, radius, window_width, window_height
        self.vertices = polygon_from_center(center, radius)
        self.fractal_pts = {}

        ## Setting initial random point
        # Construct a square around the polygon
        min_x, max_x, min_y, max_y = \
            min(self.vertices, key=lambda point: point[0])[0], \
            max(self.vertices, key=lambda point: point[0])[0], \
            min(self.vertices, key=lambda point: point[1])[1], \
            max(self.vertices, key=lambda point: point[1])[1]
        self.init_rand_point = random.randint(math.ceil(min_x), math.floor(max_x)), random.randint(math.ceil(min_y), math.floor(max_y))
        while not is_contained(self.vertices, self.init_rand_point):
            self.init_rand_point = random.randint(math.ceil(min_x), math.floor(max_x)), random.randint(math.ceil(min_y), math.floor(max_y))
        self.fractal_pts[0] = self.init_rand_point

        # Construct GUI
        # self.root = tk.Tk()
        # self.root.title("Fractal generator")
        # self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="black")
        # self.canvas.pack()
        # self.img = tk.PhotoImage(width=self.canvas_width, height=self.canvas_height)
        # self.canvas.create_image((self.canvas_width/2, self.canvas_height/2), image=self.img, state="normal")
        # self.root.mainloop()

    def next_point(self, i:int, jump_factor:float, skip_n:int=0) -> tuple:
        rand_vertex = random.choice(self.vertices)
        new_point = inter_point(rand_vertex, self.fractal_pts[i-1], 0.5)
        return new_point

    def plot_fractal(self):
        '''
        Should width and height be passed as parameter?
        '''

        i = 1
        while True:
            print("running fractal generator")
            next = self.next_point(i, 0.5)
            self.fractal_pts[i] = next
            print(f'new point is ({next[0]}, {next[1]})')
            self.img.put('white', (int(next[0]), int(next[1])))
            i += 1

if __name__ == '__main__':
    game = ChaosGameFractal((450, 450), 200, 900, 900)
    # game.plot_fractal()
