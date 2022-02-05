from tkinter import *
from tkinter import messagebox, colorchooser
import math
import random

# Lovely palettes:
# sea moss: "#FAF3DD" "#C8D5B9" "#8FC0A9" "#68B0AB" "#4A7C59"
# blossom valent: "#FD001D" "#FE8500" "#2E82B0" "#FFE2E7" "#FFBABF"
# guiding light: "#E4F5FB" "#E2DDBF" "#F4E34B" "#5BC5E8" "#E50000"
# sunset sunglasses: "#ffe0bd" "#ffcd94" "#ffad60" "#eac086" "#ffe39f" "#ff8614"
# roygbiv: "#f2120d" "#ef7626" "#faed03" "#0af508" "#051ac3" "#7d7601"

err = ""
errMessage = ""
beenPaused = 0
beenStarted = 0
isPaused = 0
f = {}
e = {}
d = {}
numColors = 0

root = Tk()
root.wm_title("sparks before the universe becomes cold and dark and expands forever")
root.config(background="#000000")
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
#root.geometry("%dx%d" % (width, height))
root.geometry(f'{width}x{height}+0+0')
root.attributes('-fullscreen', True)
root.resizable(width=False, height=False)


def startClicked():
    global beenStarted
    beenStarted = 1
    global isPaused
    if isPaused == 1:
        isPaused = 0
        render_fractal()
    err, errMessage = verify_parameters()
    if err == "y":
        messagebox.showerror("Missing Parameters", errMessage)
    else:
        global numVertices
        numVertices = int(getSides.get())
        global jumpFraction
        jumpFraction = float(setJump.get())
        global skip
        skip = Var2.get()
        global xCenter
        xCenter = int((width / 2))
        global yCenter
        yCenter = int((height / 2))
        global radius
        radius = int(getRadius.get())
        init_fractal(numVertices, jumpFraction, skip, xCenter, yCenter, radius)

def verify_parameters():
    global err
    err = "n"
    errMessage = ""
    numVertices = getSides.get()
    if numVertices == "":
        err = "y"
        errMessage += "# of vertices is required\n"
    jumpFraction = setJump.get()
    if jumpFraction == "":
        err = "y"
        errMessage += "Jump fraction is required\n"
    radius = getRadius.get()
    if radius == "":
        err = "y"
        errMessage += "Radius is required\n"
    return err, errMessage


def init_fractal(numVertices, jumpFraction, skip, xCenter, yCenter, radius):
    global x
    x = {}
    global y
    y = {}
    for i in range(0, numVertices):
        # x[i] = int(radius * math.cos(2 * math.pi * (i / numVertices)+11)) + int(width / 2) + 100 <--rotated
        # y[i] = int(radius * math.sin(2 * math.pi * (i / numVertices)+11)) + int(height / 2) - 20 <--rotated
        x[i] = int(radius * math.cos(2 * math.pi * (i / numVertices))) + int(width / 2) + 100
        y[i] = int(radius * math.sin(2 * math.pi * (i / numVertices))) + int(height / 2) - 20

    global currentX
    currentX = x[1]
    global currentY
    currentY = y[1]
    global futureX
    futureX = x[2]
    global futureY
    futureY = y[2]

    render_fractal()


def render_fractal():
    global currentX
    global currentY
    global futureX
    global futureY
    global vertex
    global slideValue
    global numColors

    vertex = {}
    if numColors != 0:
        slideValue = slider.get()
        vertex[0] = 1
        vertex[1] = 1
        for n in range(slideValue):
            vertex[n] = 1

        color = {}
        for n in range(numColors):
            color[n] = e[n].get()
    else:
        vertex[0] = 0
        vertex[1] = 0

    currentX = x[1]
    currentY = y[1]
    repeated = 0

    while isPaused != 1:
        if numColors != 0:
            if slideValue == 0:
                vertex[1] = vertex[0]
            else:
                for i in range(slideValue, 0, -1):
                    vertex[i] = vertex[i - 1]
        else:
            vertex[1] = vertex[0]

        # this block: unrestricted
        if skip == 1:
            vertex[0] = random.randint(0, (numVertices - 1))

        # this block: no doubles
        # (2x isn't permitted)
        if skip == 2:
            while vertex[0] == vertex[1]:
                vertex[0] = random.randint(0, (numVertices - 1))

        # this block: no triples
        # (3x isn't permitted)
        if skip == 3:
            if vertex[0] != vertex[1]:
                repeated = 0
            else:
                if repeated == 1:
                    while vertex[0] == vertex[1]:
                        vertex[0] = random.randint(0, (numVertices - 1))
                    repeated = 0
                else:
                    vertex[0] = random.randint(0, (numVertices - 1))
                    repeated = 1

        futureX = x[vertex[0]]
        futureY = y[vertex[0]]

        currentX += int((futureX - currentX) * jumpFraction)
        currentY += int((futureY - currentY) * jumpFraction)

        if 0 < currentX < width and 0 < currentY < height:
            if numColors == 0:
                img.put("white", (int(currentX), int(currentY)))
            else:
                col = color[vertex[(slideValue)]]
                img.put(col, (int(currentX), int(currentY)))
            newCanvas.update()

