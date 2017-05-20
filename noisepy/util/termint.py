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
"""
Terminal Interface module:
    Does the argument parsing before create effect object. It is not
    necessary to create a EffxBoard instance, since only a single
    effect will be applied.
"""
import os.path
import argparse
import sys
import util.effx

class TermInt(object):
    def __init__(self):
        # TODO: Command Pattern
        print('Hey, implement me, please')

    @classmethod
    def commandLine():
        """
        commandLine is a method which implements the
        common steps that every effect should do when
        called from the command line.
        """
        # Create argument parser object
        parser = argparse.ArgumentParser(
                description='Noisepy: Edit images as a 3 channels signal',
                epilog='A Glitch Art Python 3 module:' \
                        ' ===noisepy=== by ___madc0w___ !' \
                        ' Distributed under GNU GPL v3.' \
                        ' Check COPYING file for more information')
        # All effects must-have arguments
        parser.add_argument("infile", help="Target image path")
        parser.add_argument("outfile", help="Output file path")

        # Parse arguments
        setup = parser.parse_args()
        # Check if input image exists and has permission
        try:
            if not os.path.isfile(setup.input_path):
                raise ValueError('Could not access image file. ' \
                        'If it exists, check its permissions')
        except ValueError as message:
            print(message)
        # Check if parameters were specified
        if not setup.colors:
            setup.colors = 'rgb'

        """
        Create subparsers for subcommands as a class attribute
        """
        self.subparsers = parser.add_subparsers(help='Effect to process', \
                dest="command")

        # Check if the requested command exists
        if not hasattr(self, subparsers.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        # Load image in a numpy array
        signal = imageio.imread(setup.input_path)
        # Compute the requested signal processing function
        proc_sig = getattr(self, str(self.subparsers.command))()
        # Write the output image on target file
        imageio.imwrite(setup.output_path, proc_sig, 'jpg')

    def amplifier(self):
        """
        Amplifier implements the amplify processing on a
        3 channels signal, s[R, G, B], when called as a command.
        So it sets its help parameter table and check if they were
        passed corretly.
        """

        # Create parser for "amplifier" command
        parser_amp = self.subparsers.add_parser("amplifier", \
                help="Select amplifier signal edition")
        parser_amp.add_argument("-a", "--ampgain", type=float,
                help="Amplifier gain")
        parser_amp.add_argument("-c", "--colors", nargs='+',
                choices=['r', 'g', 'b'],
                help="Color plane(s) that will be edited: RGB")

        # Check if there are amplifier specific required parameters
        if not setup.ampgain:
            parser.error("--ampgain is required")

        # TODO: Call effect and return result
        return 0

    def inversor(self):
        """
        Inversor implements a simple color inversion when called as
        a command. It checks if the parameters were passed corretly
        and feeds its help parameter table.
        """
        parser_inv = subparsers.add_parser("inversor", help="Select inversor" \
                " signal edition")
        parser_inv.add_argument("-c", "--colors", nargs='+',
                choices=['r', 'g', 'b'],
                help="Color plane(s) that will be edited: RGB")
        parser_inv.add_argument("input_path", help="Target image path")
        parser_inv.add_argument("output_path", help="Output file path")

if __name__ == "__main__":
    """
    When executed from the command line
    """
    NoisePy.commandLine()
