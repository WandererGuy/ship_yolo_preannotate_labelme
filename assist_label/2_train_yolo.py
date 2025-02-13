from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("yolo11l.pt")  # load a pretrained model (recommended for training)
    results = model.train(data=r"1_686\YOLODataset\dataset.yaml", epochs=100, imgsz=640)
