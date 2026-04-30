from pathlib import Path
import cv2

"""
This code makes the bounding box images from the raw Unreal Engine output.
Mostly to see if the boxes look correct for the image before making data folder and training.
"""

image = ""
box_file = ""

objects = ["Red", "Lime", "Blue", "Orange", "Cranberry", "Yellow", "White", "Black"]

with open(box_file, "r") as f:
    content = f.read().strip()
    boxes = content.split("\n")
    boxes.pop()
    for i in range(len(boxes)):
        boxes[i] = boxes[i].split(" ")
        boxes[i] = [float(coord) for coord in boxes[i]]

img = cv2.imread(image)
for box in boxes:
    object, norm_cx, norm_cy, norm_w, norm_h = box
    object = int(object)

    center_x, center_y = int(norm_cx * img.shape[1]), int(norm_cy * img.shape[0])
    width, height = int(norm_w * img.shape[1]), int(norm_h * img.shape[0])

    print(center_x, center_y, width, height)

    width = int(width * 0.8)
    height = int(height * 0.8)

    color = objects[object]
    x1, y1, x2, y2 = center_x - width // 2, center_y - height // 2, center_x + width // 2, center_y + height // 2

    # x1, y1, x2, y2 = box
    cv2.rectangle(img, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)
    cv2.putText(img, color, (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # cv2.circle(img, (center_x, center_y), 5, (0, 0, 255), -1)

# cv2.imshow("image", img)
cv2.imwrite("result.png", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
