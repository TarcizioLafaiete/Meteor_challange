import cv2
import numpy as np
import sys
from enum import Enum

class Image_Objects(Enum):
    STAR = [255,255,255],
    METEOR = [0,0,255],
    WATER = [255,0,0],
    GROUND =  [0,0,0]


def map_objects_coord(image:np.ndarray) -> tuple[list,list,list]:
    lake_coords = []
    star_coords = []
    meteor_coords = []

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (image[i][j] == Image_Objects.STAR.value).all():
                star_coords.append((i,j))
            elif (image[i][j] == Image_Objects.METEOR.value).all():
                meteor_coords.append((i,j))
            elif (image[i][j] == Image_Objects.WATER.value).all():
                lake_coords.append((i,j))

    return star_coords,meteor_coords,lake_coords

def find_water_line(lakes:list) -> int:
    max_value = max(lakes)[0] + 1
    counter = np.zeros(max_value)
    for points in lakes:
        counter[points[0]] += 1

    counter_list = counter.tolist()
    max_counter = max(counter_list)
    return counter_list.index(max_counter)

def clean_lakes_coord(lakes:list,line:int) -> list:
    clean_lakes = []
    for point in lakes:
        if point[0] == line:
            clean_lakes.append(point[1])
    
    return clean_lakes
    

def counting_perpendicular_meteors(meteors:list,lakes:list) -> int:
    line_of_lakes = find_water_line(lakes)
    lake_points = clean_lakes_coord(lakes,line_of_lakes)
    count = 0
    for meteor in meteors:
        for point in lake_points:
            if meteor[1] == point:
                count += 1
                break
    return count
    

def main(name_image:str) -> None:
    
    image = cv2.imread(name_image,cv2.IMREAD_COLOR)
    stars,meteors,lakes = map_objects_coord(image)
    num_stars = len(stars)
    num_meteors = len(meteors)
    num_perpendicular_meteors = counting_perpendicular_meteors(meteors,lakes)

    print(f"Numero de estrelas: {num_stars} \n Numero de meteoros: {num_meteors} \n Numero de meteoros penpendiculares a agua: {num_perpendicular_meteors}")

if __name__ == "__main__":
    main(sys.argv[1])