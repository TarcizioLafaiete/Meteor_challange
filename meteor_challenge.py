import cv2
import numpy as np
import sys
from enum import Enum

class Image_Objects(Enum):
    STAR = [255,255,255],
    METEOR = [0,0,255],
    WATER = [255,0,0],
    GROUND =  [0,0,0]



def counting_pixel(image:np.ndarray,pattern:Image_Objects) -> int:
    count = 0
    for line in image:
        for pixel in line:
            if (pixel == pattern.value).all():
                count += 1

    return count

def find_water_max_line(image:np.ndarray) -> int:

    max_line = 0
    current_line = 0
    max_pixels = 0
    for line in image:
        count_pixels = 0
        for pixel in line:
            if(pixel == Image_Objects.WATER.value).all():
                count_pixels += 1
        
        if count_pixels > max_pixels:
            max_line = current_line
            max_pixels = count_pixels
        current_line += 1

    return max_line

def map_lakes_coord(line:np.ndarray) -> list:
    water_points = []

    for i in range(len(line)):
        if (line[i] == Image_Objects.WATER.value).all():
            water_points.append(i)

    return water_points

def map_meteors_coords(image:np.ndarray) -> list:
    meteors_map = []
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (image[i][j] == Image_Objects.METEOR.value).all():
                meteors_map.append(j)
    return meteors_map

def counting_stars(image:np.ndarray) -> int:
    pattern = Image_Objects.STAR
    return counting_pixel(image,pattern)

def counting_meteors(image:np.ndarray) -> int:
    pattern = Image_Objects.METEOR
    return counting_pixel(image,pattern)

def counting_perpendicular_meteors(image:np.ndarray) -> int:
    water_max_line = find_water_max_line(image)
    lakes_coords = map_lakes_coord(image[water_max_line])
    meteor_maps = map_meteors_coords(image)

    count = 0
    for meteor in meteor_maps:
        for lake_point in lakes_coords:
            if meteor == lake_point:
                count += 1

    return count
    

def main(name_image:str) -> None:
    
    image = cv2.imread(name_image,cv2.IMREAD_COLOR)
    num_stars = counting_stars(image)
    num_meteors = counting_meteors(image)
    num_perpendicular_meteors = counting_perpendicular_meteors(image)
    
    print(f"Numero de estrelas: {num_stars} \n Numero de meteoros: {num_meteors} \n Numero de meteoros penpendiculares a agua: {num_perpendicular_meteors}")

main(sys.argv[1])