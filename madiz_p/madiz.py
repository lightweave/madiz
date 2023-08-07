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


def count_pixels(img, const, fixed=False):
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

    pixel_brightness = np.asarray(img, dtype="uint8")

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
    group_brightness = np.asarray(img_resize_enhance, dtype="uint8")

    average = np.sum(group_brightness) / (img_resize_enhance.size[0] * img_resize_enhance.size[1]) + const

    filt = group_brightness >= average

    group_brightness = group_brightness[filt]

    return average, pixel_brightness, group_brightness


def get_coords(index, img_width):
    """
    Convert the index to coordinates.
    Parameters:
        index - index of the pixel in a 1d-array
        img_width - width of the image
    Return:
        pair of the coordiantes of a 2d-array
    """

    x_coord = index % img_width
    y_coord = index // img_width
    return (x_coord, y_coord)


def get_index(img_coords, img_width):
    """
    Convert coordinates to the index.
    Parameters:
        img_coords - coordinates of the pixel in a 2d-array
        img_width - width of the image
    Return:
        index of a 1d-array
    """

    return img_width * img_coords[1] + img_coords[0]


def get_neighbors(img_coords):
    """
    Get neighbors of the specified coordinates.
    Parameters:
        img_coords - coordinates of the pixel in a 2d-array
    Return:
        list of the coordinates of the neighboring pixels
    """

    img_neighbors = [
        (img_coords[0], img_coords[1] + 1),
        (img_coords[0] + 1, img_coords[1] + 1),
        (img_coords[0] + 1, img_coords[1]),
        (img_coords[0] + 1, img_coords[1] - 1),
        (img_coords[0], img_coords[1] - 1),
        (img_coords[0] - 1, img_coords[1] - 1),
        (img_coords[0] - 1, img_coords[1]),
        (img_coords[0] - 1, img_coords[1] + 1),
    ]
    return img_neighbors


def get_groups(br_list, width, height):
    """
    Get groups of the exposed pixels.
    Parameters:
        br_list - binarized np.array with exposed pixels
        width - width of the image
        height - height of the image
    Return:
        groups of the exposed pixels
    """

    i = 0
    cloud, neighbors, groups = [], [], []

    while i != width * height - 1:
        if br_list[i] == 1:
            br_list[i] = 0
            coords = get_coords(i, width)
            cloud.append(coords)
            for neighbor in get_neighbors(coords):
                if br_list[get_index(neighbor, width)] == 1:
                    br_list[get_index(neighbor, width)] = 0
                    neighbors.append(neighbor)

            while len(neighbors) != 0:
                neighbor = neighbors[-1]
                cloud.append(neighbor)
                neighbors.remove(neighbor)
                for n2 in get_neighbors(neighbor):
                    if br_list[get_index(n2, width)] == 1:
                        br_list[get_index(n2, width)] = 0
                        neighbors.append(n2)

            groups.append(cloud)
            cloud = []
        i += 1

    return groups


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
    br_list = np.asarray(img, dtype="uint8")
    br_list = np.where(br_list > average, 1, 0)
    br_list = br_list.flatten()

    if len(br_list) == 0:
        group_list = []
    else:
        group_list = get_groups(br_list, width, height)

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
