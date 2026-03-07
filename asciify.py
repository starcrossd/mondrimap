from PIL import Image
import math

ASCII_CHARS = ["@","#","$","%","?","*","+",";",":",",","."]

imgpath = input("Please provide a path for the image you wanna ascii-ify; ")
pathparts = imgpath.split("/")
imgname = pathparts[-1]

nameparts = imgname.split(".")
imgname = nameparts[0]


img = Image.open(imgpath)
W,H = img.size[0], img.size[1]
ratio = H/W / 3

print(f"the ratio of height to width is {ratio},")
newwidth = int(input("How wide do you want the ascii version of the image to be: "))

newheight = math.floor(newwidth * ratio) 

newimg =  img.resize((newwidth,newheight)).convert("L")

pixels = list(newimg.get_flattened_data())
characters = "".join([ASCII_CHARS[int(pixel)//25] for pixel in pixels])

pixelcount = len(characters)

asciiimage = "\n".join([characters[i:(i+newwidth)] for i in range(0,pixelcount,newwidth)])

print(asciiimage)
print(f"Height : {H}, Width : {W}")
with open(f"{imgname}output.txt", "w") as f:
    f.write(asciiimage)
    print(f"ascii saved as {imgname}output.txt")
