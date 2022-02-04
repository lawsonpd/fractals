import tkinter as tk
import math

master = tk.Tk()

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
    def create_canvas(self, canvas_width, canvas_height):
        canvas = tk.Canvas(self.master, bg="black", width=canvas_width, height=canvas_height)
        return canvas

app = Application(master=master)
canvas = app.create_canvas(900, 900)

canvas.pack()

##### Added by me
img = tk.PhotoImage(width=900, height=900)
canvas.create_image((450, 450), image=img, state="normal")

# Set center, radius, & num of vertices manually
center, radius, num_vertices = (450, 450), 100, 5
alpha = 360 / num_vertices

points = {}
for i in range(num_vertices):
    points[i] = center[0] + (radius * math.cos(math.radians(alpha * i))), \
                center[1] + (radius * math.sin(math.radians(alpha * i)))
    print(f'point: {points[i]}; theta: {i * alpha}')

colors = ["white", "yellow", "green", "blue", "red"]
img.put("white", tuple(map(int, center)))
for i, p in points.items():
    img.put("white", tuple(map(int, p)))
#####

if __name__ == '__main__':
    app.mainloop()
