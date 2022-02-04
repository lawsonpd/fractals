import tkinter as tk
import math

root = tk.Tk()

width = 900
height = 900

canvas = tk.Canvas(root, width=width, height=height, bg="black")
canvas.pack()

# canvas.create_line(width/2, height/2, width/2+1, height/2+1, fill="white")
img = tk.PhotoImage(width=width, height=height)
canvas.create_image((width/2, height/2), image=img, state="normal")
# img.put("white", (int(width/2), int(height/2)))

# Set center, radius, & num of vertices manually
center, radius, num_vertices = (width/2, height/2), 100, 5
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
root.mainloop()
