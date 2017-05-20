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
#  ./noisepy/util/effx.py -- This belongs to noisepy
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
from .tools import _color2ch, _maxColVal, _regeffx

@_regeffx
class Amp:
    """
    Amplifier class: Implements the **amplify** effect, a **Concrete command**,
    following the Command Design Pattern.
    """
    def __init__(self, signal, gain=-0.1, channels=None, **setup):
        """
        Create Amplifier effect:
            signal = image array which is being edited
            setup = gain and color(s) channel(s) [rgb]
        """
        try:
            if not gain == 0.1 and not channels == None:
                self.channels = channels
                self.gain = gain
            elif len(setup) == 2:
                self.channels = setup['channels']
                self.gain = setup['gain']
            else:
                raise ValueError('Amp setup: gain(double) and channels (rgb)')
        except (ValueError, KeyError) as error:
            print('Invalid Amplifier parameters')
            print(error)
            return
        # Reference to image signal
        self.signal = signal

    def execute(self):
        """
        Amp.execute() concrete effect command: amplify **channels**
        by a factor of **gain**
        """
        for ch in self.channels:
            self.signal[:,:,_color2ch[ch]] = \
                    self.gain*self.signal[:,:,_color2ch[ch]]
        return True

    def undo(self):
        """
        Amp.undo(): remove the gain added to the signal
        """
        for ch in self.channels:
            self.signal[:,:,_color2ch[ch]] = \
                    self.signal[:,:,_color2ch[ch]]/self.gain
        return True

@_regeffx
class Inv:
    """
    Inversor class: Implements the **invert** effect, a concrete command,
    following the Command Design Pattern.
    """
    def __init__(self, signal, channels=None, **setup):
        """
        Just set Inv.signal if it wasn't done before
        """
        try:
            if isinstance(channels, str):
                self.chs = channels
            elif channels == None and len(setup) == 1:
                self.chs = setup['channels']
            else:
                raise AttributeError("Inv requires channels parameter, rgb")
        except AttributeError as error:
            print('Could not create Inv instance')
            print('AttributeError:', error)
            return
        self.signal = signal

    def execute(self):
        """
        Inv.execute() concrete effect command: invert **channels** values:
            _maxColVal(==255) - signal[:,:,channel]
        """
        for ch in self.chs:
            self.signal[:,:,_color2ch[ch]] = \
                    _maxColVal - self.signal[:,:,_color2ch[ch]]
        return True

    def undo(self):
        """
        Inv.undo(): undo the invertion by applying it again
        """
        self.execute()
        return True

@_regeffx
class GrayScale:
    """
    GrayScale class: set the image to gray scale color set
    """
    def __init__(self, signal):
        """
        Saves a reference to the signal
        """
        self.signal = signal

    def execute(self):
        """
        Removes green and blue color planes and saves
        that for an eventual undo
        Returns the signal, due to new reference
        """
        self.recover = self.signal[:,:,1:3].copy()
        self.signal[:,:,0] = 0.299*self.signal[:,:,0] +\
                0.587*self.signal[:,:,1] + 0.114*self.signal[:,:,2]
        self.signal[:,:,1:3] = 0
        return True

    def undo(self):
        """
        Add the previously saved color planes to
        the signal
        """
        self.signal[:,:,1:3] = self.recover[1:3]
        return True
