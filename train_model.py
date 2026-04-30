from ultralytics import YOLO

"""
Use gpu or cpu for training. Gpu will be much much faster but you may need to
install the correct version of torch and cuda for your system.
See https://pytorch.org/get-started/locally/ for more info.

May need to lower the version of ultralytics for older architecture compatibility.
Try to use a different python version and use the latest compatible ultralytics version for that version.
"""

model = YOLO("yolo11n.pt")  # load a pretrained model (recommended for training)
results = model.train(data="buoy.yaml", epochs=10, imgsz=640, device=0)
# results = model.train(data="buoy.yaml", epochs=10, imgsz=640, device='cpu')