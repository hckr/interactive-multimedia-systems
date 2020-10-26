from tkinter import *
import tkinter.font as font
import tkinter.messagebox as messagebox
from PIL import Image
from PIL import ImageTk
import cv2
import random
import os
import json

from imagevariants import generate_jpeg_variants


def main():
    original_image = cv2.imread(os.path.join(
        sys.path[0], 'image-grayscale.png'), cv2.IMREAD_UNCHANGED)

    image_variants = generate_jpeg_variants(original_image)
    random.shuffle(image_variants)

    root = Tk()

    image = ImageTk.PhotoImage(Image.fromarray(original_image))
    image_panel = Label(image=image)
    image_panel.pack(side="bottom")

    ranks = []
    current_index = 0

    button_font = font.Font(size=24)

    rank_buttons_frame = Frame(root)
    Label(rank_buttons_frame, text="Perceived quality of the following image:").grid(
        row=0, column=0, columnspan=5)

    def rank_selection_handler_factory(rank):
        def impl():
            nonlocal root, image, current_index
            ranks.append((image_variants[current_index][0], rank))
            current_index += 1
            if current_index >= len(image_variants):
                messagebox.showinfo("Thanks!", "Thank you for your time")
                root.destroy()
                return
            image = ImageTk.PhotoImage(
                Image.fromarray(image_variants[current_index][1]))
            image_panel.configure(image=image)
            update_count_label()
        return impl

    for i in range(5):
        rank = i + 1
        Button(rank_buttons_frame, text=rank, font=button_font,
               width=5, command=rank_selection_handler_factory(rank)).grid(row=1, column=i)

    count_label = Label(rank_buttons_frame, text="")
    count_label.grid(row=2, column=0, columnspan=5)

    def update_count_label():
        nonlocal count_label
        count_label.configure(
            text=f"{current_index + 1}/{len(image_variants)}")

    update_count_label()

    start_button_frame = Frame(root)

    def start_handler():
        nonlocal image
        image = ImageTk.PhotoImage(Image.fromarray(
            image_variants[current_index][1]))
        image_panel.configure(image=image)
        start_button_frame.destroy()
        rank_buttons_frame.pack(side="top")
        root.update()

    Label(start_button_frame, text="Below you can see an original grayscale image.\nYour task is to rank the quality of the following transformed images.").grid(row=0, column=0)
    Button(start_button_frame, text="Continue", font=button_font,
           command=start_handler).grid(row=1, column=0)
    start_button_frame.pack(side="top")

    root.mainloop()
    print(json.dumps(ranks))


if __name__ == '__main__':
    main()
