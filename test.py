import base64

# Open the image file in binary mode
with open("test/0a06e462-70e8-45eb-85ff-794534860476.jpg", "rb") as image_file:
    # Read the image file and encode it in base64
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    print (encoded_string)
