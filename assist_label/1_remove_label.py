folder_train = r"1_686\YOLODataset\labels\train"
folder_val = r"1_686\YOLODataset\labels\val"
import os 

### excessive class 3 -> 0 ###
# names: ['0', '3', '1', 'boat'] in yaml file 

class_need_replace = "3"
class_replace_in = "0"
# dest_folder = r"refined\train"
dest_folder_train = r"refined\train"
os.makedirs(dest_folder_train, exist_ok=True)

for filename in os.listdir(folder_train):
    filepath = os.path.join(folder_train, filename)
    dest_filepath = os.path.join(dest_folder_train, filename)
    with open (dest_filepath, "w") as fout:
        print ('written in', dest_filepath)
        dest_ls = []
        with open (filepath, "r") as f:
            lines = f.readlines()
            for line in lines:
                line_ls = line.split(' ')
                if line_ls[0] == class_need_replace:
                    new_line = class_replace_in + line[1:]
                    dest_ls.append(new_line)
                else:
                    dest_ls.append(line)
            for item in dest_ls:
                fout.write(item)


### excessive class 3 -> 0 ###
# names: ['0', '3', '1', 'boat']
class_need_replace = "3"
class_replace_in = "0"
# dest_folder = r"refined\train"
dest_folder_val = r"refined\val"
os.makedirs(dest_folder_val, exist_ok=True)

for filename in os.listdir(folder_val):
    filepath = os.path.join(folder_val, filename)
    dest_filepath = os.path.join(dest_folder_val, filename)
    with open (dest_filepath, "w") as fout:
        print ('written in', dest_filepath)
        dest_ls = []
        with open (filepath, "r") as f:
            lines = f.readlines()
            for line in lines:
                line_ls = line.split(' ')
                if line_ls[0] == class_need_replace:
                    new_line = class_replace_in + line[1:]
                    dest_ls.append(new_line)
                else:
                    dest_ls.append(line)
            for item in dest_ls:
                fout.write(item)