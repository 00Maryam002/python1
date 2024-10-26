import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def load_image():
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if not file_path:
        print("No file selected. Exiting.")
        exit()
    img = Image.open(file_path)
    img.thumbnail((800, 800))
    return img

def set_zoom():
    global zoom_factor
    try:
        zoom_factor = float(zoom_entry.get())
        if zoom_factor <= 0:
            print("Zoom factor must be greater than 0.")
            return
        zoom_window.destroy()  
        display_image()       
    except ValueError:
        print("Invalid input. Please enter a valid number.")

def display_image():
    global original_img, img_label
    img_display = ImageTk.PhotoImage(original_img)
    img_label.configure(image=img_display)
    img_label.image = img_display
    img_label.bind("<Motion>", zoom_image)

def zoom_image(event):
    global original_img, zoom_area_size

    x, y = event.x, event.y

    left = max(x - zoom_area_size // 2, 0)
    upper = max(y - zoom_area_size // 2, 0)
    right = min(x + zoom_area_size // 2, original_img.width)
    lower = min(y + zoom_area_size // 2, original_img.height)

    zoomed_img = original_img.crop((left, upper, right, lower))
    zoomed_img = zoomed_img.resize((int(zoom_area_size * zoom_factor), int(zoom_area_size * zoom_factor)), Image.LANCZOS)

    zoomed_view = ImageTk.PhotoImage(zoomed_img.resize(original_img.size, Image.LANCZOS))
    zoom_label.configure(image=zoomed_view)
    zoom_label.image = zoomed_view


def open_zoom_window():
    global zoom_window, zoom_entry

    zoom_window = tk.Toplevel(root)
    zoom_window.title("Set Zoom Factor")
    
    instruction_label = tk.Label(zoom_window, text="Enter zoom factor (e.g., 1 for 100%, 0.5 for 50%)")
    instruction_label.pack()

    zoom_entry = tk.Entry(zoom_window)
    zoom_entry.pack()

    set_zoom_button = tk.Button(zoom_window, text="Set Zoom", command=set_zoom)
    set_zoom_button.pack()

    root.wait_window(zoom_window)

def main():
    global original_img, img_label, zoom_label, zoom_area_size, root
    
    zoom_area_size = 200

    root = tk.Tk()  
    root.title("Image Zoom Tool")

    original_img = load_image()

    img_frame = tk.Frame(root)
    img_frame.pack(side=tk.TOP, padx=10, pady=10)

    img_label = tk.Label(img_frame)
    img_label.grid(row=0, column=0)

    zoom_label = tk.Label(img_frame)
    zoom_label.grid(row=0, column=1)

    original_image_label = tk.Label(img_frame, text="Original Image")
    original_image_label.grid(row=1, column=0)

    zoomed_image_label = tk.Label(img_frame, text="Zoomed Image")
    zoomed_image_label.grid(row=1, column=1)

    open_zoom_window()

    display_image()

    instructions = tk.Label(root, text="Move your mouse over the original image to see the zoomed output.")
    instructions.pack()

    img_label.configure(cursor="cross")

    root.mainloop()

if __name__ == "__main__":
    main()

