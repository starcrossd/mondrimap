# mondrimap
Converts images into ASCII art in your terminal.
Built as a small side project to mess around with PIL and terminal escape codes.
May be used for ricing if you're creative enough.
Supports colour output and an inverted character set for light backgrounds.

## Install
Clone the repo and run the setup script:
```bash
git clone https://github.com/starcrossd/mondrimap
cd mondrimap
bash setup.sh # The setup script makes the program executable from anywhere through one key word
```
Then restart your shell or source your rc file.

## Usage
Just run:
```bash
mondrimap
```
You'll get prompted for an image path and output width, then it'll print the ASCII and save a `.txt` file next to the script.

### Flags
```bash
mondrimap -c        # coloured output
mondrimap -i        # inverted character set (for light backgrounds)
mondrimap -i -c     # both at once (order doesn't matter)
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
- Wider = more detail, 100-150 is usually a good sweet spot, but your terminal may need to be wider to view it properly
- Results vary a lot by image — high contrast works best