def pauseClicked():
    if beenStarted == 1:
        global isPaused
        temp = isPaused
        if temp == 1:
            isPaused = 0
        if temp == 0:
            isPaused = 1

def clearClicked():
    global beenStarted
    beenStarted == 0
    global isPaused
    isPaused = 0
    global img
    newCanvas.delete(img)
    img = PhotoImage(width=width, height=height)
    newCanvas.create_image((width // 2, height // 2), image=img, state="normal")

def set_slide_val(self):
    global slideValue
    slideValue = slider.get()
    clearClicked()

def set_side_slide(self):
    global numVertices
    numVertices = sideSlider.get()
    getSides.delete(0, END)
    getSides.insert(0, numVertices)
    clearClicked()
    if beenStarted == 1:
        startClicked()

def set_jump_slide(self):
    global jumpFraction
    jumpFraction = jumpSlider.get()
    jumpSlider.set(jumpFraction)
    setJump.delete(0, END)
    setJump.insert(0, jumpFraction)
    clearClicked()
    if beenStarted == 1:
        startClicked()

def skip_clicked():
    global skip
    global Var2
    skip = Var2.get()
    clearClicked()

def pickerClicked(blip):
    global e
    e[blip].delete(0,END)
    e[blip].config(bg="white")
    color_code = colorchooser.askcolor(title="Choose color")
    if color_code:
        e[blip].insert(0, color_code[1])
        e[blip].config(bg=color_code[1])

def colorClicked():
    pauseClicked()
    numVertices = getSides.get()
    global numColors
    if numVertices == "":
        messagebox.showerror("Error", "Please enter number of vertices first")
    else:
        global d
        global e
        global f
        global scalelabel
        global slider
        if numColors == 0:
            blankLabel = Label(parametersFrame, text="     ", background="#000000", fg="gray")
            blankLabel.grid(row=18, column=0, padx=10, pady=2)
            for n in range(int(numVertices)):
                numColors += 1
                d[n] = Label(parametersFrame, text=f"color {n + 1}", background="#000000", fg="gray")
                d[n].grid(row=(19 + int(n)), column=0, padx=10, pady=2, sticky=W)
                e[n] = Entry(parametersFrame, width=8, background="white")
                e[n].grid(row=(19 + int(n)), column=1, padx=10, pady=2)
                f[n] = Button(parametersFrame, text="pick", command=lambda n=n: pickerClicked(n), bg="#000000", fg="gray")
                f[n].grid(row=(19 + int(n)), column=0, padx=10, pady=2, sticky=E)
            blankLabel = Label(parametersFrame, text="     ", background="#000000", fg="gray")
            blankLabel.grid(row=(20 + int(numColors)), column=0, padx=10, pady=2)
            scalelabel = Label(parametersFrame, text=f"scale factor", background="#000000", fg="gray")
            scalelabel.grid(row=(21 + int(numColors)), column=0, padx=10, pady=2)

            slider = Scale(parametersFrame, from_=0, to=5, orient=HORIZONTAL, command=set_slide_val, fg="white", bg="#000000", bd=0, troughcolor="white")
            slider.grid(row=(21 + int(numColors)), column=1, padx=10, pady=2)
        else:
            for n in range(int(numVertices)):
                numColors = 0
                d[n].grid_forget()
                e[n].grid_forget()
                f[n].grid_forget()
            scalelabel.grid_forget()
            slider.grid_forget()

def saveClicked():
    print("render saved")

def minimize():
    root.state(newstate="iconic")

def do_quit():
    quit()


renderingFrame = Frame(root, width=width, height=height, bd=0, bg="#000000", highlightcolor="#000000", highlightbackground="#000000", highlightthickness=0)
renderingFrame.grid(row=0, column=0, padx=0, pady=0)
newCanvas = Canvas(renderingFrame, width=width, height=height, bg="#000000", bd=0)
newCanvas.grid(row=0, column=0, padx=0, pady=0, sticky="NW")
img = PhotoImage(width=width, height=height)
newCanvas.create_image((0, 0), image=img, state="normal", anchor="nw")

parametersFrame = Frame(renderingFrame, width=0, height=0, bg="#000000")
parametersFrame.grid(row=0, column=0, padx=25, pady=25, sticky="NW")

#bg = PhotoImage(file="fractus.png")
#limg = Label(parametersFrame, background="#000000", image=bg, anchor=CENTER)
#limg.grid(columnspan=2, pady=0)

title = Label(parametersFrame, text="f r a c t u s", background="#000000", fg="white", font=("Arial", 25))
title.grid(row=1, columnspan=2, padx=10, pady=2)

minButton = Button(parametersFrame, text="minimize", command=minimize, bg="#000000", fg="gray")
minButton.grid(row=2, column=0, padx=10, pady=10)

quitButton = Button(parametersFrame, text="quit", command=do_quit, bg="#000000", fg="gray")
quitButton.grid(row=2, column=1, padx=10, pady=10)

blankLabel = Label(parametersFrame, text="     ", background="#000000", fg="white")
blankLabel.grid(row=3, column=0, padx=10, pady=2)

startButton = Button(parametersFrame, text="start", command=startClicked, bg="#000000", fg="gray")
startButton.grid(row=4, column=0, padx=10, pady=10)

pauseButton = Button(parametersFrame, text="pause", command=pauseClicked, bg="#000000", fg="gray")
pauseButton.grid(row=4, column=1, padx=10, pady=10)

clearButton = Button(parametersFrame, text="clear", command=clearClicked, bg="#000000", fg="gray")
clearButton.grid(row=5, column=0, padx=10, pady=10)

saveButton = Button(parametersFrame, text="save", command=saveClicked, bg="#000000", fg="gray")
saveButton.grid(row=5, column=1, padx=10, pady=10)

blankLabel = Label(parametersFrame, text="     ", background="#000000", fg="white")
blankLabel.grid(row=6, column=0, padx=10, pady=2)

sidesLabel = Label(parametersFrame, text="vertices", background="#000000", fg="gray")
sidesLabel.grid(row=7, column=0, padx=10, pady=2)
getSides = Entry(parametersFrame, width=8, background="white")  #
getSides.grid(row=7, column=1, padx=10, pady=2)

sideSlider = Scale(parametersFrame, from_=3, to=10, length=300, showvalue=FALSE, orient=HORIZONTAL, command=set_side_slide, fg="white", bg="#000000", bd=0, troughcolor="white")
sideSlider.grid(row=8, column=0, padx=10, pady=2, columnspan=2, sticky=W)

jumpLabel = Label(parametersFrame, text="jump fraction", background="#000000", fg="gray")
jumpLabel.grid(row=9, column=0, padx=10, pady=2)
setJump = Entry(parametersFrame, width=8, background="white")  #
setJump.grid(row=9, column=1, padx=10, pady=2)

jumpSlider = Scale(parametersFrame, from_=0, to=2, resolution=.1, length=300, showvalue=FALSE, orient=HORIZONTAL, command=set_jump_slide, fg="white", bg="#000000", bd=0, troughcolor="white")
jumpSlider.grid(row=10, column=0, padx=10, pady=2, columnspan=2, sticky=W)

radiusLabel = Label(parametersFrame, text="radius", background="#000000", fg="gray")
radiusLabel.grid(row=11, column=0, padx=10, pady=2)
getRadius = Entry(parametersFrame, width=8, background="white")  #
getRadius.grid(row=11, column=1, padx=10, pady=2)

blankLabel = Label(parametersFrame, text="     ", background="#000000", fg="gray")
blankLabel.grid(row=12, column=0, padx=10, pady=2)

Var2 = IntVar()

RBttnLabel = Label(parametersFrame, text="unrestricted", background="#000000", fg="gray")
RBttnLabel.grid(row=13, column=0, padx=10, pady=2)
RBttn = Radiobutton(parametersFrame, borderwidth=0, bg="#000000", variable=Var2, value=1, command=skip_clicked)
RBttn.grid(row=13, column=1, padx=10, pady=2)

RBttn2Label = Label(parametersFrame, text="no double hits", background="#000000", fg="gray")
RBttn2Label.grid(row=14, column=0, padx=10, pady=2)
RBttn2 = Radiobutton(parametersFrame, borderwidth=0, bg="#000000", variable=Var2, value=2, command=skip_clicked)
RBttn2.grid(row=14, column=1, padx=10, pady=2)

RBttn3Label = Label(parametersFrame, text="no triple hits", background="#000000", fg="gray")
RBttn3Label.grid(row=15, column=0, padx=10, pady=2)
RBttn3 = Radiobutton(parametersFrame, borderwidth=0, bg="#000000", variable=Var2, value=3, command=skip_clicked)
RBttn3.grid(row=15, column=1, padx=10, pady=2)

RBttn.select()

blankLabel = Label(parametersFrame, text="     ", background="#000000", fg="white")
blankLabel.grid(row=16, column=0, padx=10, pady=2)

colorButton = Button(parametersFrame, text="color", command=colorClicked, bg="#000000", fg="gray")
colorButton.grid(row=17, column=0, padx=10, pady=2, columnspan=2)

root.mainloop()
