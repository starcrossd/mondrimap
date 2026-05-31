from PIL import Image
import math

ASCII_CHARS = ["@","#","$","%","?","*","+",";",":",",","."]
RESET = '\033[0m'
COLOURS = {
    'black':'\033[30m',
    'red':'\033[31m',
    'green':'\033[32m',
    'yellow':'\033[33m',
    'blue':'\033[34m',
    'magenta':'\033[35m',
    'cyan':'\033[36m',
    'white':'\033[37m'
}
COLOURRGB = {
    'black':(0,0,0),
    'red':(255,0,0),
    'green':(0,255,0),
    'yellow':(255,255,0),
    'blue':(0,0,255),
    'magenta':(255,0,255),
    'cyan':(0,255,255),
    'white':(255,255,255)
}

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

greyscaleimg =  img.resize((newwidth,newheight)).convert("L")
newimg = img.resize((newwidth,newheight))

pixelcolours = list(newimg.get_flattened_data())
pixels = list(greyscaleimg.get_flattened_data())


characters = []
ansicode = RESET
for i, pixel in enumerate(pixels):
    colourrange = float('inf')
    char = ASCII_CHARS[int(pixel)//25]

    cvalues = pixelcolours[i]
    for colour, rgb in COLOURRGB.items():
        cr, cg, cb = rgb
        distance =  math.sqrt((cvalues[0]-cr)**2 + (cvalues[1]-cg)**2 + (cvalues[2]-cb)**2)
        if distance < colourrange:
            colourrange = distance
            ansicode = COLOURS[colour]


    char = f"{ansicode}{char}{RESET}"
    characters.append(char)


pixelcount = len(characters)

asciiimage = "\n".join(["".join(characters[i:i+newwidth]) for i in range(0, pixelcount, newwidth)])

print(asciiimage)
print(f"Height : {H}, Width : {W}")
with open(f"{imgname}output.txt", "w") as f:
    f.write(asciiimage)
    print(f"ascii saved as {imgname}output.txt")
