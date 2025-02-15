from ultralytics import YOLO
import os 
import torch
import uuid
import cv2
import shutil
import yaml
import argparse
IMAGE_INTO_MEM = 100
SAVE_SHIP_FOLDER = "only_ships"
# os.makedirs(SAVE_SHIP_FOLDER, exist_ok= True)

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

def save_cropped_objects(single_image_result, single_object_result):
        xyxy = single_object_result.boxes.xyxy.cpu().numpy()[0]
        img = single_image_result.orig_img
        save_detect(xyxy = xyxy, 
                    img = img, 
                    img_path = single_image_result.path)  
        
def create_chunks(image_ls: list[str]) -> list[list[str]]:
    """
    divided into chunks, then batches 
    """
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

    return chunk_image_ls

def handle_found_object(single_image_result, txt_output_folder: str, image_output_folder: str) -> None:
        print (single_image_result.path)
        print ("find interested object")
        filename = os.path.basename(single_image_result.path)
        name = filename.split(".")[0] + ".txt"
        single_image_result.save_txt(os.path.join(txt_output_folder,name))		
        shutil.copy(single_image_result.path, image_output_folder)
     
def main():
    """
    given a folder of only images
    filter images (with interested object) from the folder
    return saved txt yolo output (in 1 folder) and pic output (in another folder) 
    """
    with open("config.yaml", "r") as file:
        data = yaml.safe_load(file)

    MODEL_PATH = data["MODEL_PATH"]
    KEY_CLASS_KEEP_LIST = data["KEY_CLASS_KEEP_LIST"]

    model = YOLO(MODEL_PATH)  # pretrained YOLO11n model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print (device)
    model.to(device)

    parser = argparse.ArgumentParser(description='convert coco txt to labelme json.')
    parser.add_argument('--image_input_folder', type=str, help='Width of the image', required=True)
    parser.add_argument('--txt_output_folder', type=str, help='Height of the image', required=True)
    parser.add_argument('--image_output_folder', type=str, help='yolo txt_filepath', required=True)  # Change to str

    args = parser.parse_args()
    image_input_folder = args.image_input_folder
    txt_output_folder = args.txt_output_folder
    image_output_folder = args.image_output_folder
    os.makedirs(txt_output_folder, exist_ok=True)
    os.makedirs(image_output_folder, exist_ok=True)

    #### release memory by streaming 
    image_ls = [os.path.join(image_input_folder, filename) for filename in os.listdir(image_input_folder)]
    chunk_image_ls = create_chunks(image_ls)
    for chunk in chunk_image_ls:
        for batch_yolo_result in model.predict(
            source = chunk,
            batch=8,
            conf=0.40,
            imgsz=640,
            verbose=True,
            save=False,
            stream=True
        ):
            for single_image_result in batch_yolo_result:
                print ("----------------------------------------------------")
                found_object = False
                for single_object_result in single_image_result: # loop through objects in 1 image 
                    if int(single_object_result.boxes.cls.item()) in KEY_CLASS_KEEP_LIST:
                            found_object = True
                            # save_cropped_objects(single_image_result, single_object_result)
                    else:
                            continue 
                if found_object:
                    handle_found_object(single_image_result, txt_output_folder, image_output_folder)
                else: 
                    print (single_image_result.path)
                    print ("not found interested object")

if __name__ == "__main__":
    main()