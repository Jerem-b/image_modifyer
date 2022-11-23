import PySimpleGUI as sg
from PIL import Image, ImageOps
import io, os
import numpy as np
import math
import pyautogui

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]

w_screen, h_screen = pyautogui.size()

def get_img_data(f, maxsize=(w_screen, h_screen), first=False):
        img = Image.open(f)
        img.thumbnail(maxsize)
        if first:
            bio = io.BytesIO()
            img.save(bio, format="PNG")
            del img
            return bio.getvalue()
        return ImageTk.PhotoImage(img)

default_image = "./ressources/img/app_logo.jpg"
tmp_img_name = 'temporary_image.png'
open_image = default_image
is_modifiable = False
can_save = False

menu_start = ['File', ['Open', '!Save', 'Close']], ['!Transformations', ['Turn left', 'Turn right', 'Mirror', 'Scale']], ['!Filters', ['Black and white', 'Red cutter', 'Green cutter', 'Blue cutter', 'Pixellate']]
menu_editing = ['File', ['Open', 'Save', 'Close']], ['Transformations', ['Turn left', 'Turn right', 'Mirror', 'Scale']], ['Filters', ['Black and white', 'Red cutter', 'Green cutter', 'Blue cutter', 'Pixellate']]

menu = sg.Menu(menu_start, background_color='white',text_color='black')
image_elem = sg.Image(data=get_img_data(open_image, first=True))

layout = [
                [menu],
                [image_elem]
        ]

def block_focus(window):
    for key in window.key_dict:
        element = window[key]
        if isinstance(element, sg.Button):
            element.block_focus()

def save_as_popup():
    name = sg.InputText(key='text')
    folder_info = os.listdir()

    layout = [
            [sg.Text('Files inside the current folder: ')],
            [sg.Listbox(values=folder_info, select_mode='extended', size=(30, 6))],
            [sg.Text('Save Image as: ')],
            [name],
            [sg.Button('Save'), sg.Button('Cancel')],
        ]
    window = sg.Window("Save", layout, finalize=True)
    block_focus(window)
    while True:
        event, values = window.read()
        if event == 'Cancel':
            window.close()
            return False, ''
        if values['text'].lower().endswith(('.png', '.jpeg', '.jpg')) == True:
            window.close()
            return True, values['text']
        else:
            sg.Popup('Incorrect Extension name !')

#Transformations
def rotate_left(f):
        im = Image.open(f)
        im = im.rotate(90, expand=1)
        im.save(tmp_img_name)
        image_elem.update(data=get_img_data(tmp_img_name, first=True))
        im.close()
        window.Refresh()

def rotate_right(f):
        im = Image.open(f)
        im = im.rotate(-90, expand=1)
        im.save(tmp_img_name)
        image_elem.update(data=get_img_data(tmp_img_name, first=True))
        im.close()
        window.Refresh()

def mirror(f):
        im = Image.open(f)
        im = ImageOps.mirror(im)
        im.save(tmp_img_name)
        image_elem.update(data=get_img_data(tmp_img_name, first=True))
        im.close()
        window.Refresh()

def scale(f):
        im = Image.open(f)
        curr_w, curr_h = im.size
        width = sg.popup_get_text('Select the new width in px: (current width: ' + str(curr_w) + ') ')
        height = sg.popup_get_text('Select the new height in px: (current height: ' + str(curr_h) + ') ')
        if width is None or height is None:
                width = curr_w
                height = curr_h
        elif width.isnumeric() == False or height.isnumeric() == False or int(width) <= 0 or int(height) <= 0:
                width = curr_w
                height = curr_h
                sg.popup_ok('invalid size parameter, please try again !')
        else:
                width = int(width)
                height = int(height)
        im = im.resize((width, height))
        im.save(tmp_img_name)
        image_elem.update(data=get_img_data(tmp_img_name, first=True))
        im.close()
        window.Refresh()


#Filters
def black_and_white(f):
        im = Image.open(f)
        im = im.convert('1')
        im.save(tmp_img_name)
        image_elem.update(data=get_img_data(tmp_img_name, first=True))
        im.close()
        window.Refresh()

