# mondrimap
Piet Mondrian was a Dutch painter known for his abstract grids of primary colours and black lines. The name felt fitting for a tool that reduces images down to a grid of characters.

Converts images into ASCII art in your terminal.
Built as a small side project to mess around with PIL and terminal escape codes.
May be used for ricing if you're creative enough.
Supports colour output and an inverted character set for light backgrounds.

## Install
Clone the repo and run the setup script:
\```bash
git clone https://github.com/starcrossd/mondrimap
cd mondrimap
bash setup.sh
\```
The setup script installs Pillow if needed, adds a `mondrimap` alias to your shell rc file, then deletes itself. Restart your shell or source your rc file after.

> ⚠ Only bash and zsh are supported by the setup script. Fish/other shell users will need to add the alias manually.

## Usage
Run with no flags for interactive prompts:
\```bash
mondrimap
\```
You'll be asked for an image path and output width, then it'll print the ASCII and save a `.txt` next to the script.

### Flags
\```bash
mondrimap -m path/to/image.png   # skip the image path prompt
mondrimap -w 120                 # skip the width prompt
mondrimap -o path/to/out.txt     # custom output path
mondrimap -c                     # coloured output
mondrimap -i                     # inverted character set (for light backgrounds)
mondrimap -m img.png -w 120 -c -i  # everything at once
\```

## How it works
The script resizes your image to the specified width, then maps each pixel's brightness to a character from the set:
\```
@ # $ % ? * + ; : , .
\```
Dense → sparse, so dark pixels get `@` and light ones get `.`. Invert flips this for light backgrounds.

For colour mode it finds the nearest ANSI colour to each pixel using Euclidean distance in RGB space and wraps each character in the right escape code.

## Notes
- Output `.txt` won't preserve colour, just the characters
- 100–150 width is usually a good sweet spot — your terminal may need to match
- High contrast images work best; results vary a lot by source
