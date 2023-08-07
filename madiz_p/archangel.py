"""
Identify blobs of exposed pixels on the image
"""

from PIL import Image
import numpy as np


def get_coords(index, img_width):
    """
    Convert the index to coordinates
    """
    x_coord = index % img_width
    y_coord = index // img_width
    return (x_coord, y_coord)


def get_index(img_coords, img_width):
    """
    Convert coordinates to the index
    """
    return img_width * img_coords[1] + img_coords[0]


def get_neighbors(img_coords):
    """
    Get neighbors of the specified coordinates
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


img = Image.open("long_exposure13_45.png").convert("L")

width, height = img.size
br_list = np.asarray(img, dtype="uint8")
br_list = np.where(br_list > 80, 1, 0)
br_list = br_list.flatten()

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

print(len(groups))
