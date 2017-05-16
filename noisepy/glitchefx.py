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
            """
            signal: static variable which holds the image represented as
            a 3 channels signal, an imageio object
            """
            if isinstance(image, imageio.core.util.Image):
                self.signal = image
            elif isinstance(image, str):
                self.signal = imageio.imread(image)
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
        # TODO: It is possible to create effect object when enqueue-ing
        try:
            if not EffxHist.iseffect(effect, reverse=self._reverse):
                raise AttributeError("Only effects should be enqueued")
            self._cmdqueue.append(effect)
        except AttributeError as message:
            print('Could not enqueue:', message)
            exit(1)
        return True

    def execute(self, effect, **setup):
        """
        EffxHist:execute(): add effect and execute it
        """
        try:
            if EffxHist.iseffect(effect, reverse=self._reverse):
                newEffect = effect
            elif isinstance(effect, str):
                module = __import__(module_name)
                effectClass_ = getattr(module, effect)

                if not effectClass:
                    raise ValueError("Effect not found:", effect)

                # TODO: Strip setup
                newEffect = effectClass(setup)
            else:
                raise TypeError("Effect should be string containing the" \
                        "effect name, or an effect object")
            newEffect.execute()
            self._cmdqueue.append(effect)
        except:
            # TODO: catch the correct exceptions
            exit(1)
        return True


    def executeQueue(self):
        """
        EffxHist:executeQueue(): Executes all the effects on the command queue.
        If some object doesn't has a execute method implemented, raises error.
        """
        # TODO: execute the non applyed effects from the queue
        try:
            for effect in self._cmdqueue:
                effect.execute()
        except NotImplementedError:
            print('Effect', effect.__class__.__name__, \
                    "isn't an effect: It doesn't implement a concrete command")
            # TODO: Undo all the effects that are already done
            exit(1)
        return True

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
        return True

class Amp:
    """
    Amplifier class: Implements the **amplify** effect, a **Concrete command**,
    following the Command Design Pattern.
    """
    def __init__(self, signal, gain, channels):
        """
        Create Amplifier effect:
            signal = image array which is being edited
            setup = gain and color(s) channel(s) [rgb]
        """
        try:
            self.channels = channels
            self.gain = gain
        except:
            print('Invalid Parameters')
            exit(1)
        # Reference to image signal
        self._signal = signal

    def execute(self):
        """
        Amp.execute() concrete effect command: amplify **channels**
        by a factor of **gain**
        """
        for ch in self.channels:
            self._signal[:,:,colorChannel[ch]] = \
                    self.gain*self._signal[:,:,colorChannel[ch]]
        return True

    def undo(self):
        """
        Amp.undo(): remove the gain added to the signal
        """
        for ch in self.channels:
            self._signal[:,:,colorChannel[ch]] = \
                    self._signal[:,:,colorChannel[ch]]/self.gain
        return True

class Inv:
    """
    Inversor class: Implements the **invert** effect, a concrete command,
    following the Command Design Pattern.
    """
    def __init__(self, signal):
        """
        Just set Inv._signal if it wasn't done before
        """
        self._signal = signal

    def execute(self):
        """
        Inv.execute() concrete effect command: invert **channels** values:
            maxColorValue(==255) - signal[:,:,channel]
        """
        self._signal = maxColorValue - self._signal
        return True

    def undo(self):
        """
        Inv.undo(): undo the invertion by applying it again
        """
        self.execute()
        return True
