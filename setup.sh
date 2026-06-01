#!/usr/bin/bash
SCRIPTDIR=$(dirname "$(realpath "$0")")
PYFILE="$SCRIPTDIR/main.py"

SHELLTYPE=$SHELL
ALIASADDPATH=""

COMMANDSTR="python3 $PYFILE"

source /etc/os-release

command -v python3 || { echo "python3 not found, please install it."; exit 1; }

echo "Enter password to confrim the installation for the pillow python library"
if [[ $ID == "arch" ]]; then
    sudo pacman -S python-pillow
elif [[ $ID == "ubuntu" || $ID == "debian" ]]; then
    sudo apt install python3-pil -y
else
    python3 -m pip install pillow --break-system-packages
fi

if [[ $SHELLTYPE == *bash* ]]; then
    ALIASADDPATH="$HOME/.bashrc"
else
    ALIASADDPATH="$HOME/.zshrc"
fi

echo "#made by setup.sh for mondrimap" >> $ALIASADDPATH
echo "alias mondrimap='$COMMANDSTR'" >> $ALIASADDPATH

source $ALIASADDPATH

echo "The setup file will now delte itself, thank you for installinf mondrimap"
(sleep 1 && rm -- "$0") &
