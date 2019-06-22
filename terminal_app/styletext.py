#!/usr/bin/env python3
import os


class ColorText:

    def __init__(self, color, text):
        """
        ColorText('color', 'Text to be colorized')
        Takes a color and "text" as input and outputs relevent stylized text
        to stdout.
        Options:
            : red
            : blue
            : green
            : yellow
            : cyan
            : white
        """
        if color == "red":
            os.system('echo "\033[1;31m {} \033[0m"'.format(text))
        elif color == "blue":
            os.system('echo "\033[1;34m {} \033[0m"'.format(text))
        elif color == "green":
            os.system('echo "\033[1;32m {} \033[0m"'.format(text))
        elif color == "yellow":
            os.system('echo "\033[1;33m {} \033[0m"'.format(text))
        elif color == "cyan":
            os.system('echo "\033[1;36m {} \033[0m"'.format(text))
        elif color == "white":
            os.system('echo "\033[1;37m {} \033[0m"'.format(text))

        
    def clear_screen(self):
        os.system("clear")