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

data_img_dir = "data/images"
data_label_dir = "data/labels"

os.mkdir("data")
os.mkdir(data_img_dir)
os.mkdir(data_label_dir)
os.mkdir(f"{data_img_dir}/train")
os.mkdir(f"{data_img_dir}/val")
os.mkdir(f"{data_label_dir}/train")
os.mkdir(f"{data_label_dir}/val")

objects = ["Red", "Lime", "Blue", "Orange", "Cranberry", "Yellow", "White", "Black"]

count = 1
num_pics = len(os.listdir(images_dir))

for box_file in Path.iterdir(Path(boxes_dir)):
    print(count)
    file_name = box_file.stem

    with open(box_file, "r") as f:
        content = f.read().strip()
        boxes = content.split(";")
        boxes.pop()
        for i in range(len(boxes)):
            boxes[i] = boxes[i].split(" ")
            for item in boxes[i]:
                boxes[i][0] = int(boxes[i][0])
                boxes[i][1] = int(boxes[i][1])
                boxes[i][2] = int(boxes[i][2])
                boxes[i][3] = int(boxes[i][3])

    img_path = f"{images_dir}/{file_name}.png"
    img = cv2.imread(img_path)
    img_height, img_width, _ = img.shape

    if count <= int(0.8 * num_pics):
        subset = "train"
    else:
        subset = "val"

    cv2.imwrite(f"{data_img_dir}/{subset}/IMG_{count}.png", img)

    with open(f"{data_label_dir}/{subset}/IMG_{count}.txt", "w") as f:
        for box in boxes:
            center_x, center_y, width, height, color = box
            width = int(width * 0.8)
            height = int(height * 0.8)
            # Normalize coordinates
            norm_cx = center_x / img_width
            norm_cy = center_y / img_height
            norm_w = width / img_width
            norm_h = height / img_height
            class_id = objects.index(color)

            if norm_cx < 0 or norm_cx > 1 or norm_cy < 0 or norm_cy > 1:
                continue

            f.write(f"{class_id} {norm_cx} {norm_cy} {norm_w} {norm_h}\n")

    count += 1