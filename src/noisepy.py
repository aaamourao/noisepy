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
maxColorValue = 255

def amplify(gain, channels, signal):
    # Copy input signal
    out = signal
    # Just a simple amp of each plane
    for ch in channels:
        out[:,:,colorChannel[ch]] = gain*signal[:,:,colorChannel[ch]]
    return out

def invert(channels, signal):
    out = maxColorValue - signal
    return out

# Manual glitching interface: Check user inputs, open,
# create, and save images as numpy arrays...
def main():
    import os.path
    import argparse

    # Create argument parser object
    parser = argparse.ArgumentParser(
            description='Noisepy: Edit images as a 3 channels signal',
            epilog='A Glitch Art Python 3 module:' \
                    ' ===noisepy=== by ___madc0w___ !' \
                    ' Distributed under GNU GPL v3.' \
                    ' Check COPYING file for more information'
            )
    # Create sub-parsers for sub-commands
    subparsers = parser.add_subparsers(help='sub-command help', dest="command")

    # Create parser for "amplifier" command
    parser_amp = subparsers.add_parser("amplifier", help="Select amplifier" \
            " signal edition")
    parser_amp.add_argument("-a", "--ampgain", type=float, help="Amplifier gain")
    parser_amp.add_argument("-c", "--colors", nargs='+', choices=['r', 'g', 'b'],
            help="Color plane(s) that will be edited: RGB")
    parser_amp.add_argument("input_path", help="Target image path")
    parser_amp.add_argument("output_path", help="Output file path")

    parser_inv = subparsers.add_parser("inversor", help="Select inversor" \
            " signal edition")
    parser_inv.add_argument("-c", "--colors", nargs='+', choices=['r', 'g', 'b'],
            help="Color plane(s) that will be edited: RGB")
    parser_inv.add_argument("input_path", help="Target image path")
    parser_inv.add_argument("output_path", help="Output file path")

    # Parse arguments
    setup = parser.parse_args()
    # Check if parameters were specified
    if not setup.colors:
        parser.error("--colors should be specified")
    if setup.command == 'amplifier':
        # Check if some op was requested
        if not setup.ampgain:
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
        if setup.command == 'amplifier':
            output = amplify(setup.ampgain, setup.colors, signal)
        elif setup.command == 'inversor':
            output = invert(setup.colors, signal)

        # Write the output image on target file
        imageio.imwrite(setup.output_path, output, 'jpg')
    except ValueError as message:
        print(message)

# Executing in a terminal
if __name__ == "__main__":
    main()
