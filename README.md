
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

# Noisepy Setup

Check if **Python 3.5** is installed on your system. *Virtualenv* will
install the last *Python 3.5* version available, and noisepy should
work smoothly.

If **Python 3.5** is not installed and you can't or don't want to install
it, you should specify that you want **Python 3.5** on the virtualenv
creation.


```bash
$ python3 -m venv noisepy-env
$ . noisepy-env/bin/activate
$ pip install -r requirements.txt
$ chmod +x src/noisepy.py
```

You only need to do the last step, `chmod +x`, if you want to use noisepy
from the command line or inside *bash scrips*.

# Usage

The following image will be noisepy-ed to illustrate the usage example:

![Source Image: images/veneza.jpg](/images/veneza.jpg)

Amplifying the green channel by a factor of `2` from the command line:

```
$ cd src/
$ ./noisepy -c g -a 2 ../images/veneza.jpg ../glitch/glitched-images.jpg
```

![Output Image: glitched/veneza.jpg](/glitched/glitched-veneza.jpg)

## Help output

The **Help output** was developed using argparse and it only outputs
implemented features. Thus, it should be incremented in each step.
So far, only amplify was added to the module, so the help,
`-h or --help`, output looks like:

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

# License

All the photos in `/images` and `/glitched` were shot and edited
by me and they are distributed under the same copyleft license
than the code, **GPL**.
