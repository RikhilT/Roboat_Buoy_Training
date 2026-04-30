import numpy as np
import os
from pathlib import Path
import cv2

"""
This code makes the bounding box images from the raw Unreal Engine output.
Mostly to see if the boxes look correct for the image before making data folder and training.

Change directory variables as needed
"""

images_dir = "images"
boxes_dir = "boxes"
output_dir = "outputs"

for box_file in Path.iterdir(Path("boxes")):
    filename = box_file.stem
    with open(box_file, "r") as f:
        content = f.read().strip()
        boxes = content.split(";")
        boxes.pop()  # Remove the last empty element if any
        for i in range(len(boxes)):
            boxes[i] = boxes[i].split(",")
            boxes[i] = [int(float(coord)) for coord in boxes[i]]
        # print(boxes)

    img_path = f"{images_dir}\\{filename}.png"
    img = cv2.imread(img_path)
    for box in boxes:
        # center_x, center_y, height, width = box
        # cv2.rectangle(img, (center_x - width // 2, center_y - height // 2),
        #               (center_x + width // 2, center_y + height // 2),
        #               color=(0, 0, 255), thickness=2)
        x1, y1, x2, y2 = box
        cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)  # Draw red rectangles

    cv2.imwrite(f"{output_dir}/{filename}_output.png", img)  # Save the image with boxes
