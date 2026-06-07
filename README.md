# mondrimap
> Piet Mondrian reduced the world to grids of primary colours and black lines. This reduces images to grids of characters.

Converts images to ASCII art in your terminal. Built to mess around with PIL and terminal escape codes. Supports colour output and an inverted charset for light backgrounds.

| Truecolour | Ansi Colours |
|---|---|
| ![demo - moodyblues trucolour](imgs/moodyblues.png)  | ![demo - purplehaze base ansi colour](imgs/purplehaze.png) |

| Black and White | Gifs |
|----|
| ![demo - ryu black and white ](imgs/ryu.png) | ![demo - donut gif](imgs/donut.gif) |


## Install
```bash
git clone https://github.com/starcrossd/mondrimap
cd mondrimap
bash setup.sh
```
The setup script installs Pillow if needed, adds a `mondrimap` alias to your shell rc file, then deletes itself. Restart your shell or source your rc file after.

> ⚠️ Only bash and zsh are supported. Fish/other shell users will need to add the alias manually.

---

## Usage
Run without flags for interactive prompts:
```bash
mondrimap
```
You'll be asked for an image path and output width. The ASCII output is printed to the terminal and saved as a `.txt` next to the script.

### Flags
| Flag | Description |
|------|-------------|
| `-img path/to/image.png` | Image path (skips prompt) |
| `-gif path/to/anim.gif` | GIF path — plays in terminal on loop |
| `-w 120` | Output width in characters (skips prompt) |
| `-o path/to/out.txt` | Custom output path |
| `-c` | Colour output |
| `-i` | Invert charset (for light backgrounds) |
| `-tc` | Truecolour output |
| `-s` | Save the output to a file |

```bash
mondrimap -img photo.png -w 120 -c -i
mondrimap -gif anim.gif -w 80 -tc
```

---

## How it works
The script resizes your image to the specified width, then maps each pixel's brightness to a character:
```
@ # $ % ? * + ; : , .
```
Dense → sparse: dark pixels get `@`, light ones get `.`. `-i` flips this for light backgrounds.

Colour mode finds the nearest ANSI colour to each pixel using Euclidean distance in RGB space, then wraps each character in the matching escape code.

GIF mode splits each frame, converts it, and plays them back in a loop directly in your terminal. Frame timing is fixed at 100ms — close with `Ctrl+C`.

---

## Notes
- `.txt` output won't preserve colour — just the characters
- 100–150 width is usually a good sweet spot; your terminal width should match
- High contrast images work best
- GIFs play on loop until interrupted — best viewed in a terminal that supports truecolour
