from ultralytics import YOLO
import torch

"""
Use gpu or cpu for training. Gpu will be much much faster but you may need to
install the correct version of torch and cuda for your system.
See https://pytorch.org/get-started/locally/ for more info.

May need to lower the version of ultralytics for older architecture compatibility.
Try to use a different python version and use the latest compatible ultralytics version for that version.
"""

def main():

    # print(torch.cuda.is_available())
    model = YOLO("yolo26n.pt")  # load a pretrained model (recommended for training)
    results = model.train(data="buoy.yaml", epochs=100, imgsz=640, batch=0.8, device=0)
    # results = model.train(data="buoy.yaml", epochs=10, imgsz=640, device='cpu')

if __name__ == "__main__":
    main()