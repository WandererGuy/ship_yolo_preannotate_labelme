from ultralytics import YOLO
import os 
import torch
import uuid
import cv2

# Load a model
SAVE_FOLDER = "output"
# os.makedirs(SAVE_FOLDER, exist_ok= True)
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

import shutil
     
if __name__ == "__main__":
    """
    given a folder of only pictures
    filter boat images from frames
    return saved txt yolo output in 1 folder and pic output in another folder 
    """
    import yaml

    # Load the YAML file
    with open("config.yaml", "r") as file:
        data = yaml.safe_load(file)

    tmp_ship = []
    MODEL_PATH = data["MODEL_PATH"]
    model = YOLO(MODEL_PATH)  # pretrained YOLO11n model
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print (device)
    model.to(device)

    KEY_CLASS_KEEP_LIST = data["KEY_CLASS_KEEP_LIST"]
    import argparse
    # Set up argument parser
    parser = argparse.ArgumentParser(description='convert coco txt to labelme json.')
    parser.add_argument('--image_input_folder', type=str, help='Width of the image', required=True)
    parser.add_argument('--txt_output_folder', type=str, help='Height of the image', required=True)
    parser.add_argument('--image_output_folder', type=str, help='yolo txt_filepath', required=True)  # Change to str

    # Parse arguments
    args = parser.parse_args()
    image_input_folder = args.image_input_folder
    txt_output_folder = args.txt_output_folder
    image_output_folder = args.image_output_folder
    image_ls = [os.path.join(image_input_folder, filename) for filename in os.listdir(image_input_folder)]
    os.makedirs(txt_output_folder, exist_ok=True)
    os.makedirs(image_output_folder, exist_ok=True)
    # Process results list
    #### release memory
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
            found_boat = False
            for single_object_result in single_image_result: # loop through objects in 1 image 
                single_object_result_box = single_object_result.boxes
                if int(single_object_result_box.cls.item()) in KEY_CLASS_KEEP_LIST:
                        found_boat = True
                        # xyxy = single_object_result_box.xyxy.cpu().numpy()[0]
                        # img = single_image_result.orig_img
                        # save_detect(xyxy = xyxy, 
                        #             img = img, 
                        #             img_path = single_image_result.path)  
                else:
                        continue 
                
            if found_boat:
                print (single_image_result.path)
                print ("find interested object")
                filename = os.path.basename(single_image_result.path)
                # single_image_result.save(os.path.join(SAVE_FOLDER, filename))
                name = os.path.basename(single_image_result.path).split(".")[0] + ".txt"
                single_image_result.save_txt(os.path.join(txt_output_folder,name))		
                shutil.copy(single_image_result.path, image_output_folder)

            else: 
                print (single_image_result.path)
                print ("not found interested object")

