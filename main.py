import tkinter as tk
from PIL import ImageTk
from detect import Detection

def select_image(image_number):
    window.destroy()
    Detection(image_number)

# generate window
window = tk.Tk()
window.title("Select")

# load images
image_files = [
    'component/img1.jpg',
    'component/img2.jpg',
    'component/img3.jpg',
    'component/img4.jpg',
    'component/img5.jpg',
    'component/img6.jpg',
    'component/img7.jpg',
    'component/img8.jpg',
    'component/img9.jpg'
]

images = [ImageTk.PhotoImage(file=image_file) for image_file in image_files]

# create buttons
buttons = []
for i, image in enumerate(images):
    button = tk.Button(
        window,
        image=image,
        relief=tk.FLAT,
        command=lambda i=i: select_image(i + 1)
    )
    buttons.append(button)

# create select message
select_message = tk.Button(
    window,
    text="Please select an image",
    background='white',
    width=100,
    padx=5,
    pady=5,
    font=('Helvetica 15 bold'),
    foreground='black'
)

# grid layout for buttons
rows = 3
columns = 3
for i, button in enumerate(buttons):
    row = i // columns + 1
    column = i % columns + 1
    button.grid(row=row, column=column)

# place select message
select_message.grid(row=0, column=1, columnspan=3)

# run window
window.mainloop()