def red_cutter(f):
        im = Image.open(f)
        width, height = im.size
        mode = im.mode
        new_image = Image.new(mode, (width, height))
        orig_pixel_map = im.load()
        new_pixel_map = new_image.load()

        for x in range(width):
                for y in range(height):
                        origin_pixel = orig_pixel_map[x, y]
                        modified_pixel = (0, origin_pixel[1], origin_pixel[2])
                        new_pixel_map[x, y] = modified_pixel

        new_image.save(tmp_img_name)
        image_elem.update(data=get_img_data(tmp_img_name, first=True))
        im.close()
        new_image.close()
        window.Refresh()

def green_cutter(f):
        im = Image.open(f)
        width, height = im.size
        mode = im.mode
        new_image = Image.new(mode, (width, height))
        orig_pixel_map = im.load()
        new_pixel_map = new_image.load()

        for x in range(width):
                for y in range(height):
                        origin_pixel = orig_pixel_map[x, y]
                        modified_pixel = (origin_pixel[0], 0, origin_pixel[2])
                        new_pixel_map[x, y] = modified_pixel

        new_image.save(tmp_img_name)
        image_elem.update(data=get_img_data(tmp_img_name, first=True))
        im.close()
        new_image.close()
        window.Refresh()

def blue_cutter(f):
        im = Image.open(f)
        width, height = im.size
        mode = im.mode
        new_image = Image.new(mode, (width, height))
        orig_pixel_map = im.load()
        new_pixel_map = new_image.load()

        for x in range(width):
                for y in range(height):
                        origin_pixel = orig_pixel_map[x, y]
                        modified_pixel = (origin_pixel[0], origin_pixel[1], 0)
                        new_pixel_map[x, y] = modified_pixel

        new_image.save(tmp_img_name)
        image_elem.update(data=get_img_data(tmp_img_name, first=True))
        im.close()
        new_image.close()
        window.Refresh()

def pixellate(f):
        im = Image.open(f)

        percent = sg.popup_get_text('percentage of pixellate: ')

        if percent is None:
                percent = 0
        if percent.isnumeric() == False or int(percent) > 100 or int(percent) < 0:
                percent = 0
                sg.popup_ok('invalid size parameter, please try again !')
        exp = 100 - int(percent)
        result = pow(2, exp)
        imgSmall = im.resize((result,result), resample=Image.Resampling.BILINEAR)
        im = imgSmall.resize(im.size, Image.Resampling.NEAREST)
        im.save(tmp_img_name)
        image_elem.update(data=get_img_data(tmp_img_name, first=True))
        im.close()
        window.Refresh()

sg.theme('DarkTeal4')
window = sg.Window('Image Modifier', layout, resizable=True).Finalize()
window.Maximize()
while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
                break
        if event == 'Open':
                open_image = sg.popup_get_file("Browse an image", file_types=file_types)
                if open_image is None:
                        open_image = default_image
                else:
                        image_elem.update(data=get_img_data(open_image, first=True))
                        is_modifiable = True
                        window.Refresh()
        if event == 'Save':
                im = Image.open(open_image)
                im = im.convert('1')
                can_save, fname = save_as_popup()
        if can_save:
                im.save(fname)
        if event == 'Close':
                break
        if is_modifiable == True:
                menu.update(menu_editing)

        #transformations
        if event == 'Turn left':
                rotate_left(open_image)
                open_image = tmp_img_name;
        if event == 'Turn right':
                rotate_right(open_image)
                open_image = tmp_img_name;
        if event == 'Mirror':
                mirror(open_image)
                open_image = tmp_img_name;
        if event == 'Scale':
                scale(open_image)
                open_image = tmp_img_name;

        #filters
        if event == 'Black and white':
                black_and_white(open_image)
                open_image = tmp_img_name;
        if event == 'Red cutter':
                red_cutter(open_image)
                open_image = tmp_img_name;
        if event == 'Blue cutter':
                blue_cutter(open_image)
                open_image = tmp_img_name;
        if event == 'Green cutter':
                green_cutter(open_image)
                open_image = tmp_img_name;
        if event == 'Pixellate':
                pixellate(open_image)
                open_image = tmp_img_name;

os.remove(tmp_img_name)
window.close()
