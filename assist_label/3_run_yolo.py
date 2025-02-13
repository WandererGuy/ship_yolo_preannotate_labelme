from ultralytics import YOLO
import os 
import torch
import uuid
import cv2

# Load a model
# SAVE_FOLDER = "output"
# os.makedirs(SAVE_FOLDER, exist_ok= True)
IMAGE_INTO_MEM = 100
SAVE_SHIP_FOLDER = "only_ships"
# os.makedirs(SAVE_SHIP_FOLDER, exist_ok= True)

os.makedirs("5_image_have_ships", exist_ok= True)
os.makedirs("6_image_have_ships_txt", exist_ok= True)

def save_detect(xyxy, img, img_path):
    # Extract coordinates
    x1, y1, x2, y2 = xyxy
    y1 = int(y1)
    x1 = int(x1)
    y2 = int(y2)
    x2 = int(x2)
    # Crop the image
    cropped_img = img[y1:y2, x1:x2]
    name = str(uuid.uuid4()) + ".jpg"
    # Optionally, save or display the cropped image
    sub_folder = os.path.basename(img_path).split(".")[0]
    os.makedirs(os.path.join(SAVE_SHIP_FOLDER, sub_folder), exist_ok= True)
    cv2.imwrite(os.path.join(SAVE_SHIP_FOLDER, sub_folder, name), cropped_img)

import shutil
     
if __name__ == "__main__":

    tmp_ship = []
    model = YOLO("best.pt")  # pretrained YOLO11n model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print (device)
    model.to(device)
    image_ls = [os.path.join("IMAGES", filename) for filename in os.listdir("IMAGES")]
    chunk_image_ls = []
    tmp = []
    for index, image_path in enumerate(image_ls):   
        if index == len(image_ls) - 1:
            tmp.append(image_path)
            chunk_image_ls.append(tmp)
            break
        if index % IMAGE_INTO_MEM == 0 and index != 0:
            chunk_image_ls.append(tmp)
            tmp = []
        else:
            tmp.append(image_path)
    for chunk in chunk_image_ls:
        for single_image_result in model.predict(
            source = chunk,
            batch=8,
            conf=0.40,
            imgsz=640,
            verbose=True,
            save=False,
            stream=True
        ):
            print ("----------------------------------------------------")
            for single_object_result in single_image_result: # loop through objects in 1 image 
                single_object_result_box = single_object_result.boxes
                
            print (single_image_result.path)
            print ("BOATTTTTTTTTTT")
            filename = os.path.basename(single_image_result.path)
            # single_image_result.save(os.path.join(SAVE_FOLDER, filename))
            name = os.path.basename(single_image_result.path).split(".")[0] + ".txt"
            single_image_result.save_txt(f"6_image_have_ships_txt/{name}")		
            shutil.copy(single_image_result.path, "5_image_have_ships")

