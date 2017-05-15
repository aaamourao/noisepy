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
#  glitchefx.py -- This belongs to noisepy
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
colorChannel constant: Color dictionary for translating RGB to
the numpy array position
"""
colorChannel = {'r' : 0, 'g' : 1, 'b' : 2}
"""
maxColorValue constant: The maximum color int value which each
pixel can assume.
"""
maxColorValue = 255

"""
imageio: lib for handling images as numpy arrays
"""
import imageio

class EffxHist:
    """
    Effect History class: Implements the effect history, **the Invoker** class,
    following the Command Design Pattern.

    Due to duck typing it is not necessary, or is unpythonic, creating an
    abstract method to define an interface. Thus, EffxHist checks on runtime
    if the given object is implemented concrete command.
    """
    def __init__(self, image, *, reverse=True):
        """
        _glitchin: every instance of EffxHist has its own glitch image
        generated from the same or from a different source image.

        Obs.: 'image' might be a ndarray or a string containing the
        path to the file
        """
        try:
            if isinstance(image, imageio.core.util.Image):
                self._glitchin = image
            elif isinstance(image, str):
                self._glitchin = imageio.imread(image)
            else:
                raise AttributeError("'image' input is not valid")
        except AttributeError as error:
            print('Attribute Error:', error)
            exit(1)

        """
        _cmdqueue: every instance of EffxHist has its own command queue.
        """
        self._cmdqueue = list()
        """
        _reverse: Holds a boolean value. If 'True', it is mandatory to
        all effects to implement the 'undo' operation
        """
        self._reverse = reverse

    @staticmethod
    def iseffect(defendant, *, reverse=True):
        """
        EffxHist: static method that checks if an object is an effect, which
        should implement the command interface
        """
        try:
            if not hasattr(defendant, 'execute'):
                raise NotImplementedError("no 'execute' operation implemented")
            if reverse and not hasattr(defendant, 'undo'):
                raise NotImplementedError("no 'undo' operation implemented")
        except NotImplementedError as message:
            print(defendant.__class__.__name__, ' not an real effect:', message)
            return False
        return True

    def enqueue(self, effect):
        """
        EffxHist:enqueue(): Append effect to the queue.
        """
        try:
            if not EffxHist.iseffect(effect, reverse=self._reverse):
                raise AttributeError("Only effects should be enqueued")
            self._cmdqueue.append(effect)
        except AttributeError as message:
            print('Could not enqueue:', message)
            exit(1)
        return True

    def execute(self):
        """
        EffxHist:execute(): Executes all the effects on the command queue.
        If some object doesn't has a execute method implemented, raises error.
        """
        try:
            for effect in self._cmdqueue:
                effect.execute()
        except NotImplementedError:
            print('Effect', effect.__class__.__name__, \
                    "isn't an effect: It doesn't implement a concrete command")
            # TODO: Undo all the effects that are already done
            exit(1)

    def undo(self):
        """
        EffxHist:undo(): Undo the command queue, checking if each
        element has the undo operation implemented
        """
        try:
            effect = self._cmdqueue.pop().undo()
        except NotImplementedError:
            print('Effect ', effect.__class__.__name__, 'cannot be undone')
            self._cmdqueue.append(effect)
            exit(1)

class Amp:
    """
    Amplifier class: Implements the **amplify** effect, a **Concrete command**,
    following the Command Design Pattern.
    """

    """
    Reference of the target image, which will be handled as a 3 channels signal.
    """
    _signal = None

    def __init__(self, pimage, setup):
        """
        Create Amplifier effect:
            pimage = image object which is being edited
            setup = gain and color(s) channel(s) [rgb]
        """
        self.setup = setup
        # TODO: Slice setup
        try:
            self.channels = 'r' # TODO: just for devel
            self.gain = 2 # TODO: just for devel
        except:
            print('Invalid Parameters')
            exit(1)

        # Check if pimage is a reference to a imageio object
        if not isinstance(pimage, imageio.core.util.Image):
            raise AttributeError('pimage should be a reference to', \
                    ' ndarray (imageio)')
        # Signal is a reference of pimage
        if Amp._signal == None:
            Amp._signal = pimage

    def execute(self):
        """
        Amp.execute() concrete effect command: amplify **channels**
        by a factor of **gain**
        """
        # Just a simple amp of each plane
        for ch in self.channels:
            Amp._signal[:,:,colorChannel[ch]] = \
                    self.gain*Amp._signal[:,:,colorChannel[ch]]
        return Amp._signal

    def undo(self):
        """
        Amp.undo(): remove the gain added to the signal
        """
        for ch in self.channels:
            Amp._signal[:,:,colorChannel[ch]] = \
                    Amp._signal[:,:,colorChannel[ch]]/self.gain
        return Amp._signal

class Inv:
    """
    Inversor class: Implements the **invert** effect, a concrete command,
    following the Command Design Pattern.
    """

    """
    Reference of the target image, which will be handled as a 3 channels signal.
    """
    _signal = None

    def __init__(self, pimage):
        """
        Just set Inv._signal if it wasn't done before
        """
        if Inv._signal == None:
            Inv._signal = pimage

    def execute(self):
        """
        Inv.execute() concrete effect command: invert **channels** values
        """
        Inv._signal = maxColorValue - Inv._signal

        return Inv._signal

    def undo(self):
        """
        Amp.undo(): remove the gain added to the signal
        """
        return self.execute()
