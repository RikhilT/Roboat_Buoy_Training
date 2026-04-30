from pathlib import Path
import cv2
import os

"""
Make sure each image and its box file have the same name
Change the images_dir and boxes_dir variables to your actual directories containing the images and box files.

The script will create a "data" folder with "images" and "labels" subfolders,
and further split them into "train" and "val" subfolders. The images will be
"""
images_dir = "images"
boxes_dir = "boxes"


data_img_dir = "data/images/"
data_label_dir = "data/labels/"
os.mkdir("data")
os.mkdir(data_img_dir)
os.mkdir(data_label_dir)
os.mkdir(f"{data_img_dir}train/")
os.mkdir(f"{data_img_dir}val/")
os.mkdir(f"{data_label_dir}train/")
os.mkdir(f"{data_label_dir}val/")

count = 1
num_pics = len(list(Path.iterdir(Path("boxes"))))

for box_file in Path.iterdir(Path("boxes")):
    filename = box_file.stem

    with open(box_file, "r") as f:
        content = f.read().strip()
        boxes = content.split(";")
        boxes.pop()  # Remove the last empty element if any
        for i in range(len(boxes)):
            boxes[i] = boxes[i].split(",")
            boxes[i] = [int(float(coord)) for coord in boxes[i]]

    for i in range(len(boxes)):
        # print(boxes[i])
        x1, y1, x2, y2 = boxes[i]
        for j in range(len(boxes)):
            if i == j:
                continue
            x3, y3, x4, y4 = boxes[j]
            # Check if the top-left and bottom-right corners of box[i] are inside box[j]
            if x1 >= x3 and y1 >= y3 and x2 <= x4 and y2 <= y4:
                print("Found inside box")
                boxes[i] = [-1, -1, -1, -1]  # Mark box as invalid

    img_path = f"{images_dir}\\{filename}.png"
    img = cv2.imread(img_path)
    height, width, _ = img.shape

    if count <= 0.8*num_pics:
        img_subdir = "train/"
    else:
        img_subdir = "val/"

    cv2.imwrite(f"{data_img_dir}{img_subdir}/IMG_{count}.png", img)

    if count <= 0.8*num_pics:
        label_subdir = "train/"
    else:
        label_subdir = "val/"

    with open(f"{data_label_dir}{label_subdir}IMG_{count}.txt", "w") as f:
        for box in boxes:
            x1, y1, x2, y2 = box
            if x1 == -1:
                continue
            center_x = (x1 + x2) / 2 / width
            center_y = (y1 + y2) / 2 / height
            box_width = (x2 - x1) / width
            box_height = (y2 - y1) / height

            if center_x < 0 or center_x > 1 or center_y < 0 or center_y > 1:
                continue
            f.write(f"0 {center_x} {center_y} {box_width} {box_height}\n")

    count += 1
