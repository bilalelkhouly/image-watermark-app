import tkinter.messagebox
from tkinter import *
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageFont, ImageDraw

img = None
watermarked_img = None
FONT = ("Arial", 15, "bold")
BLACK = "#000000"
text_color = (255, 0, 0)
font_size = 50
wm_opacity = 255
font_main = 'arial.ttf'
wm_y = 300
wm_x = 350
original_width = 0
original_height = 0


# ---------------------------- LOAD IMAGE ------------------------------- #
def get_image():
    global img, original_height, original_width
    file_types = [('Jpg Files', '*.jpg'), ('PNG Files', '*.png')]
    filename = filedialog.askopenfilename(filetypes=file_types)
    img = Image.open(filename)
    original_width = img.width
    original_height = img.height
    resized_img = img.resize((700, 600))
    resized_img = ImageTk.PhotoImage(resized_img)
    image_frame.config(image=resized_img)
    image_frame.image = resized_img


# ---------------------------- ADD WATERMARK TEXT ------------------------------- #
def add_text():
    global img, wm_x, wm_y, text_color, font_main, font_size, watermarked_img
    if img:
        original_image = img.copy().convert('RGBA')
        resized_img = original_image.resize((700, 600))
        text_font = ImageFont.truetype(font_main, font_size)
        text = watermark_input.get()
        edit_image = ImageDraw.Draw(resized_img)
        fill_color = (text_color[0], text_color[1], text_color[2], wm_opacity)
        edit_image.text((wm_x, wm_y), text, fill=fill_color, font=text_font)
        resized_img.save('edit.png')
        resized_img = Image.open('edit.png')
        watermarked_img = ImageTk.PhotoImage(resized_img)
        image_frame.config(image=watermarked_img)
        image_frame.image = watermarked_img
    else:
        tkinter.messagebox.showerror("Error", "No image loaded, please upload the image first.")


# ---------------------------- WATERMARK POSITION ------------------------------- #
def up():
    global wm_y
    if wm_y > 5:
        wm_y -= 10
        add_text()
    else:
        tkinter.messagebox.showerror("Error", "Can't move text higher than this point")


def down():
    global wm_y, font_size
    if wm_y < 600 - font_size:
        wm_y += 10
        add_text()
    else:
        tkinter.messagebox.showerror("Error", "Can't move text lower than this point")


def right():
    global wm_x
    if wm_x < 650:
        wm_x += 10
        add_text()
    else:
        tkinter.messagebox.showerror("Error", "Can't move to the right more than this point")


def left():
    global wm_x
    if wm_x > 10:
        wm_x -= 10
        add_text()
    else:
        tkinter.messagebox.showerror("Error", "Can't move to the left more than this point")


# ---------------------------- WATERMARK COLOR ------------------------------- #
def color():
    global text_color
    colors = askcolor(title="Choose Text Color")
    text_color = colors[0]
    add_text()


# ---------------------------- WATERMARK OPACITY ------------------------------- #
def opacity(value):
    global wm_opacity
    wm_opacity = int(value)
    add_text()


# ---------------------------- WATERMARK FONT SIZE ------------------------------- #
def change_font_size():
    global font_size
    font_size = int(font_size_spinbox.get())
    add_text()


# ---------------------------- SAVE IMAGE ------------------------------- #
def save_image():
    global watermarked_img, original_height, original_width
    if watermarked_img:
        file = filedialog.asksaveasfilename(defaultextension='png', filetypes=
                                            [("jpeg", ".jpg"), ("png", ".png"), ("bitmap", "bmp"), ("gif", ".gif")])
        image_to_save = ImageTk.getimage(watermarked_img)
        image_to_save = image_to_save.resize((original_width, original_height))
        image_to_save = image_to_save.convert('RGB')
        image_to_save.save(file)
        tkinter.messagebox.showinfo("Success", "Image has been watermarked and saved!")
    else:
        tkinter.messagebox.showerror("Error", "No image uploaded to save.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Image Watermark Application")
window.minsize(width=500, height=100)
window.config(padx=20, pady=20, bg="#000000")

# ---------------------------- IMAGE SETUP ------------------------------- #
blank_image = Image.new(mode="RGBA", size=(700, 600), color="#7f8383")
image = ImageTk.PhotoImage(blank_image)
image_frame = Label(image=image)
image_frame.image = image
image_frame.grid(column=0, rowspan=6)

# ---------------------------- WATERMARK ------------------------------- #
watermark_label = Label(text="Watermark: ", font=FONT, bg=BLACK, fg="white")
watermark_label.grid(row=0, column=1, padx=20)
watermark_input = Entry(width=50, fg=BLACK)
watermark_input.grid(row=0, column=2, columnspan=3)
add_watermark = Button(text="Add", highlightbackground=BLACK, font=FONT, command=add_text)
add_watermark.grid(row=0, column=5, padx=20)

# ---------------------------- MOVE WATERMARK ------------------------------- #
up_button = Button(text="↑", highlightbackground=BLACK, height=2, width=2, font=("Arial", 30, "bold"), justify='center',
                   command=up)
up_button.grid(row=1, column=3)
down_button = Button(text="↓", highlightbackground=BLACK, height=2, width=2, font=("Arial", 30, "bold"),
                     justify='center', command=down)
down_button.grid(row=3, column=3)
left_button = Button(text="←", highlightbackground=BLACK, height=2, width=2, font=("Arial", 30, "bold"),
                     justify='center', command=left)
left_button.grid(row=2, column=2)
right_button = Button(text="→", highlightbackground=BLACK, height=2, width=2, font=("Arial", 30, "bold"),
                      justify='center', command=right)
right_button.grid(row=2, column=4)

# ---------------------------- WATERMARK COLOR ------------------------------- #
color_label = Label(text="Color:", font=FONT, bg=BLACK, fg="white")
color_label.grid(row=4, column=2)
color_button = Button(text="Pick Color", bg=BLACK, highlightbackground=BLACK, fg=BLACK, command=color)
color_button.grid(row=4, column=3)

# ---------------------------- WATERMARK OPACITY ------------------------------- #
opacity_label = Label(text="Opacity: ", font=FONT, bg=BLACK, fg="white")
opacity_label.grid(row=5, column=2)
opacity_scale = Scale(from_=0, to=255, orient='horizontal', bg=BLACK, fg='white', command=opacity)
opacity_scale.grid(row=5, column=3)

# ---------------------------- WATERMARK FONT SIZE ------------------------------- #
font_size_label = Label(text='Font Size: ', font=FONT, bg=BLACK, fg="white")
font_size_label.grid(row=6, column=2)
default_font_size = tkinter.IntVar(value=50)
font_size_spinbox = Spinbox(from_=1, to=200, textvariable=default_font_size, command=change_font_size)
font_size_spinbox.grid(row=6, column=3)

# ---------------------------- SAVE IMAGE ------------------------------- #
save_button = Button(text="Save Image", command=save_image, bg=BLACK, highlightbackground=BLACK, font=FONT)
save_button.grid(row=7, column=4, padx=20)

# ---------------------------- UPLOAD FILE ------------------------------- #
select_file_button = Button(text="Select file", command=get_image, bg=BLACK, highlightbackground=BLACK, font=FONT)
select_file_button.grid(row=7, column=0, pady=20)

window.mainloop()
