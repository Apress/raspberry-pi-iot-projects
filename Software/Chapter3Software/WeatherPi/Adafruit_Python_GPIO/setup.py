from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

import sys

# Define required packages.
requires = []
# Assume spidev is required on non-windows & non-mac platforms (i.e. linux).
if sys.platform != 'win32' and sys.platform != 'darwin':
    requires.append('spidev')

setup(name              = 'Adafruit_GPIO',
      version           = '0.8.0',
      author            = 'Tony DiCola',
      author_email      = 'tdicola@adafruit.com',
      description       = 'Library to provide a cross-platform GPIO interface on the Raspberry Pi and Beaglebone Black using the RPi.GPIO and Adafruit_BBIO libraries.',
      license           = 'MIT',
      url               = 'https://github.com/adafruit/Adafruit_Python_GPIO/',
      install_requires  = requires,
      packages          = find_packages())
