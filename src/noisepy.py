#!/usr/bin/python3
#     ____ _     ___ _____ ____ _   _      _      ____    _____     _  _
#    / ___| |   |_ _|_   _/ ___| | | |    / \    |  _ \  |_   _|  _| || |
#   | |  _| |    | |  | || |   | |_| |   / _ \   | |_) |   | |   |_  ..  _|
#   | |_| | |___ | |  | || |___|  _  |  / ___ \  |  _ <    | |   |_      _|
#    \____|_____|___| |_| \____|_| |_| /_/   \_\ |_| \_\   |_|     |_||_|
#
# by
#      ___          ___         _____         ___          ___          ___
#     /__/\        /  /\       /  /::\       /  /\        /  /\        /__/\
#    |  |::\      /  /::\     /  /:/\:\     /  /:/       /  /::\      _\_ \:\
#    |  |:|:\    /  /:/\:\   /  /:/  \:\   /  /:/       /  /:/\:\    /__/\ \:\
#  __|__|:|\:\  /  /:/~/::\ /__/:/ \__\:| /  /:/  ___  /  /:/  \:\  _\_ \:\ \:\
# /__/::::| \:\/__/:/ /:/\:\\  \:\ /  /://__/:/  /  /\/__/:/ \__\:\/__/\ \:\ \:\
# \  \:\~~\__\/\  \:\/:/__\/ \  \:\  /:/ \  \:\ /  /:/\  \:\ /  /:/\  \:\ \:\/:/
#  \  \:\       \  \::/       \  \:\/:/   \  \:\  /:/  \  \:\  /:/  \  \:\ \::/
#   \  \:\       \  \:\        \  \::/     \  \:\/:/    \  \:\/:/    \  \:\/:/
#    \  \:\       \  \:\        \__\/       \  \::/      \  \::/      \  \::/
#     \__\/        \__\/                     \__\/        \__\/        \__\/
#
#  noisepy.py -- This belongs to noisepy
#
#  noisepy is a python module which implements methods for creating glitch art
#  pictures and movies
#
#  Copyright (C) 2017 madc0w - adriano mourao <madc0w@protonmail.ch>
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation; either version 3, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
#  for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import imageio

colorChannel = {'r' : 0, 'g' : 1, 'b' : 2}

def amplify(gain, channels, signal):
    # Just a simple amp of each plane
    for ch in channels:
        signal[:,:,colorChannel[ch]] = gain*signal[:,:,colorChannel[ch]]
    return signal

# Manual glitching interface: Check user inputs, open,
# create, and save images as numpy arrays...
def main():
    import os.path
    import argparse

    # Create argument parser object
    parser = argparse.ArgumentParser(
            description='Noisepy: Edit images as 3 channels signals.',
            epilog='A glitch art Python 3 module:' \
                    ' ==noisepy== by __madc0w__\n' \
                    'Distributed under GNU GPL v3.' \
                    ' Check COPYING file for more information'
            )

    # Load arguments
    parser.add_argument("-a", "--ampgain", type=float, help="Amplifier gain")
    parser.add_argument("-c", "--colors", nargs='+', choices=['r', 'g', 'b'],
            help="Color plane(s): RGB")
    parser.add_argument("input_path", help="Target image path")
    parser.add_argument("output_path", help="Output file path")

    # Parse arguments
    setup = parser.parse_args()

    # Check if some op was requested
    if not setup.ampgain or not setup.colors:
        parser.error("--ampgain and --colors values should be specified")

    # Check if input image exists and has permission
    try:
        if not os.path.isfile(setup.input_path):
            raise ValueError('Could not access image file. ' \
                    'If it exists, check its permissions')

        # Load image in a numpy array. It will contain a matrix with
        # an element for each picture. Each element is a 3 dimensional
        # vector. It will be treated it as a 3 channels signal.
        signal = imageio.imread(setup.input_path)
        output = amplify(setup.ampgain, setup.colors, signal)

        # Write the output image on target file
        imageio.imwrite(setup.output_path, output, 'jpg')
    except ValueError as message:
        print(message)

# Executing in a terminal
if __name__ == "__main__":
    main()
