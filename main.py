#!/usr/bin/env python3
from PIL import Image, ImageSequence
import math
import os
import argparse
import time

BASEPATH = os.path.dirname(__file__)

ASCIICHARS = open(os.path.join(BASEPATH, 'charset.txt')).readlines()[0]

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

def colourimg(pixels, pixelcolours, charset):
    ansicode = RESET
    for i, pixel in enumerate(pixels):
        colourrange = float('inf')
        char = charset[int(pixel)//25]

        cvalues = pixelcolours[i]
        for colour, rgb in COLOURRGB.items():
            cr, cg, cb = rgb
            distance =  math.sqrt((cvalues[0]-cr)**2 + (cvalues[1]-cg)**2 + (cvalues[2]-cb)**2)
            if distance < colourrange:
                colourrange = distance
                ansicode = COLOURS[colour]


        char = f"{ansicode}{char}{RESET}"
        characters.append(char)
    return characters

def truecolourimg(pixels, pixelcolours, charset):
    for i, pixel in enumerate(pixels):
        char = charset[int(pixel)//25]

        cvalues = pixelcolours[i]

        truecolouransicode = f"\x1b[38;2;{cvalues[0]};{cvalues[1]};{cvalues[2]}m"

        char = f"{truecolouransicode}{char}{RESET}"
        characters.append(char)
    return characters

def blackandwhiteimg(pixels, charset):
    for pixel in pixels:
        characters.append(charset[int(pixel)//25])
    return characters

def splitgif(input_path):
    frames = []
    img = Image.open(input_path)

    for frame in ImageSequence.Iterator(img):
        frames.append(frame.copy())

    return frames

def formatchars(characters, newwidth):
    pixelcount = len(characters)

    asciiimage = "\n".join(["".join(characters[i:i+newwidth]) for i in range(0, pixelcount, newwidth)])

    return asciiimage

def saveascii(asciiimage):
    print(asciiimage)
    with open(outpath,"w") as f:
        f.write(asciiimage)
        print(f"ascii saved as {imgname}output.txt")

parser = argparse.ArgumentParser(prog='mondrimap', description='converts images into ascii art')

parser.add_argument('-img', '--img', default=None, help='File for the image, optional flag as file can be added even if not used')
parser.add_argument('-c', '--colour',action='store_true', help='Makes the resulting ascii colourful, using classic ansi escape codes')
parser.add_argument('-i', '--invert',action='store_true', help='Inverts the character set used')
parser.add_argument('-o', '--output', default=None, help='change the output path for your new image')
parser.add_argument('-w', '--width', help='specify the width of the image from the command')
parser.add_argument('-tc', '--truecolour',action='store_true', help='Much wider range of colours that can be displayed by terminal')
parser.add_argument('-s', '--save', action='store_true', help='Option to save file to prevent unecessary files being made')
parser.add_argument('-gif', '--gif', default=None, help='Allows you to use a gif rather than an image to convert')

args = parser.parse_args()

if args.gif:
    characters = []

    gifpath = args.gif

    pathparts = gifpath.split("/")
    gifname = pathparts[-1]
    nameparts = gifname.split(".")
    gifname = nameparts[0]

    outpath = args.output or os.path.join(BASEPATH,f'{gifname}-output.txt')

    frames = splitgif(args.gif)

    newwidth = int(args.width) or  int(input("How wide do you want the ascii version of the gif to be: "))

    while True:
        for frame in frames:
            W,H = frame.size

            ratio = W/H / 3

            newheight = math.floor(newwidth * ratio)

            greyscaleimg =  frame.resize((newwidth,newheight)).convert("L")
            newimg = frame.resize((newwidth,newheight)).convert("RGB")

            pixelcolours = list(newimg.get_flattened_data())
            pixels = list(greyscaleimg.get_flattened_data())

            charset = ASCIICHARS[::-1] if args.invert else ASCIICHARS
            if args.colour:
                characters = colourimg(pixels, pixelcolours, charset)
            elif args.truecolour:
                characters = truecolourimg(pixels, pixelcolours,charset)
            else:
                characters = blackandwhiteimg(pixels, charset)

            print(formatchars(characters, newwidth))
            time.sleep(0.1)


else:
    characters = []
    imgpath = args.img or input("Please provide a path for the image you want to abstract; ")

    pathparts = imgpath.split("/")
    imgname = pathparts[-1]

    nameparts = imgname.split(".")
    imgname = nameparts[0]

    outpath = args.output or os.path.join(BASEPATH,f'{imgname}-output.txt')

    img = Image.open(imgpath)
    W,H = img.size
    ratio = H/W / 3

    print(f"the ratio of height to width is {ratio},")
    newwidth = int(args.width) or  int(input("How wide do you want the ascii version of the image to be: "))

    newheight = math.floor(newwidth * ratio)

    greyscaleimg =  img.resize((newwidth,newheight)).convert("L")
    newimg = img.resize((newwidth,newheight))

    pixelcolours = list(newimg.get_flattened_data())
    pixels = list(greyscaleimg.get_flattened_data())

    charset = ASCIICHARS[::-1] if args.invert else ASCIICHARS
    if args.colour:
        characters = colourimg(pixels, pixelcolours, charset)
    elif args.truecolour:
        characters = truecolourimg(pixels, pixelcolours,charset)
    else:
        characters = blackandwhiteimg(pixels, charset)

    print(formatchars(characters, newwidth))

    if args.save or args.output:
        saveascii(formatchars(characters, newwidth))

# future plans : gif support, background removal, custom charsets
# highlight mode? highlighting specific colours in the img
