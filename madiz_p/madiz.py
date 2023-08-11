"""
This script uses Raspberry Pi camera to capture pictures and analyze the radiation background.
The script counts the number of exposed pixels, classifies them into groups
and then puts the corresponding data into a log file for further analysis.
"""

import sys
import datetime
from io import BytesIO
from PIL import Image, ImageEnhance
import numpy as np
import picamera

def is_overexposed(img):
    """
    Check if the image is overexposed.
    Parameters:
        img - input image
    Return:
        True if the image is overexposed, False otherwise
    """

    pixel_values = list(img.getdata())
    mean_intensity = sum(pixel_values) / len(pixel_values)
    threshold = 100
    return mean_intensity > threshold

def count_pixels(img, const, fixed = False):
    """
    Count the number of exposed pixels.
    Parameters:
        img - input image
        const - constant value to be added to the threshold
        fixed - set the threshold to 80 if fixed is True
    Return:
        threshold
        np.array of the exposed pixels
        np.array of groups of pixels
    """

    pixel_brightness = np.asarray(img, dtype='uint8')
    if fixed:
        average = 80
    else:
        average = np.sum(pixel_brightness) / (img.size[0] * img.size[1]) + const

    filt = pixel_brightness >= average

    pixel_brightness = pixel_brightness[filt]

    enhancer = ImageEnhance.Brightness(img)
    factor = 255
    img = enhancer.enhance(factor)

    newsize = (img.size[0] // 99, img.size[1] // 99)
    img_resize = img.resize(newsize)
    enhancer = ImageEnhance.Brightness(img_resize)
    factor = 80
    img_resize_enhance = enhancer.enhance(factor)
    group_brightness = np.asarray(img_resize_enhance, dtype='uint8')

    average = np.sum(group_brightness) / (img_resize_enhance.size[0] * img_resize_enhance.size[1]) + const

    filt = group_brightness >= average

    group_brightness = group_brightness[filt]

    return average, pixel_brightness, group_brightness

def get_groups(num_ar, pos, visited = [], coord_list = [], group_list = []):
    """
    Classify exposed pixels into groups using recursion.
    Parameters:
        num_ar - np.array of the coordinates of the exposed pixels
        pos - coordinates of the entry point
        visited - list of the visited pixels
        coord_list - list of the exposed pixels in one group
        group_list - list of the groups of the exposed pixels
    Return:
        group_list - list of the groups of the exposed pixels
    """

    if pos in visited:
        return group_list
    visited.append(pos)

    if pos not in coord_list:
        coord_list.append(pos)

    num_ar = np.delete(num_ar, num_ar.tolist().index(pos), 0)

    neighbors = [[pos[0] + 1, pos[1]],
                 [pos[0], pos[1] + 1],
                 [pos[0] - 1, pos[1]],
                 [pos[0], pos[1] - 1],
                 [pos[0] - 1, pos[1] + 1],
                 [pos[0] + 1, pos[1] - 1],
                 [pos[0] + 1, pos[1] + 1],
                 [pos[0] - 1, pos[1] - 1]]

    for neighbor in neighbors:
        if neighbor in num_ar.tolist():
            coord_list.append(neighbor)
            return get_groups(num_ar, neighbor, visited, coord_list, group_list)

    if num_ar.tolist() == []:
        return group_list

    group_list.append(coord_list)
    coord_list = []

    return get_groups(num_ar, num_ar[0].tolist(), visited, coord_list, group_list)

def count_groups(img, average):
    """
    Prepare the image for the get_groups function.
    Parameters:
        img - input image
        average - threshold for the binarization
    Return:
        number of the groups of the exposed pixels
    """

    width, height = img.size
    const_br = average
    br_list = np.asarray(img, dtype='uint8').T

    x = np.arange(0, width)
    y = np.arange(0, height)
    num_ar = np.array(np.meshgrid(x, y)).T
    num_ar = num_ar[br_list > const_br]
    if len(num_ar) == 0:
        group_list = []
    else:
        group_list = get_groups(num_ar, num_ar[0].tolist())

    return len(group_list)

save_image = bool(sys.argv[1])

while True:

    stream = BytesIO()
    with picamera.PiCamera() as camera:
        camera.start_preview()
        camera.resolution = (3280, 2464)
        camera.shutter_speed = 3000000
        camera.ISO = 800
        camera.capture(stream, format="jpeg")
        stream.seek(0)
        image = Image.open(stream).convert("L")
        if save_image:
            a = f"{str(datetime.datetime.now())}.png"
            image.save(a)

    const1 = 7
    const2 = 9
    const3 = 11
    const4 = 15
    const5 = 17
    pixel_brightness_const6 = np.asarray(image, dtype='uint8')
    const6 = np.sum(pixel_brightness_const6) / (image.size[0] * image.size[1]) / 32

    average1, pixel_brightness1, group_brightness1 = count_pixels(image, const1)
    average2, pixel_brightness2, group_brightness2 = count_pixels(image, const2)
    average3, pixel_brightness3, group_brightness3 = count_pixels(image, const3)
    average4, pixel_brightness4, group_brightness4 = count_pixels(image, const4)
    average5, pixel_brightness5, group_brightness5 = count_pixels(image, const5)
    average6, pixel_brightness6, group_brightness6 = count_pixels(image, const6)
    average7, pixel_brightness7, group_brightness7 = count_pixels(image, 80, True)

    with open("20230719.csv", "a") as file:
        file.write(str(datetime.datetime.now()) + ";" +
                   str(is_overexposed(image)) + ";" +
                   str(int(average1)) + ";" +
                   str(len(pixel_brightness1)) + ";" +
                   str(len(group_brightness1)) + ";" +
                   str(count_groups(image, average1)) + ";" +
                   str(int(average2)) + ";" +
                   str(len(pixel_brightness2)) + ";" +
                   str(len(group_brightness2)) + ";" +
                   str(count_groups(image, average2)) + ";" +
                   str(int(average3)) + ";" +
                   str(len(pixel_brightness3)) + ";" +
                   str(len(group_brightness3)) + ";" +
                   str(count_groups(image, average3)) + ";" +
                   str(int(average4)) + ";" +
                   str(len(pixel_brightness4)) + ";" +
                   str(len(group_brightness4)) + ";" +
                   str(count_groups(image, average4)) + ";" +
                   str(int(average5)) + ";" +
                   str(len(pixel_brightness5)) + ";" +
                   str(len(group_brightness5)) + ";" +
                   str(count_groups(image, average5)) + ";" +
                   str(len(pixel_brightness6)) + ";" +
                   str(len(group_brightness6)) + ";" +
                   str(count_groups(image, average6)) + ";" +
                   str(len(pixel_brightness7)) + ";" +
                   str(len(group_brightness7)) + ";" +
                   str(count_groups(image, average7)) + "\n")
