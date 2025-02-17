import cv2
import json 
import os 
from tqdm import tqdm 
import copy
import base64
EXAMPLE_JSON = {
  "version": "5.6.1",
  "flags": {},
  "shapes": [
  ],
  "imagePath": "",
  "imageData": None,
  "imageHeight": 0,
  "imageWidth": 0
}
os.makedirs("json_files", exist_ok=True)

def encode_image_data(image_path):
    # Open the image file in binary mode
    with open(image_path, "rb") as image_file:
        # Read the image file and encode it in base64
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

def extract_width_height(filepath):
    # Read the image
    image = cv2.imread(filepath)

    # Get the height and width of the image
    height, width, channels = image.shape
    return width, height

def read_yolo_coor(txt_filepath):
    yolo_coor_ls = []
    with open(txt_filepath, "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            value = line.split(' ')
            class_id, x_center, y_center, width, height = value
            yolo_coor_ls.append([class_id, float(x_center), float(y_center), float(width), float(height)])
    return yolo_coor_ls

def coor2coor(yolo_coor, imageWidth, imageHeight):
    x_center, y_center, width, height = yolo_coor
    x_center = x_center * imageWidth
    y_center = y_center * imageHeight
    width = width * imageWidth
    height = height * imageHeight

    x_min = x_center - width / 2
    y_min = y_center - height / 2
    x_max = x_center + width / 2
    y_max = y_center + height / 2

    return [x_min, y_min, x_max, y_max]



class Total_example_json:
    def __init__(self):
        self.result = copy.deepcopy(EXAMPLE_JSON)
        self.result["imageData"] = None
    def add_object(self, new_object_json):
        self.result["shapes"].append(new_object_json)
    def add_json_coor(self, object_json_coor):
        xmin, ymin, xmax, ymax = object_json_coor
        new_object_json = {
                "label": "boat",
                "points": [
                    [
                    xmin,
                    ymin
                    ],
                    [
                    xmax,
                    ymax
                    ]
                ],
                "group_id": None,
                "description": "",
                "shape_type": "rectangle",
                "flags": {},
                "mask": None
                }
        self.add_object(new_object_json)
    def add_image_path(self, filename):
        self.result["imagePath"] = filename
        
    def add_image_width_height(self, imageWidth, imageHeight):
        self.result["imageHeight"] = imageHeight
        self.result["imageWidth"] = imageWidth
    def add_image_data(self, image_path):
        self.result["imageData"] = encode_image_data(image_path)
class OneObject:
    def __init__(self, imageHeight, imageWidth, yolo_coor):
        self.imageHeight = imageHeight
        self.imageWidth = imageWidth
        self.class_id = yolo_coor[0]
        self.yolo_coor = yolo_coor[1:]
    def process_coor(self):
        x_min, y_min, x_max, y_max = coor2coor(self.yolo_coor, self.imageWidth, self.imageHeight)
        return [x_min, y_min, x_max, y_max]

import yaml
if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        data = yaml.safe_load(file)

    KEY_CLASS_KEEP_LIST = data["KEY_CLASS_KEEP_LIST"]

    img_ls = []
    count = 0 
    import argparse
    # Set up argument parser
    parser = argparse.ArgumentParser(description='convert coco txt to labelme json.')
    parser.add_argument('--image_input_folder', type=str, help='Width of the image', required=True)
    parser.add_argument('--txt_input_folder', type=str, help='Height of the image', required=True)
    parser.add_argument('--json_output_folder', type=str, help='yolo txt_filepath', required=True)  # Change to str

    # Parse arguments
    args = parser.parse_args()
    image_input_folder = args.image_input_folder
    txt_input_folder = args.txt_input_folder
    json_output_folder = args.json_output_folder
    os.makedirs(json_output_folder, exist_ok=True)
    # json_output_folder = "test_output"
    for filename in tqdm(os.listdir(image_input_folder), total = len(os.listdir(image_input_folder))):
        count +=1 
        # if count <= 22000:
        #     continue 
        print (count)
        filepath = os.path.join(image_input_folder, filename)
        filename_id = filename.split(".")[0]
        if filename.endswith('.jpg') or filename.endswith('.png'):
            created = False
            txt_filepath = os.path.join(txt_input_folder, filename.replace(".jpg", ".txt").replace(".png", ".txt"))
            yolo_coor_ls = read_yolo_coor(txt_filepath)
            width, height = extract_width_height(filepath)
            
            for yolo_coor in yolo_coor_ls:
                one_object = OneObject(imageHeight = height,
                                imageWidth = width, 
                                yolo_coor = yolo_coor)
                
                one_object_json_coor = one_object.process_coor()
                
                if int(one_object.class_id) in KEY_CLASS_KEEP_LIST:
                    if created == False:
                        res = Total_example_json()
                        res.add_image_path(filename = filename)
                        res.add_image_data(image_path = filepath)
                        res.add_image_width_height(imageWidth = width, 
                            imageHeight = height)
                        created = True
                    res.add_json_coor(one_object_json_coor)
            dump_file = os.path.join(json_output_folder,filename_id + ".json")
            
            with open(dump_file, 'w') as file:
                json.dump(res.result, file, indent=4)

            
        


        
        
        




