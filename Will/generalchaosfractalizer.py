import random
import math
from tkinter import Tk, Canvas, PhotoImage
#width = 2140
#height = 1400
width = 1440
height = 900
window = Tk()
canvas = Canvas(window, width=width, height=height, bg="#000000")
canvas.pack()
img = PhotoImage(width=width, height=height)
canvas.create_image((width // 2, height // 2), image=img, state="normal")
window.title('Generalized Chaos Game Fractal Generator')
# try these:
# sides=3, jump=0, skip=n, vertices=a,  x=0, y=0, radius=750
# sides=4, jump=.5, skip=y, vertices=a, x:0, y=0, radius=900
# sides=4, jump=.618, skip=n, vertices=a, x=0, y=0, radius=700
# sides=5, jump=0, skip=y, vertices=a,  x=0, y=0, radius=750
# sides=5, jump=.618, skip=n, vertices=a, x=0, y=0, radius=700
# sides=5, jump=.5, skip=y, vertices=a, x=0, y=0, radius=800
# sides=5, jump=1.382, skip=n, vertices=a, x=0, y=0, radius=300
# sides=7, jump=.692, skip=n, vertices=a, x=0, y=0, radius=700
sides = int(input("\nhow many sides? "))
jumpFraction = float(input("jump fraction (enter 0 to autocalculate): "))
if jumpFraction == 0:
    jumpFraction = (sides / (sides + 3))
skipPrevious = input("skip previous vertex, [y]es or [n]o? ")
x = {}
y = {}
manAuto = input("[m]anually enter vertices, or [a]utocalculate? ")
if manAuto == "m":
    for i in range(0, sides):
        x[i] = int(input(f"x coordinate of vertex {(i+1)}: "))
        y[i] = int(input(f"y coordinate of vertex {(i+1)}: "))
else:
    xCenter = int(input("x coordinate of center? (enter 0 for center) "))
    if xCenter == 0:
        xCenter = int((width / 2))
    yCenter = int(input("y coordinate of center? (enter 0 for center) "))
    if yCenter == 0:
        yCenter = int((height / 2))
    radius = int(input("radius? (max is ~800) "))
    for i in range(0, sides):
        x[i] = int(radius * math.cos(2 * math.pi * (i / sides))) + xCenter
        y[i] = int(radius * math.sin(2 * math.pi * (i / sides))) + yCenter
currentX = x[1]
currentY = y[1]
futureX = x[2]
futureY = y[2]
newVertex = 1
oldVertex = 1
while 2 == 2:
    if skipPrevious == "y":
        while newVertex == oldVertex:
            newVertex = random.randint(0, (sides - 1))
        oldVertex = newVertex
    else:
        newVertex = random.randint(0, (sides - 1))
    futureX = x[newVertex]
    futureY = y[newVertex]
    currentX += (futureX - currentX) * jumpFraction
    currentY += (futureY - currentY) * jumpFraction
    img.put("white", (int(currentX), int(currentY)))
    window.update()

