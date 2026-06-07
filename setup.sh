#!/usr/bin/bash
SCRIPTDIR=$(dirname "$(realpath "$0")")
PYFILE="$SCRIPTDIR/main.py"

SHELLTYPE=$SHELL
ALIASADDPATH=""
CHARSET="@#$%?*+;:,."

COMMANDSTR="python3 $PYFILE"

source /etc/os-release

command -v python3 || { echo "python3 not found, please install it."; exit 1; }

python3 -c "import PIL" 2>/dev/null && echo "pillow is installed." || { ISPILLOWINSTALLED=0; echo "pillow needs installation"; }

if [[ $ISPILLOWINSTALLED == 0 ]]; then
    echo "Enter password to confrim the installation for the pillow python library"
    if [[ $ID == "arch" ]]; then
        sudo pacman -S python-pillow
    elif [[ $ID == "ubuntu" || $ID == "debian" ]]; then
        sudo apt install python3-pil -y
    else
        python3 -m pip install pillow --break-system-packages
    fi
fi

if [[ $SHELLTYPE == *bash* ]]; then
    ALIASADDPATH="$HOME/.bashrc"
else
    ALIASADDPATH="$HOME/.zshrc"
fi

read -p "Would you like to keep the 'imgs/' folder in the repository as example screenshots? [y/n]: " KEEPIMGS
if [[ ${KEEPIMGS,,} == "n" ]]; then
    rm -rf imgs/
fi

echo "This is the default character set for the ascii images produced:"
echo $CHARSET
read -p "Would you like to use the default character set? (recommended) [y/n]: " KEEPCHARS
if [[ ${KEEPCHARS,,} == "y" ]]; then
    echo $CHARSET > $SCRIPTDIR/"charset.txt"
else
    read -p "What set of characters would you like to use? (it can later be changed in ${SCRIPTDIR}/.charset.txt)" CHARSET
    echo $CHARSET > $SCRIPTDIR/"charset.txt"
fi

echo "#made by setup.sh for mondrimap" >> $ALIASADDPATH
echo "alias mondrimap='$COMMANDSTR'" >> $ALIASADDPATH

source $ALIASADDPATH

echo "The setup file will now delete itself, thank you for installing mondrimap"
(sleep 1 && rm -- "$0") &
