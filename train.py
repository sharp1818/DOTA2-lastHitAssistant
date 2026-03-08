from ultralytics import YOLO
import torch

device = 0 if torch.cuda.is_available() else "cpu"
print(f"Usando dispositivo: {torch.cuda.get_device_name(0) if device == 0 else 'CPU'}")

model = YOLO("yolo26n.pt")

train_results = model.train(
    data="dataset.yaml",
    epochs=100, 
    imgsz=640, 
    device="gpu", 
)

metrics = model.val()
path = model.export(format="onnx") 