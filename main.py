#!/usr/bin/env python3
from PIL import Image, ImageSequence
import math
import os
import argparse
import time
import subprocess

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


        char = f"{ansicode}{char}{RESET}" if not args.background else f"\033[{40 + list(COLOURS.keys()).index(colour)}m{ansicode}{char}{RESET}"
        characters.append(char)
    return characters

def truecolourimg(pixels, pixelcolours, charset):
    for i, pixel in enumerate(pixels):
        char = charset[int(pixel)//25]

        cvalues = pixelcolours[i]

        truecolouransicode = f"\x1b[38;2;{cvalues[0]};{cvalues[1]};{cvalues[2]}m"

        char = f"{truecolouransicode}{char}{RESET}"  if not args.background else f"\x1b[48;2;{cvalues[0]};{cvalues[1]};{cvalues[2]}m{truecolouransicode}{char}{RESET}"
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

    asciiimage = "\n".join(["".join(characters[i:i+newwidth]) + RESET for i in range(0, pixelcount, newwidth)])

    return asciiimage

def saveascii(asciiimage):
    print(asciiimage)
    with open(outpath,"w") as f:
        f.write(asciiimage)
        print(f"ascii saved as {imgname}output.txt")

parser = argparse.ArgumentParser(prog='mondrimap', description='Converts images or gifs into ascii art\nThere are a lot of options to play around with but you dont need to use them all')

parser.add_argument('-img', '--img', default=None, help='File for the image, optional flag as file can be added even if not used')
parser.add_argument('-c', '--colour',action='store_true', help='Makes the resulting ascii colourful, using classic ansi escape codes')
parser.add_argument('-i', '--invert',action='store_true', help='Inverts the character set used')
parser.add_argument('-o', '--output', default=None, help='change the output path for your new image')
parser.add_argument('-w', '--width', help='specify the width of the image from the command')
parser.add_argument('-tc', '--truecolour',action='store_true', help='Much wider range of colours that can be displayed by terminal')
parser.add_argument('-s', '--save', action='store_true', help='Option to save file to prevent unecessary files being made')
parser.add_argument('-gif', '--gif', default=None, help='Allows you to use a gif rather than an image to convert')
parser.add_argument('-bg', '--background', action='store_true', help='Toggles the use of background colours to make the characters into full pixels')
parser.add_argument('-fps', '--frames', default=None, help='Allows you to set a custom fps')

args = parser.parse_args()

if args.gif:
    gifpath = args.gif

    pathparts = gifpath.split("/")
    gifname = pathparts[-1]
    nameparts = gifname.split(".")
    gifname = nameparts[0]

    outpath = args.output or os.path.join(BASEPATH,f'{gifname}-output.txt')

    frames = splitgif(args.gif)

    newwidth = int(args.width) if args.width else os.get_terminal_size().columns

    try:
        print("\033[?25l")

        asciiframes = []

        for frame in frames:
            characters = []
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

            asciiframes.append(formatchars(characters, newwidth))

        while True:
            for frame in asciiframes:
                print('\033[H', end='')
                start = time.time()

                print(frame)
                elapsed = time.time() - start

                sleepdur = 1 / int(args.frames) if args.frames else max(0, 0.05 - elapsed)
                time.sleep(sleepdur)

    except KeyboardInterrupt:
        print("\033[?25h", end="")
        subprocess.run(["clear"])


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
    newwidth = int(args.width) if args.width else os.get_terminal_size().columns

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
