folder_train = r"1_686\YOLODataset\labels\train"
folder_val = r"1_686\YOLODataset\labels\val"
import os 

### check class ###
collect_class = set()
for filename in os.listdir(folder_train):
    filepath = os.path.join(folder_train, filename)
    with open (filepath, "r") as f:
        lines = f.readlines()
        for line in lines:
            line_ls = line.split(' ')
            collect_class.update(line_ls[0])
for filename in os.listdir(folder_val):
    filepath = os.path.join(folder_val, filename)
    with open (filepath, "r") as f:
        lines = f.readlines()
        for line in lines:
            line_ls = line.split(' ')
            collect_class.update(line_ls[0])

print (collect_class)