```
     ___          ___                   ___          ___          ___
    /__/\        /  /\      ___        /  /\        /  /\        /  /\    ___
    \  \:\      /  /::\    /  /\      /  /:/_      /  /:/_      /  /::\  /__/|
     \  \:\    /  /:/\:\  /  /:/     /  /:/ /\    /  /:/ /\    /  /:/\:\|  |:|
 _____\__\:\  /  /:/  \:\/__/::\    /  /:/ /::\  /  /:/ /:/_  /  /:/~/:/|  |:|
/__/::::::::\/__/:/ \__\:\__\/\:\__/__/:/ /:/\:\/__/:/ /:/ /\/__/:/ /:/_|__|:|
\  \:\~~\~~\/\  \:\ /  /:/  \  \:\/\  \:\/:/~/:/\  \:\/:/ /:/\  \:\/:/__/::::\
 \  \:\  ~~~  \  \:\  /:/    \__\::/\  \::/ /:/  \  \::/ /:/  \  \::/   ~\~~\:\
  \  \:\       \  \:\/:/     /__/:/  \__\/ /:/    \  \:\/:/    \  \:\     \  \:\
   \  \:\       \  \::/      \__\/     /__/:/      \  \::/      \  \:\     \__\/
    \__\/        \__\/                 \__\/        \__\/        \__\/
             _____        ___
            /  /::\      /__/|
           /  /:/\:\    |  |:|
          /  /:/~/::\   |  |:|
         /__/:/ /:/\:|__|__|:|
         \  \:\/:/~/:/__/::::\
          \  \::/ /:/   ~\~~\:\
           \  \:\/:/      \  \:\
            \  \::/        \__\/
             \__\/
     ___          ___        _____        ___          ___          ___
    /__/\        /  /\      /  /::\      /  /\        /  /\        /__/\
   |  |::\      /  /::\    /  /:/\:\    /  /:/       /  /::\      _\_ \:\
   |  |:|:\    /  /:/\:\  /  /:/  \:\  /  /:/       /  /:/\:\    /__/\ \:\
 __|__|:|\:\  /  /:/~/::\/__/:/ \__\:|/  /:/  ___  /  /:/  \:\  _\_ \:\ \:\
/__/::::| \:\/__/:/ /:/\:\  \:\ /  /:/__/:/  /  /\/__/:/ \__\:\/__/\ \:\ \:\
\  \:\~~\__\/\  \:\/:/__\/\  \:\  /:/\  \:\ /  /:/\  \:\ /  /:/\  \:\ \:\/:/
 \  \:\       \  \::/      \  \:\/:/  \  \:\  /:/  \  \:\  /:/  \  \:\ \::/
  \  \:\       \  \:\       \  \::/    \  \:\/:/    \  \:\/:/    \  \:\/:/
   \  \:\       \  \:\       \__\/      \  \::/      \  \::/      \  \::/
    \__\/        \__\/                   \__\/        \__\/        \__\/

```

# Intro

**Noisepy** is a collection of all my glitch art scripts organized as a Python module. I will update the
project with new methods as soon as I get the code in a human-readble-like way.

Initialy, the main goal is to develop a Python 3 module with generic
transformation methods, which can be loaded with another python
tools. Thus, it will be part of a broader development-creative environment
for glitch artists

# Alpha "build"

```bash
pip install -r requirements.txt
chmod +x noisepy.py
```

# Usage

```bash
usage: noisepy.py [-h] [-a AMPGAIN] [-c {r,g,b} [{r,g,b} ...]]
                  input_path output_path

positional arguments:
  input_path            Target image path
  output_path           Output file path

optional arguments:
  -h, --help            show this help message and exit
  -a AMPGAIN, --ampgain AMPGAIN
                        Amplifier gain
  -c {r,g,b} [{r,g,b} ...], --colors {r,g,b} [{r,g,b} ...]
                        Color plane(s): RGB
```
