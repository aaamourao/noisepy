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
#  ./noisepy/util/core.py -- This belongs to noisepy
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
imageio: lib for handling images as numpy arrays
numpy: for complementary array operations
effxdic: all effects on a dictionary with their names on strings
util.effx: effects objects
"""
import imageio
import numpy
from util.tools import effxdic
from util.effx import *

class EffxBoard:
    """
    Effects Board class: Implements the effect history, **the Invoker** class,
    following the Command Design Pattern.

    Due to duck typing it is not necessary, or is unpythonic, creating an
    abstract method to define an interface. Thus, EffxBoard checks on runtime
    if the given object is implemented concrete command.
    """

    def __init__(self, image, *, reverse=True):
        """
        _glitchin: every instance of EffxBoard has its own glitch image
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
            print('Not valid image input')
            print(error)
            return
        except IOError as error:
            print('Error when opening image:', image)
            print(error)
            return
        """
        __cmdqueue: every instance of EffxBoard has its own command queue.
        """
        self.__cmdqueue = list()
        """
        __reverse: Holds a boolean value. If 'True', it is mandatory to
        all effects to implement the 'undo' operation
        """
        self.__reverse = reverse

    @staticmethod
    def iseffect(defendant, *, reverse=True):
        """
        EffxBoard: static method that checks if an object is an effect, which
        should implement the command interface
        """
        try:
            if not hasattr(defendant, 'execute'):
                raise NotImplementedError("no 'execute' operation implemented")
            if reverse and not hasattr(defendant, 'undo'):
                raise NotImplementedError("no 'undo' operation implemented")
        except NotImplementedError as message:
            return False
        return True

    def enqueue(self, effect, **setup):
        """
        EffxBoard:enqueue(): Append effect to the queue.
        """
        try:
            if isinstance(effect, str):
                print(setup)
                self.__cmdqueue.append(effxdic[effect](self.signal, **setup))
            elif not EffxBoard.iseffect(effect, reverse=self.__reverse):
                raise AttributeError("Only effects should be enqueued")
            else:
                self.__cmdqueue.append(effect)
        except AttributeError as error:
            print('Could not enqueue effect')
            print('AttributeError:', error)
            return False
        return True

    def execute(self, effect, **setup):
        """
        EffxBoard:execute(): add effect and execute it
        """
        try:
            if EffxBoard.iseffect(effect, reverse=self.__reverse):
                effxobj = effect
            elif isinstance(effect, str):
                if setup:
                    effxobj = effxdic[effect](self.signal, setup)
                else:
                    effxobj = effxdic[effect](self.signal)
            else:
                raise TypeError("Effect should be string containing the" \
                        "effect name, or an effect object")
            effxobj.execute()
            self.__cmdqueue.append(effxobj)
        except TypeError as error:
            print(error)
            return False
        return True


    def executeQueue(self):
        """
        EffxBoard:executeQueue(): Executes all the effects on the command queue.
        If some object doesn't has a execute method implemented, raises error.
        """
        # TODO: execute the non applyed effects from the queue
        try:
            for effect in self.__cmdqueue:
                effect.execute()
        except NotImplementedError:
            # TODO: Undo all the effects that are already done
            print('Effect', effect.__class__.__name__, \
                    "isn't an effect: It doesn't implement a concrete command")
            return False
        return True

    def save(self, path='./glitched.jpg'):
        """
        EffxBoard:save(): Saves ignal with applied effects as an image file.
        If path is not passed, the default, ./glitched.jpg, will be used.
        """
        self.currpath = path
        try:
            savingSignal = self.signal
            if numpy.all(self.signal[:,:,1:3]==0):
                """
                GrayScale only has one channel
                """
                savingSignal = self.signal[:,:,0]
            imageio.imwrite(path, savingSignal)
        except Exception as error:
            print('Could not save image')
            print(error)
            return False
        return True

    def undo(self):
        """
        EffxBoard:undo(): Undo the the last executed command on the queue,
        checking if each element has the undo operation implemented
        """
        try:
            effect = self.__cmdqueue.pop().undo()
        except NotImplementedError as error:
            print('Effect ', effect.__class__.__name__, 'cannot be undone')
            self.__cmdqueue.append(effect)
            print(error)
            return False
        return True
