# asciify

Converts images into ascii art in your terminal.
Built as a small side project to mess around with PIL and terminal escape codes.
May be used for ricing if youre creative enough.
Supports colour output and an inverted character set for light backgrounds.

## Install
```bash
# This is a requirement for the program to run
pip install pillow
```

## Usage
```bash
python3 path/to/asciify.py
```
You'll get prompted for an image path and output width, then it'll print the ascii and save a `.txt` file next to the script.

### Flags
```bash
python3 asciify.py -c        # coloured output
python3 asciify.py -i        # inverted character set (for light backgrounds)

# The flags can be used at the same time to make an inverted, colourful output (order doesn't matter)
python3 asciify.py -i -c
```

## How it works

The script resizes your image to the width you specify, then maps each pixel's brightness to a character from the set:
```
@ # $ % ? * + ; : , .
```
Dense → sparse, so dark pixels get `@` and light ones get `.`. Invert flips this, useful if your terminal has a white background.

For colour mode it finds the nearest ANSI colour to each pixel using euclidean distance in RGB space and wraps the character in the right escape code.

## Notes
- Output `.txt` won't preserve colour, just the characters
- Wider = more detail, 100-150 is usually a good sweet spot, but your terminal/canvas may need to be larger to view it properly
- Results vary a lot by image — high contrast images look best
